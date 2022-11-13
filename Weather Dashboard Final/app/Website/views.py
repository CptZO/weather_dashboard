import json

from flask import Blueprint, render_template, request, redirect, url_for, flash
from .weather import *
from . import db
from .models import City

views = Blueprint('views', __name__)


@views.route("/", methods=['POST'])
def home_post():
	ERROR_MSG = ""

	new_city = request.form.get('city')
	if new_city:
		exists = City.query.filter_by(name=new_city).first()
		if exists:
			ERROR_MSG = "City Already Exists"
		else:
			new_city_data = get_weather_data(new_city)
			if new_city_data['cod'] == 200:
				new_city_obj = City(name=new_city)

				db.session.add(new_city_obj)
				db.session.commit()
			else:
				ERROR_MSG = 'City does not Exist'

		if ERROR_MSG:
			flash(ERROR_MSG, 'error')
		else:
			flash('City added!')

	return redirect(url_for('views.home_get'))


@views.route("/")
def home_get():
	cities = City.query.all()

	URL = "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=30bbb19aad4badf2852e44ab8517fc0d"
	weather_data = []

	for city in cities:
		response = get_weather_data(city.name)

		weather = {
			"city": city.name,
			"temperature": response['main']['temp'],
			"description": response['weather'][0]['description'],
			"icon": response['weather'][0]['icon']
		}

		weather_data.append(weather)

	return render_template("home.html", weather_data=weather_data)


@views.route("/delete/<name>")
def delete_city(name):
	city = City.query.filter_by(name=name).first()
	db.session.delete(city)
	db.session.commit()

	return redirect(url_for('views.home_get'))
