from mongoengine import StringField, IntField, Document, EmbeddedDocument, ListField, EmbeddedDocumentField
from mongoengine import connect
import xlrd


class Postcode(Document):
    id = IntField(required=True, primary_key=True)
    suburb = StringField(required=True)
    postcode = StringField(required=True)

    def __init__(self, id, lga_region, postcode, *args, **values):
        super().__init__(*args, **values)
        self.id = id
        self.suburb = lga_region
        self.postcode = postcode

def excel_to_json(name):
    data = xlrd.open_workbook(name)
    table = data.sheets()[0]
    nrows = table.nrows
    print("nrows ", nrows)

    for i in range(1, nrows):
        # print('table.row_values(i) ', table.row_values(i))
        lga_region = table.row_values(i)[1]
        postcode = table.row_values(i)[2]
        db_json = Postcode(i, lga_region, str(postcode))
        connect(host = "mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3")
        db_json.save()
        # d2.save()

excel_to_json('nsw_postcode.xlsx')