from flask import Flask, jsonify
from flask_restful import reqparse
from mongoengine import StringField, IntField, Document, EmbeddedDocument, ListField, EmbeddedDocumentField
from mongoengine import connect
import xlrd
import requests
import os

# connect(host="mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3")

class Crime(Document):
    crime_type = StringField(required=True)
    trend_24month = StringField(required=True)
    trend_60month = StringField(required=True)

    def __init__(self, crime_type, trend_24month, trend_60month, *args, **values):
        super().__init__(*args, **values)
        self.crime_type = crime_type
        self.trend_24month = trend_24month
        self.trend_60month = trend_60month

# method for download the lga
def get_and_save_lga(suburb):
    '''
    下载下来一个 crime的excel表
    :param suburb: input的值
    :return: 内存中存在相应的excel表
    '''
    url = "http://www.bocsar.nsw.gov.au/Documents/RCS-Annual/" + suburb + "LGA.xlsx"
    r = requests.get(url)
    with open(suburb + ".xlsx", 'wb') as f:
        f.write(r.content)


def crime_excel_to_json(filename):
    '''
    将下载下来的 crime excel表，已json的形式输出
    :param filename: suburb+'.xlsx'
    :return: json(crime_type(highest_rate),trend_24month,trend_60month)
    '''
    try:
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        rank = 100000000000000
        rate_24month = 0
        rate_60month = 0
        trend_24month, trend_60month = None, None
        # print(table.row_values(7)[14] == ' ')
        count = 17
        for i in range(7, 23):
            try:
                if int(table.row_values(i)[14]) < rank:
                    crime_type = table.row_values(i)[1]
                    rank = int(table.row_values(i)[14])
                    count -= 1
                else:
                    count -= 1
            except:
                crime_type = None
            try:
                if float(table.row_values(i)[12]) > rate_24month:
                    rate_24month = float(table.row_values(i)[12])
                    trend_24month = table.row_values(i)[1]
            except:
                pass
            try:
                if float(table.row_values(i)[13]) > rate_60month:
                    rate_60month = float(table.row_values(i)[13])
                    trend_60month = table.row_values(i)[1]
            except:
                pass
        # print(crime_type, trend_24month, trend_60month)
        # print(crime_type,highest_rate)
    except:
        crime_type, trend_24month, trend_60month = 'Not Found Related Data', 'Not Found Related Data', 'Not Found Related Data'
        count = 170000
    # print('count ',count)
    db_json = Crime(crime_type, trend_24month, trend_60month)
    dictionary = {'crime_type': db_json.crime_type, 'trend_24month_crime_type': db_json.trend_24month,
                  'trend_60month_crime_type': db_json.trend_60month}
    return dictionary, count

def delete_excel(filename):
    '''
    删除已存在的crime excle表
    :param filename: suburb+'.xlsx'
    :return: 
    '''
    if os.path.isfile(filename):
        os.remove(filename)

def show_info(suburb):
    get_and_save_lga(suburb)
    filename = suburb + '.xlsx'
    dictionary, count = crime_excel_to_json(filename)
    delete_excel(filename)
    return dictionary

# sample1
# d = show_info('Randwick')
# print(d)
# {'trend_24month_crime_type': None, 'crime_type': 'Steal from person', 'trend_60month_crime_type': 'Sexual assault'}
# sample2
# d = show_info('Sydney')
# print(d)
# {'trend_24month_crime_type': 'Indecent assault, act of indecency and other sexual offences', 'trend_60month_crime_type': 'Indecent assault, act of indecency and other sexual offences', 'crime_type': None}
# sample3
# d = show_info('kengsinton')
# print(d)
# {'trend_24month_crime_type': 'Not Found Related Data', 'trend_60month_crime_type': 'Not Found Related Data', 'crime_type': 'Not Found Related Data'}

def get_mark(suburb):
    '''
    
    :param suburb: 
    :return: dictionary{safety: score}
    '''
    get_and_save_lga(suburb)
    filename = suburb + '.xlsx'
    dictionary, count = crime_excel_to_json(filename)
    if round(count/17*100,2) <= 100:
        mark = str(round(count/17*100,2)) + '%'
    else:
        mark = 'Not Found Related Data'
    safety = {'safety': mark}
    delete_excel(filename)
    return safety

# sample1
# m = get_mark('Randwick')
# print(m)
# {'safety': '29.41%'}
# sample2
# m = get_mark('Sydney')
# print(m)
# {'safety': '100.0%'}
# sample3
# m = get_mark('kengsinton')
# print(m)
# {'safety': 'Not Found Related Data'}

    

