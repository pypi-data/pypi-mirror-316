from datetime import datetime
from enum import Enum
import json
import os
from uuid import UUID
from pymongo import MongoClient
from dateutil import parser
import requests
from a2ginputstream.inputstream import INSERTION_MODE, Inputstream


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return str(obj)
        else:
            return super().default(obj)

class CustomJsonDecoder(json.JSONDecoder):
    def __init__(self, *args ,**kargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kargs)

    def object_hook(self, obj:dict):
        for k, v in obj.items():
            if isinstance(v, str) and 'T' in v and '-' in v and ':' in v and len(v) < 40:
                try:
                    dv = parser.parse(v)
                    dt = dv.replace(tzinfo=None)
                    obj[k] = dt
                except:
                    pass
        return obj

# Environment production
A2G_DATA_URL        = os.environ.get("DATA_URL"         , "https://v2streams.a2g.io")
A2G_QUERY_MANAGER   = os.environ.get("QUERY_MANAGER"    , "https://v2streams.a2g.io")  
A2G_INPUTSTREAM_URL = os.environ.get("INPUTSTREAM_URL"  , "https://v2apigateway.a2g.io")

# Environment development
# A2G_DATA_URL        = os.environ.get("DATA_URL", "https://localhost:1008")
# A2G_QUERY_MANAGER   = os.environ.get("QUERY_MANAGER", "http://localhost:1012")
# A2G_INPUTSTREAM_URL = os.environ.get("INPUTSTREAM_URL", "https://localhost:1000")

mongo_conn  = os.environ.get("DATA_MONGO_CONN", None)
mongo_db    = os.environ.get("DATA_DB_NAME", None)
print(f"mongo_conn: {mongo_conn}, mongo_db: {mongo_db} from cloud_inputstream.py")

class A2GHttpClient():

    def __init__(self, token):
        self.token = token


    def get_inputstream_by_ikey(self, ikey:str) -> Inputstream:
        try:
            headers = { "Authorization": f"A2G {self.token}"}
            res = requests.get(A2G_INPUTSTREAM_URL + f"/Inputstream/Ikey/{ikey}", headers=headers, verify=False)
            if res.status_code != 200:
                print(res.status_code, res.text) 
                if res.status_code == 404: raise Exception("Inputstream not found, please check your ikey")
                if res.status_code == 401: raise Exception("Unauthorized: please check your token or access permissions")
                if res.status_code == 403: raise Exception("Forbidden: please check your access permissions")
                raise Exception("Error al obtener el inputstream")
            content = res.json(cls=CustomJsonDecoder)
            if not content["success"]: raise Exception(content["errorMessage"])
            return Inputstream(from_response=True, **content["data"])
        except Exception as e:
            raise e
    

    def insert(self, ikey:str, data:list[dict], mode:INSERTION_MODE, wait_response:bool) -> tuple[int, str]:
        try:
            headers = {
                "Authorization": f"A2G {self.token}",
                "ikey": ikey
            }

            if mode == INSERTION_MODE.REPLACE: 
                headers["Replace"] = "true"
                headers["Transaction"] = "false"

            elif mode == INSERTION_MODE.INSERT_UNORDERED: 
                headers["Replace"] = "false"
                headers["Transaction"] = "false"

            elif mode == INSERTION_MODE.TRANSACTION:
                headers["Replace"] = "false"
                headers["Transaction"] = "true"

            if wait_response: headers["WaitResponse"] = "true"

            res = requests.post(A2G_DATA_URL + "/Data/Insert", headers=headers, json=data, verify=False)
            if res.status_code != 200: raise Exception("Error al obtener el inputstream")
            return res.status_code, res.text
        except Exception as e:
            raise e
        
        

