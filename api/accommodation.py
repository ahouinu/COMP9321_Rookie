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

from mongoengine import StringField, IntField, Document, EmbeddedDocument, ListField, EmbeddedDocumentField
from mongoengine import connect
import xlrd


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
            connect(host = "mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3")
            db_json.save()


# TODO: Call this function @MH
def get_info(suburb):
    '''
    :param suburb: 'suburb name'
    :return: list of info (could be empty)
    '''
    connect(host="mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3")
    info = []
    # TEST ONLY
    _override = 'Sydney'
    suburb = _override
    for i in Accommodation.objects:
        if i.suburb.lower() == suburb.lower():
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
    return info

# print(show_info('Albury'))


# print(get_info('kingsford'))
