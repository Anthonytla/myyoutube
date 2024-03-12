from flask import Flask
import os

#app = Flask(__name__, static_url_path='/home/laanthony/myYoutube/api/static/', 
app = Flask(__name__, static_url_path='/static/', 
            static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/myapi'
app.config['SECRET_KEY'] = 'dev'
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
app.config["ERROR_404_HELP"] = False
app.config['CORS_HEADERS'] = 'Content-Type'
# Other FLASK config varaibles ...
#app.config["ALLOWED_EXTENSIONS"] = ["jpg", "png", "mov", "mp4", "mpg"]
#app.config["MAX_CONTENT_LENGTH"] = 1000 * 1024 * 1024  # 1000mb

#app.config["MAX_CONTENT_LENGTH"] = 100 * 10 * 1

from core.extensions import db, bcrypt, ma, cors
db.init_app(app)
bcrypt.init_app(app)
ma.init_app(app)
cors.init_app(app)

from resources import api
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')