'''

Author: @MH
Top-level flask APIs using internal APIs in ./api

'''

from flask import render_template, Flask, redirect, url_for, make_response
from flask import Blueprint
import flask_restful
from flask import request as re  # avoid duplicate names
# from app.views import bp
from app.models import Suburb
import api.accommodation as acc
import api.crime as crime
import api.poi as poi
import api.wiki as wiki
import api.curation as cur
# import app.db as db

candidates = cur.build_suburb_list()
lga_dict = cur.get_lga()


# app = Blueprint('app', __name__, url_prefix='')
# app = bp


# @app.route("/results/crime/<suburb_name>", methods=['POST'])
def get_crime(suburb_name):
    return crime.get_info(suburb_name)


# @app.route("/results/poi/<suburb_name>", methods=['POST'])
def get_poi(suburb_name):
    return poi.get_info(suburb_name)


# @app.route("/results/accommodation/<suburb_name>", methods=['POST'])
def get_accommodation(suburb_name):
    return acc.get_info(suburb_name)


def get_wiki_info(suburb_name):
    return wiki.get_info(suburb_name)


def get_rates(suburb_name):
    crime_rate = list(crime.get_mark(suburb_name).values())[0]
    acc_rate = list(acc.get_mark(suburb_name).values())[0]
    poi_rates = list(poi.get_info(suburb_name)[1].values())
    poi_rate = sum(poi_rates) / len(poi_rates)

    res = [crime_rate / 100 * 5, acc_rate / 100 * 5, poi_rate]

    all_rates = sum(res) / 3
    res.append(all_rates)

    return res


def check_input(suburb_name):
    if suburb_name in candidates:
        return True
    return False


def correct_input(suburb_name):
    return cur.typo_check(suburb_name)


def get_suburb_obj(suburb_name):

    # if db.is_stored(suburb_name):
    #     res = db.get_doc(suburb_name)
    #     return res

    lga = lga_dict[suburb_name]

    _crime = get_crime(lga)
    _acc = get_accommodation(lga)
    _poi = get_poi(suburb_name)
    _wiki = get_wiki_info(suburb_name)
    suburb = Suburb(suburb_name, _crime, _acc, _poi, _wiki)

    rates = get_rates(lga)

    suburb.set_rates(rates[0], rates[1], rates[2], rates[3])
    suburb.set_lga(lga)

    # db.save_doc(suburb)

    return suburb


# # @bp.route('/search', methods=['POST'])
# def search():
#     # parser = re.RequestParser()
#     # parser.add_argument('rt', type=str)
#     # args = parser.parse_args()
#
#     # postcode = re.form.get("postcode")
#     suburb_name = re.form.get('suburb')
#
#     crime = get_crime(suburb_name)
#     acc = get_accommodation(suburb_name)
#     poi = get_poi(suburb_name)
#     suburb_obj = Suburb(suburb_name, crime, acc, poi)
#
#     return redirect(url_for('.suburb', suburb=suburb_name))


# routes = dict(
#     rule='/search/',
#     endpoint='search',
#     view_func=search,
#     options=dict(methods=['POST']))

# print(get_rates('Randwick'))
# import _pickle as pickle
# obj = get_suburb_obj('Kingsford')
# with open('Kingsford.pkl', 'wb') as output:
#     pickle.dump(obj, output)
# # print(get_suburb_obj('Kingsford'))
# print()