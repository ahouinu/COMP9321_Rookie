'''URL Model
http://maps.six.nsw.gov.au/arcgis/rest/services/public/NSW_POI/MapServer/find?searchText=opera
&contains=true&searchFields=&sr=&layers=0&layerDefs=&returnGeometry=true&maxAllowableOffset=
&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=html
'''

import requests
from bs4 import BeautifulSoup
from collections import Counter
# check the url
def check_link(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.txt
    except:
        print('can not reach the URL')

#get the resource
def get_content(item_list, src):
    flag = 'key'
    soup = BeautifulSoup(src, 'lxml')
    collection = soup.find_all('ul')

    if not collection:
        return('There is no results!')

    for ul in collection:
        item = {}
        for br in ul:
            '''every br element has two i element'''
            for i in br:
                if flag == 'key':
                    key = i.string
                    flag = 'value'
                elif flag == 'value':
                    value = i.string
                    item[key] = value
                    flag = 'key'
        item_list.append(item)

def inter_check(data):
    '''The format of data looks like
    [[{  }, {  }, {  }...], [{  }, {  }, {  }...], ... ]
    '''
    list = []
    for divide_result in data:
        for dic in divide_result:
            list.append(dic['RID:'])
    i = Counter(list)

    rid_list = []
    '''The format of j is (Rid, freqeuncy appear), 
    if the frequency of the Rid equals the number of the resutls, then record Rid'''
    for j in i.most_common():
        if j[1] == data.length():
            rid_list.append(j[0])
    if rid_list == []:
        return ('No such results!')
    else:
        return rid_list

'''
main functoin
The input of the user should be split by space

'''
def run(user_input):
    condition_list = user_input.split(' ')
    point_list = []
    inter_check_list = []
    url = ''
    resource = check_link(url)

    get_content(point_list, resource)

    if len(condition_list) == 1:
        return point_list
    elif len(condition_list) > 1:
        data_combine = []
        for i in range(len(condition_list)):
            data_combine.append(run(condition_list[i]))

        rid_list = inter_check(data_combine)
        '''
        data is dic
        '''
        for data in data_combine[0]:
            if data['Rid'] in rid_list:
                inter_check_list.append(data)
        return inter_check_list
