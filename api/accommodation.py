'''
Accommodation API
Author: LY
Sample payload:
sample1
{
    "_id": 4,
    "suburb": "Total",
    "dewelling_type": "Total",
    "bedroom_number": [
        {
            "total": "370.0 ~ 600.0 ( 481.67 )",
            "not_specified": "360.0 ~ 590.0 ( 466.67 )",
            "one_bedroom": "339.0 ~ 550.0 ( 448.0 )",
            "two_bedrooms": "360.0 ~ 620.0 ( 485.0 )",
            "three_bedrooms": "370.0 ~ 600.0 ( 473.33 )",
            "four_or_more_bedrooms": "450.0 ~ 720.0 ( 576.67 )",
            "bedsitter": "320.0 ~ 460.0 ( 391.67 )",
            "_cls": "Bedroom_number"
        }
    ]
}
sample2
{
    "_id": 32,
    "suburb": "Total",
    "dewelling_type": "Flat/Unit",
    "bedroom_number": [
        {
            "total": "380.0 ~ 620.0 ( 500.0 )",
            "not_specified": "360.0 ~ 580.0 ( 463.33 )",
            "one_bedroom": "364.0 ~ 560.0 ( 466.33 )",
            "two_bedrooms": "380.0 ~ 650.0 ( 510.0 )",
            "three_bedrooms": "440.0 ~ 870.0 ( 646.67 )",
            "four_or_more_bedrooms": "450.0 ~ 1075.0 ( 741.67 )",
            "bedsitter": "320.0 ~ 450.0 ( 383.33 )",
            "_cls": "Bedroom_number"
        }
    ]
}
'''


# print(get_mark('Wentworth'))
# {'Townhouse': 100.0}
# print(get_mark('Randwick'))
# {'Townhouse': 42.98}
# print(get_mark('Albury'))
# {'Total': 40.68}
# print(get_mark('Armidale Regional'))
# {'House': 59.09}
# print(get_mark('Blacktown'))
# {'House': 37.2}


from mongoengine import StringField, IntField, Document, EmbeddedDocument, ListField
from mongoengine import connect
import xlrd

# acc_db = connect(host="mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3", alias='acc')

