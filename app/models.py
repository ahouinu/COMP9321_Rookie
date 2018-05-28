from mongoengine import StringField, IntField, Document, ListField, DictField, DateTimeField
from datetime import datetime


class Suburb():

    _instances = {}

    # id = IntField(required=True, primary_key=True)
    # name = StringField(required=True, max_length=50)
    # lga = StringField(required=True, max_length=50)
    # crime_stats = DictField(required=True)
    # acc_stats = ListField(required=True)
    # poi = ListField(required=True)
    # poi_rate = DictField(required=True)
    # wiki = StringField(required=True)
    # rates = DictField(required=True)
    # last_updated = DateTimeField(required=True)

    def __init__(self, name, crime_stats, acc_stats, poi, wiki, *args, **kwargs):
        # Test
        super().__init__(*args, **kwargs)
        # self.id = len(self._instances)
        self.name = name
        self.crime_stats = crime_stats
        self.acc_stats = acc_stats
        self.poi = poi[0]
        self.poi_rate = poi[1]
        self.wiki = wiki
        self._instances[name] = self
        self.rates = {}
        self.lga = None
        self.is_lga = False
        self.last_updated = datetime.now()

    @classmethod
    def get_instance(cls, suburb_name):
        try:
            return cls._instances[suburb_name]
        except KeyError:
            return {}

    def set_rates(self, crime_rate, acc_rate, poi_rate, all_rate):
        self.rates = {'all': all_rate,
                      'crime': crime_rate,
                      'acc': acc_rate,
                      'poi': poi_rate}

    def set_lga(self, lga):
        self.lga = lga
        self.is_lga = \
            self.lga == self.name