class CloudInputstream:

    def __init__(self, token:str, **kwargs):
        self.token  = token
        if mongo_conn is None or mongo_db is None:
            raise Exception("Missing MONGO_CONN or DB_NAME environment variables")
        self.client = MongoClient(mongo_conn)
        self.db     = self.client[mongo_db]
        self.inputstreams: dict[str, Inputstream] = {}
        self.a2g_client = A2GHttpClient(token)


    def get_inputstream(self, ikey:str, **kwargs) -> Inputstream:
        """
        return Inputstream
        """
        inputstream = self.inputstreams.get(ikey, None)
        if inputstream is None:
            inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
            self.inputstreams[ikey] = inputstream
        
        return inputstream


    def get_inputstream_schema(self, ikey:str, cache:bool=True, **kwargs) -> dict:
        """
        return Inputstream schema
        params:
            ikey: str
            cache: bool = True -> if True, use cache if exists and is not expired
        """
        inputstream = self.inputstreams.get(ikey, None)
        if inputstream is None:
            inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
            self.inputstreams[ikey] = inputstream
        
        return json.loads(inputstream.Schema)


    def find(self, ikey:str, query:dict, cache:bool=True, **kwargs):
        """
        return data from inputstream
        params:
            ikey: str
            query: dict
        """
        inputstream = self.inputstreams.get(ikey, None)
        if inputstream is None:
            inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
            self.inputstreams[ikey] = inputstream
        coll_name = inputstream.CollectionName
        data = list(self.db[coll_name].find(query))
        for d in data: d.pop("_id")
        return data


    def find_one(self, ikey:str, query:dict, cache:bool=True, **kwargs):
        """
        return one data from inputstream
        params:
            collection: str
            query: dict
        """
        inputstream = self.inputstreams.get(ikey, None)
        if inputstream is None:
            inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
            self.inputstreams[ikey] = inputstream
        coll_name = inputstream.CollectionName
        doc = self.db[coll_name].find_one(query)   
        if doc is not None: doc.pop("_id")
        return doc
     

    def get_data_aggregate(self, ikey:str, query: list[dict], cache:bool=True, **kwargs):
        """
        return data from inputstream
        params:
            ikey: str
            query: list[dict]
        """
        inputstream = self.inputstreams.get(ikey, None)
        if inputstream is None:
            inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
            self.inputstreams[ikey] = inputstream
        coll_name = inputstream.CollectionName
        data = list(self.db[coll_name].aggregate(query))
        for d in data: 
            if "_id" in d: d.pop("_id")

        return data
    

    def insert_data(self, ikey:str, data:list[dict], mode:INSERTION_MODE = INSERTION_MODE.REPLACE, wait_response = True, batch_size:int=1000, cache:bool=True):
        """
        validate data against inputstream JsonSchema and insert into inputstream collection
        params:
            ikey: str
            data: list[dict]
        """
        inputstream = self.inputstreams.get(ikey, None)
        if inputstream is None:
            inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
            self.inputstreams[ikey] = inputstream


        data_parsed = json.loads(json.dumps(data, cls=CustomJSONEncoder)) 
                
        # insert data into inputstream collection in batch size of 1000
        # TODO: Optimizar para asyncio
        for i in range(0, len(data_parsed), batch_size):
            code, message = self.a2g_client.insert(ikey, data_parsed[i:i+batch_size], mode, wait_response)
            batch_size_aux = batch_size if i+batch_size < len(data_parsed) else len(data_parsed) - i
            print(f"batch {(i//batch_size) + 1}, docs: [{i} - {i+batch_size_aux}] - {code} - {message}")
    

    def remove_documents(self, ikey:str, query:dict) -> int:
        """
        delete data from inputstream
        params:
            ikey: str
            query: dict
        """
        inputstream = self.inputstreams.get(ikey, None)
        if inputstream is None:
            inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
            self.inputstreams[ikey] = inputstream
        coll_name = inputstream.CollectionName
        if len(query) == 0: raise Exception("Query is empty, you must provide a valid query, if you want to delete all data, use clear_inputstream method")
        docs = self.db[coll_name].delete_many(query)
        return docs.deleted_count

    
    def clear_inputstream(self, ikey:str) -> int:
        """
        delete all data from inputstream
        params:
            ikey: str
        """
        inputstream = self.inputstreams.get(ikey, None)
        if inputstream is None:
            inputstream = self.a2g_client.get_inputstream_by_ikey(ikey)
            self.inputstreams[ikey] = inputstream
        coll_name = inputstream.CollectionName
        docs = self.db[coll_name].delete_many({})
        return docs.deleted_count