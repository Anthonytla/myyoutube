from flask import Flask
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
#app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://root:root@localhost/db_name'
#db = SQLAlchemy(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)