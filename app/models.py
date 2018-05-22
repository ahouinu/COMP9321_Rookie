class Suburb:

    _instances = {}

    def __init__(self, name, crime_stats, acc_stats, poi, wikigit):
        # Test
        self.name = name
        self.crime_stats = crime_stats
        self.acc_stats = acc_stats
        self.poi = poi
        self.wiki = wiki
        self._instances[name] = self

    @classmethod
    def get_instance(cls, suburb_name):
        try:
            return cls._instances[suburb_name]
        except KeyError:
            return {}
