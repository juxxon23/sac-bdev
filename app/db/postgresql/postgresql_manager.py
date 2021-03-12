from app.db.postgresql.model import db
from sqlalchemy.exc import SQLAlchemyError


class PostgresqlManager:

    def add(self, *args):
        try:
            for new in args:
                db.session.add(new)
                db.session.commit()
            return 'ok'
        except SQLAlchemyError as e:
            error_msg = {'exception': 'sqlalchemy add', 'ex': str(e)}
            return error_msg
        except Exception as ex:
            error_msg = {'exception': 'postgres_tool add', 'ex': str(ex)}
            return error_msg

    def update(self):
        try:
            db.session.commit()
            return 'ok'
        except SQLAlchemyError as e:
            error_msg = {'exception': 'sqlalchemy update', 'ex': str(e)}
            return error_msg
        except Exception as ex:
            error_msg = {'exception': 'postgres_tool update', 'ex': str(ex)}
            return error_msg

    def delete(self, obj):
        try:
            db.session.delete(obj)
            db.session.commit()
            return 'ok'
        except SQLAlchemyError as e:
            error_msg = {'exception': 'sqlalchemy delete', 'ex': str(e)}
            return error_msg
        except Exception as ex:
            error_msg = {'exception': 'postgres_tool delete', 'ex': str(ex)}
            return error_msg

    def get_all(self, table_name):
        try:
            data = db.session.query(table_name).all()
            return data
        except SQLAlchemyError as e:
            error_msg = {'exception': 'sqlalchemy get_all', 'ex': str(e)}
            return error_msg
        except Exception as ex:
            error_msg = {'exception': 'postgres_tool get_all', 'ex': str(ex)}
            return error_msg

    # table.query.filter_by(col=data).first()
    def get_by(self, table_name, value):
        try:
            data = db.session.query(table_name).filter_by(
                document_u=value).first()
            return data
        except SQLAlchemyError as e:
            error_msg = {'exception': 'sqlalchemy get_by', 'ex': str(e)}
            return error_msg
        except Exception as ex:
            error_msg = {'exception': 'postgres_tool get_by', 'ex': str(ex)}
            return error_msg

    def get_by_email(self, table_name, value):
        try:
            print('1')
            data = db.session.query(table_name).filter_by(
                email_inst=value).first()
            print('2')
            return data
        except SQLAlchemyError as e:
            error_msg = {'exception': 'sqlalchemy get_by', 'ex': str(e)}
            return error_msg
        except Exception as ex:
            error_msg = {'exception': 'postgres_tool get_by', 'ex': str(ex)}
            return error_msg
