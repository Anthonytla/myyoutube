from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()
cors = CORS()