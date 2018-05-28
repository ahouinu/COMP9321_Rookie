from mongoengine import connect
from app.models import Suburb
from datetime import datetime, timedelta

host = 'mongodb://ass3:ass3@ds157641.mlab.com:57641/comp9321_ass3'
# connect(db='comp9321_ass3', username='ass3', password='ass3', host=host)


def save_doc(suburb_obj):
    connect('suburb', host=host)
    # connect(db='comp9321_ass3', username='ass3', password='ass3', host=host)
    suburb_obj.save()


def is_stored(suburb_name):

    # connect(db='comp9321_ass3', username='ass3', password='ass3', host=host)
    connect('suburb', host=host)

    obj = Suburb.objects(name=suburb_name)
    now = datetime.now()

    if not obj.only_fields:
        # if query set is empty
        return False
    elif now - obj.last_updated > timedelta(hours=72.0):
        obj.delete()
        return False


def get_doc(suburb_name):

    # connect(db='comp9321_ass3', username='ass3', password='ass3', host=host, port=27018)
    connect('suburb')

    return Suburb.objects(name=suburb_name)


# if __name__ == '__main__':
#     # connect('suburb')
#     connect(db='comp9321_ass3', username='ass3', password='ass3', host=host)

# print(is_stored('Kingsford'))
# print(get_doc('Kingsford'))
# from app.models import Suburb
# suburb = Suburb('test', {'crime': 'test'}, ['acc_test'], (['poi_0'], {'poi_1': 'test'}), 'wiki_test')
# suburb.set_lga('testLga')
# suburb.set_rates(1,2,3,4)
# connect('suburb')
# suburb.save()
