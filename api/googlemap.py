import googlemaps

gmaps = googlemaps.Client(key='AIzaSyDbdgCBSoXfep6LvrUsPRciIDc6ov9KceA')
# target url: https://www.google.com.au/maps/search/-33.8305779,151.1646371

def get_info(poi):
    '''

    :param poi: string of poi name
    :return: x and y geo_coordinate
    '''

    geocode_test = gmaps.geocode(poi)
    # geo_place = geocode_test[0]['geometry']['location']

    x = geocode_test[0]['geometry']['location']['lat']
    y = geocode_test[0]['geometry']['location']['lng']

    geo_dic = {'x':x,'y':y}

    return geo_dic

## can be used to generate a target url:
# url = f'https://www.google.com.au/maps/search/{lat},{lng}'


## TEST
# print(url)
# print(get_info('KINGSFORD SMITH OVAL'))