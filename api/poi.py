'''URL Model
http://maps.six.nsw.gov.au/arcgis/rest/services/public/NSW_POI/MapServer/find?searchText=opera
&contains=true&searchFields=&sr=&layers=0&layerDefs=&returnGeometry=true&maxAllowableOffset=
&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=html
'''

import requests

import math

from bs4 import BeautifulSoup
from collections import Counter
# check the url
def check_link(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print(r.text)
        return r.text
    except:
        print('can not reach the URL')


# def get_content2(item_list, url):
#     soup = BeautifulSoup(open(url))
#     item = {}
#
#     flag = 'key'
#
#     for ul in soup.ul:
#         print(ul, '+++++++++++')
#
#     item_list.append(item)


#get the resource
def get_content(item_list, src):
    flag = 'key'
    soup = BeautifulSoup(src, 'html.parser')
    collection = soup.find_all('ul')

    if not collection:
        return('There is no results!')

    for ul in collection:
        item = {}
        countline = 0
        for br in ul:
            if countline == 0:
                countline += 1
                continue
            if countline == 1 and br:
                for i in br:
                    key = i
                    # print(key)
                    countline += 1
                continue
            if countline == 2:
                item[key] = br
                countline += 1
                continue
            if countline == 3:
                countline = 0
                continue
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


    url = "http://maps.six.nsw.gov.au/arcgis/rest/services/public/NSW_POI/MapServer/find?searchText="+ condition_list[0] + "&contains=true&searchFields=&sr=&layers=0&layerDefs=&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=html"

    # print(url)
    point_list = []
    inter_check_list = []
    
    resource = check_link(url)

    get_content(point_list, resource)
    # get_content2(point_list, resource)
    if len(condition_list) == 1:
        # print(point_list)
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

def rank_initial(dic):
    dic["Community"] = 0
    dic["Education"] = 0
    dic["Recreation"] = 0
    dic["Transport"] = 0
    return dic

def rank_count(result, Surburb_value):
    # rank 1(count: 0 - 3)
    # rank 2(count: 3 - 6)
    # rank 3(count: 6 - 9)
    # rank 4(count: 9 - 12)
    # rank 5(count: 12 or more)
    for item in result:
        if item["poigroup: "] == " Community":
            Surburb_value["Community"] += 1
        if item["poigroup: "] == " Education":
            Surburb_value["Education"] += 1
        if item["poigroup: "] == " Recreation":
            Surburb_value["Recreation"] += 1
        if item["poigroup: "] == " Transport":
            Surburb_value["Transport"] += 1

def rank(result):
    dict = {}
    Surburb_value = rank_initial(dict)
    rank_count(result, Surburb_value)
    for _ in Surburb_value.keys():
        Surburb_value[_] = math.ceil(Surburb_value[_]/3)
        if Surburb_value[_] > 5:
            Surburb_value[_] = 5
        if Surburb_value[_] == 0:
            Surburb_value[_] = 1
    return Surburb_value

def get_info(input):
    # return a list contains several dictionaries which fit the requirement

    # run(input)
    return run(input), rank(run(input))

