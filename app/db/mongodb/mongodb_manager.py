from flask_pymongo import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import current_app as app

client = pymongo.MongoClient(app.config['MONGO_URI'], ssl=True, ssl_cert_reqs='CERT_NONE')
mongo = client.get_database("sac-ddb")

class MongoDBManager():

    def add_doc(self, doc_data):
        try:
            id_doc = mongo.documents.insert(doc_data)
            return id_doc
        except Exception as ex:
            error_msg = {'error': 'mongodb_tool add_doc', 'ex': str(ex)}
            return error_msg

    def delete_doc(self, id_acta):
        try:
            mongo.documents.delete_one({'_id':  ObjectId(id_acta)})
            return 'ok'
        except Exception as ex:
            error_msg = {'error': 'mongodb_tool delete_doc', 'ex': str(ex)}
            return error_msg

    def update_doc(self, id_acta, doc, cont):
        try:
            up_doc = mongo.documents.update_one(
                {'_id':  ObjectId(id_acta)},
                {'$set': {'document_u': doc, 'content': cont}}
            )
            return 'ok'
        except Exception as ex:
            error_msg = {'error': 'mongodb_tool update_doc', 'ex': str(ex)}
            return error_msg

    def get_all_docs(self):
        try:
            docs = mongo.documents.find()
            #docs_d = dumps(docs)
            return docs
        except Exception as ex:
            error_msg = {'error': 'mongodb_tool get_all_docs', 'ex': str(ex)}
            return error_msg

    def get_by_id(self, id_acta):
        try:
            doc = mongo.documents.find_one({'_id': ObjectId(id_acta)})
            return doc
        except Exception as ex:
            error_msg = {'error': 'mongodb_tool get_by_id', 'ex': str(ex)}
            return error_msg
