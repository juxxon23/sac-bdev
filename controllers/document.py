from flask.views import MethodView
from flask import jsonify, request
from marshmallow import validate
from helpers.document_tool import DocumentTool
from db.mongodb.mongodb_manager import MongoDBManager
from validators.document_val import DocumentVal, DocumentUpdate
from db.postgresql.postgresql_manager import PostgresqlManager
from db.postgresql.model import User

doc_tool = DocumentTool()
doc_schema = DocumentVal()
doc_up_schema = DocumentUpdate()
mongo_tool = MongoDBManager()
postgres_tool = PostgresqlManager()

class Document(MethodView):

    def get(self):
        try:
            id_acta = request.headers.get('id_a')
            if id_acta == None:
                docs = mongo_tool.get_all_docs()
                docs_list = []
                for doc in docs:
                    docs_list.append({
                        '_id': str(doc['_id']),
                        'document_u': doc['document_u'],
                        'format_id': doc['format_id']
                    })
                return jsonify({'docs': docs_list}), 200
            else:
                doc_user = mongo_tool.get_by_id(id_acta)
                template_url = doc_tool.template_selector(doc_user['format_id'])
                template = doc_tool.read_html(template_url)
                u = {
                    'document_u': doc_user['document_u'],
                    'content': doc_user['content']
                    }
                return jsonify({'us': u, 'template': template}), 200
        except Exception as ex:
            return jsonify({'status':'exception', 'ex': str(ex)}), 400

    def post(self):
        try:
            data = request.get_json()
            errors = doc_schema.validate(data)
            if errors:
                return jsonify({'status':'error', 'errors':errors}), 400
            msg = mongo_tool.add_doc(data)
            if msg == 'error':
                return jsonify({"status": "add error"}), 400
            else:
                user_cred = postgres_tool.get_by(User, data['document_u'])
                if user_cred == None or type(user_cred) == dict:
                    user_cred = 'no-data'
                u = {
                    'document': user_cred.document_u,
                    'email': user_cred.email_inst,
                    'name': user_cred.name_u,
                    'lastname': user_cred.lastname_u,
                    'phone': user_cred.phone_u,
                    'regional': user_cred.regional_u,
                    'center': user_cred.center_u,
                    'bonding': user_cred.bonding_type
                }
                template_url = doc_tool.template_selector(data['format_id'])
                template = doc_tool.read_html(template_url)
                answ = {'id_acta': str(msg), 'us': u, 'template': template}
                return jsonify({"format": answ, "status": "ok"}), 200     
        except Exception as ex:
            return jsonify({"status":"exception", "ex": str(ex)}), 400
    
    def put(self):
        try:
            data = request.get_json()
            errors = doc_up_schema.validate(data)
            if errors:
                return jsonify({'status':'validation_error', 'errors':errors}), 400
            content = doc_tool.get_content_data(data['content'])
            msg = mongo_tool.update_doc(data['id_acta'], data['document_u'], content)
            if msg == 'ok':
                return jsonify({"status": "ok"}), 200    
            else:
                return jsonify({"status": "update error", "ex": msg}), 400         
        except Exception as ex:
            return jsonify({"status":"exception", "ex":str(ex)}), 400