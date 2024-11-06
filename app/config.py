from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from flask_redis import FlaskRedis
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

import os
import secrets
from datetime import timedelta


## charge enviroment variables
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# secret key for mongo session
tokens_session = secrets.token_hex(20)
app.config["SECRET_KEY"] = tokens_session

# Cors config
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = tokens_session
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
jwt = JWTManager(app)

app.config['TIMEZONE'] = 'America/Bogota'

app.config['X-API-KEY'] = os.getenv("X_API_KEY")

# Swagger config
template = {
    "swagger": "2.0",
    "info": {
        "title": "Users management microservice",
        "description": "Microservice created by me",
        "contact": {
            "responsibleOrganization": "DeijoseDevelop",
            "responsibleDeveloper": "DeijoseDevelop",
            "email": "estudiandovazmore@gmail.com",
        },
        "version": "0.1.0"
    },
}

# Machine learning config
app.config["model"] = "/home/DeijoseDevelop/ml_u_backend/app/modules/category_classificator/train_models/model.joblib"
app.config["vectorizer"] = "/home/DeijoseDevelop/ml_u_backend/app/modules/category_classificator/train_models/vectorizer.joblib"
app.config["recognition_data"] = "/home/DeijoseDevelop/ml_u_backend/app/modules/user_recognition/train_data/images"
app.config["classification_data"] = "/home/DeijoseDevelop/ml_u_backend/app/modules/category_classificator/train_data/test_data.xlsx"

swagger = Swagger(app, template=template)

app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")

# Redis config
# app.config['REDIS_URL'] = "redis://localhost:6379/0"
# redis_client = FlaskRedis(app)
# redis = redis_client.provider_class()