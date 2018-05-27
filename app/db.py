from mongoengine import connect
from app.models import Suburb
from datetime import datetime, timedelta

host = 'mongodb://rookie:rookie@ds235850.mlab.com:35850/rookie'
db = connect(db='rookie', username='rookie', password='rookie', host=host, port=27018)


def save_doc(suburb_obj):
    connect('Suburb', alias='default')
    suburb_obj.save()


def is_stored(suburb_name):

    obj = Suburb.objects(name=suburb_name)
    now = datetime.now()

    if not obj.only_fields:
        # if query set is empty
        return False
    elif now - obj.last_updated > timedelta(hours=72.0):
        obj.delete()
        return False


def get_doc(suburb_name):

    return Suburb.objects(name=suburb_name)


# print(is_stored('Kingsford'))
# print(get_doc('Kingsford'))
