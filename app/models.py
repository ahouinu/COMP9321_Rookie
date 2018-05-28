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
        self.wiki = wiki[0]
        self.images = wiki[1]
        self._instances[name] = self
        self.rates = {}
        self.lga = None
        self.is_lga = False
        self.last_updated = datetime.now()
        self.acc_path = None
        self.poi_path = None
        self.rates_value = {}
        self.poi_locations = []
        self.poi_urls = []
        self.nb_of_pois = 0

    @classmethod
    def get_instance(cls, suburb_name):
        try:
            return cls._instances[suburb_name]
        except KeyError:
            return {}

    @classmethod
    def imported(cls, suburb_name):
        return suburb_name in cls._instances.keys()

    def set_rates(self, crime_rate, acc_rate, poi_rate, all_rate):
        self.rates = {'all': all_rate,
                      'crime': crime_rate,
                      'acc': acc_rate,
                      'poi': poi_rate}
        for key, value in self.rates.items():
            self.rates_value[key] = f'{float(value) / 20.0 : .1f}'

    def set_lga(self, lga):
        self.lga = lga
        self.is_lga = \
            self.lga == self.name

    def set_figure_paths(self, acc_path, poi_path):
        self.acc_path = acc_path
        self.poi_path = poi_path

    def set_poi_locations(self, poi_locations):
        self.poi_locations = poi_locations
        for poi in poi_locations:
            tmp = ','.join([str(poi['lat']), str(poi['lng'])])
            self.poi_urls.append(tmp)
        self.nb_of_pois = len(poi_locations)
