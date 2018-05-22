'''
Author: @MH
Top-level flask APIs using internal APIs in ./api
'''

from flask import render_template, Flask, redirect, url_for, make_response
from flask import Blueprint
import flask_restful
from flask import request as re  # avoid duplicate names
from app.views import bp
from app.models import Suburb
import api.accommodation as acc
import api.crime as crime
import api.poi as poi



# app = Blueprint('app', __name__, url_prefix='')
app = bp


# @app.route("/results/crime/<suburb_name>", methods=['POST'])
def get_crime(suburb_name):
    return crime.get_info(suburb_name)



# @app.route("/results/poi/<suburb_name>", methods=['POST'])
def get_poi(suburb_name):
    return poi.get_info(suburb_name)


# @app.route("/results/accommodation/<suburb_name>", methods=['POST'])
def get_accommodation(suburb_name):
    return acc.get_info(suburb_name)


@bp.route('/search', methods=['POST'])
def search():
    parser = re.RequestParser()
    parser.add_argument('rt', type=str)
    args = parser.parse_args()

    # postcode = re.form.get("postcode")
    suburb_name = re.form.get('suburb')

    crime = get_crime(suburb_name)
    acc = get_accommodation(suburb_name)
    poi = get_poi(suburb_name)
    suburb_obj = Suburb(suburb_name, crime, acc, poi)

    return url_for('.suburb', suburb=suburb_obj)
