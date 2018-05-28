import googlemaps
from collections import defaultdict


gmaps = googlemaps.Client(key='AIzaSyDbdgCBSoXfep6LvrUsPRciIDc6ov9KceA')
# target url: https://www.google.com.au/maps/search/-33.8305779,151.1646371

def get_info(poi):
    '''

    :param poi: list of poi name.
    :return: dict {name: location(x, y)}
    '''
    geo_dic = dict()

    for i in poi:
        i = i.strip() + ', NEW SOUTH WALES, AU'
        geocode_test = gmaps.geocode(i)
        # geo_place = geocode_test[0]['geometry']['location']

        x = geocode_test[0]['geometry']['location']['lat']
        y = geocode_test[0]['geometry']['location']['lng']
        geo_dic[i] = (x,y)

    # print(len(geo_dic))
    return geo_dic

## can be used to generate a target url:
# url = f'https://www.google.com.au/maps/search/{lat},{lng}'


## TEST
# print(url)
# print(get_info(['KINGSFORD SMITH OVAL',' KINGSFORD SMITH PARK']))