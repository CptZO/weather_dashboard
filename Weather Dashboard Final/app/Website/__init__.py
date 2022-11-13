from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "weather.db"


def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = "has}G_,lO<s@/='Btq74p09*(popsda"

	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	from.views import views

	app.register_blueprint(views, url_prefix="/")

	create_database(app)

	return app


def create_database(app):
	if not path.exists('Website/'+DB_NAME):
		db.create_all(app=app)
		print('Created Database!')
	else:
		print('Database Already Exists!')
