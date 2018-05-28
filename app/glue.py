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
import api.googlemap as map
import matplotlib.pyplot as plt
# import mpld3
import os
# import app.db as db

candidates = cur.build_suburb_list()
lga_dict = cur.get_lga()
ROOT = os.getcwd()
FIGURE_PATH = ROOT + '/templates/static/figures/'


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
    p = wiki.get_info(suburb_name)
    return p.content.split('\n'), p.images


def get_rates(suburb_name):
    crime_rate = list(crime.get_mark(suburb_name).values())[0]
    acc_rate = list(acc.get_mark(suburb_name).values())[0]
    poi_rates = list(poi.get_info(suburb_name)[1].values())
    poi_rate = sum(poi_rates) / len(poi_rates)

    tmp = [round(crime_rate), round(acc_rate), round(poi_rate * 20)]

    all_rates = sum(tmp) / 3

    tmp.append(all_rates)

    res = [str(e) for e in tmp]

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
    _acc_list = get_accommodation(lga)
    _acc = []
    for acc in _acc_list:
        tmp_avg = acc['Bedroom_number.total']
        l_offset = tmp_avg.find('(')
        r_offset = tmp_avg.find(')')
        avg = tmp_avg[l_offset + 1: r_offset]
        if avg == '':
            avg = 0
        tmp = {'type': acc['dewelling_type '],
               'average': float(avg)}
        _acc.append(tmp)
    _poi_list = get_poi(suburb_name)
    _poi = []
    for poi in _poi_list[0]:
        tmp = {'name': poi['poiname: '],
               'type': poi['poitype: ']
               }
        _poi.append(tmp)
    _wiki = get_wiki_info(suburb_name)
    suburb = Suburb(suburb_name, _crime, _acc, (_poi, _poi_list[1]), _wiki)

    rates = get_rates(lga)

    suburb.set_rates(rates[0], rates[1], rates[2], rates[3])
    suburb.set_lga(lga)

    acc_path = draw_acc_plot(suburb)
    poi_path = draw_poi_plot(suburb)

    suburb.set_figure_paths(acc_path, poi_path)

    suburb.set_poi_locations(get_poi_locations(suburb))

    # db.save_doc(suburb)

    return suburb


def draw_acc_plot(suburb_obj):
    _name = suburb_obj.lga
    _acc = suburb_obj.acc_stats
    _index = []
    _value = []
    for e in _acc:
        _index.append(e['type'])
        _value.append(e['average'])

    plt.bar(_index, _value, width=0.5, color='#41A4C3')
    # fig = plt.gcf()
    # plt.show()
    filename = _name + '_acc.png'
    path = FIGURE_PATH + filename
    plt.savefig(path)
    plt.close()
    return filename


def draw_poi_plot(suburb_obj):
    _name = suburb_obj.name
    _poi = suburb_obj.poi_rate
    _index = []
    _value = []
    for key, value in _poi.items():
        _index.append(key)
        _value.append(value)

    plt.bar(_index, _value, width=0.5, color='#41A4C3')
    # fig = plt.gcf()
    # plt.show()
    filename = _name + '_poi.png'
    path = FIGURE_PATH + filename
    plt.savefig(path)
    plt.close()
    return filename


def get_poi_locations(suburb_obj):
    poi_list = []
    for e in suburb_obj.poi:
        poi_list.append(e['name'])

    tmp = map.get_info(poi_list)
    res = []
    for k, v in tmp.items():
        res.append({'lat': v[0], 'lng': v[1]})

    return res



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
# get_poi_locations(obj)
# draw_acc_plot(obj)
# draw_poi_plot(obj)
# print(obj)
# draw_plot(1,1,1)
# with open('Kingsford.pkl', 'wb') as output:
#     pickle.dump(obj, output)
# # print(get_suburb_obj('Kingsford'))
# print()
# print(candidates)