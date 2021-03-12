
class PostgresqlError:


    def msg(self, error):
        if error == None:
            msg = {'status': 'user', 'msg': 'The user doesn\'t exists'}
            return msg
        elif type(error) == dict:
            msg = {'status': error['exception'], 'ex': error['ex']}
            return msg
        else:
            msg = {'status': 'ok'}
            return msg