class Bedroom_number(EmbeddedDocument):
    total = StringField(required=True)
    not_specified = StringField(required=True)
    one_bedroom = StringField(required=True)
    two_bedrooms = StringField(required=True)
    three_bedrooms = StringField(required=True)
    four_or_more_bedrooms = StringField(required=True)
    bedsitter = StringField(required=True)

    def __init__(self, total, not_specified, one_bedroom, two_bedrooms, three_bedrooms,
                 four_or_more_bedrooms, bedsitter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total = total
        self.not_specified = not_specified
        self.one_bedroom = one_bedroom
        self.two_bedrooms = two_bedrooms
        self.three_bedrooms = three_bedrooms
        self.four_or_more_bedrooms = four_or_more_bedrooms
        self.bedsitter = bedsitter

class Accommodation(Document):
    id = IntField(required=True, primary_key=True)
    suburb = StringField(required=True)
    dewelling_type = StringField(required=True)
    bedroom_number = ListField(required=True)

    def __init__(self, id, suburb, dewelling_type, bedroom_number = [], *args, **values):
        super().__init__(*args, **values)
        self.id = id
        self.suburb = suburb
        self.dewelling_type = dewelling_type
        self.bedroom_number = bedroom_number

def excel_to_json(name):
    data = xlrd.open_workbook(name)
    table = data.sheets()[1]
    nrows = table.nrows
    # print("nrows ", nrows)

    for i in range(4,nrows-7,7):
        if table.row_values(i)[4] != 'Other':
            suburb = table.row_values(i)[3]
            dewelling_type = table.row_values(i)[4]

            bn = {'Total': '-', 'Not Specified': '-', '1 Bedroom': '-', '3 Bedrooms': '-',
                  '2 Bedrooms': '-', '4 or more Bedrooms': '-', 'Bedsitter': '-'}
            for j in range(7):
                if suburb == table.row_values(i+j)[3]:
                    if table.row_values(i+j)[6] != '-' and table.row_values(i+j)[7] != '-' and table.row_values(i+j)[8] != '-':
                        avg_range = str(table.row_values(i+j)[6]) + ' ~ ' + str(table.row_values(i+j)[8])
                        mean = str(round((int(table.row_values(i+j)[6]) + int(table.row_values(i+j)[7])
                                          + int(table.row_values(i+j)[8]))/3,2))
                        bn[table.row_values(i+j)[5]] = avg_range + ' ( ' + mean + ' )'
                else:
                    break
            # print(bn)
            db_json = Accommodation(i, suburb, dewelling_type,
                                    [Bedroom_number(bn['Total'],bn['Not Specified'],bn['1 Bedroom'],
                                                    bn['2 Bedrooms'],bn['3 Bedrooms'],
                                                    bn['4 or more Bedrooms'],bn['Bedsitter'])])
            connect(host="mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3")
            # connect(db='comp9321_ass3')
            db_json.save()

# excel_to_json('Rent.xlsx')
def show_info(suburb):
    connect('accommodation', host="mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3")
    # connect('accommodation')
    # connect(db='comp9321_ass3')
    info = []
    dewelling_type = ['Total','House','Townhouse','Flat/Unit']
    for i in Accommodation.objects(suburb=suburb):
        if i.dewelling_type in dewelling_type:
            dewelling_type.remove(i.dewelling_type)
            spec_info = {}
            spec_info.update({'dewelling_type ':i.dewelling_type})
            for j in i.bedroom_number:
                spec_info.update({'Bedroom_number.total': j.total})
                spec_info.update({'Bedroom_number.not_specified': j.not_specified})
                spec_info.update({'Bedroom_number.one_bedroom': j.one_bedroom})
                spec_info.update({'Bedroom_number.two_bedrooms': j.two_bedrooms})
                spec_info.update({'Bedroom_number.three_bedrooms': j.three_bedrooms})
                spec_info.update({'Bedroom_number.four_or_more_bedrooms': j.four_or_more_bedrooms})
                spec_info.update({'Bedroom_number.bedsitter': j.bedsitter})
            info.append(spec_info)
    if not info:
        return show_info(suburb='Total')
    return info

# print(show_info('randwick'))

def get_mark(suburb):
    '''
    get highest price performance ratio & corresponding dewelling type
    if mark == 0, it means that Not found related data
    :param suburb: suburb
    :return: dictionary{corresponding dewelling type: float(max score in four types)}
    '''
    raw_list = show_info(suburb)
    sum_price_dic = {}
    price_performance_ratio = {}
    for raw in raw_list:
        if raw['Bedroom_number.total'] == '-':
            price_ratio = 0 #'Not Found Related Data'
        else:
            sum_price = 0
            for e in raw.keys():
                if e != 'Bedroom_number.total' and e != 'dewelling_type ':
                    if raw[e] != '-':
                        # print(e, raw[e])
                        sum_price += float(raw[e].split(' ')[-2])
            price_ratio = round(sum_price/(6*float(raw['Bedroom_number.total'].split(' ')[-2]))*100,2)
        sum_price_dic.update({raw['dewelling_type ']: price_ratio})
    for key in sum_price_dic.keys():
        if sum_price_dic[key] == max(sum_price_dic.values()):
            price_performance_ratio = {key: round(max(sum_price_dic.values())/sum(sum_price_dic.values())*100,2)}
    return price_performance_ratio

# print(get_mark('Albury'))

def get_info(suburb_name):
    # excel_to_json(suburb_name)
    return show_info(suburb_name)


# if __name__ == '__main__':
    # connect(host="mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3", username='ass3', password='ass3',
    #         alias='acc')


