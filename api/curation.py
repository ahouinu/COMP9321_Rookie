import pandas as pd
from collections import defaultdict
import ssl
import nltk

ssl._create_default_https_context = ssl._create_unverified_context


def get_lga():
    lga_dic = defaultdict(str)
    if len(lga_dic) == 0:
        lga = "https://docs.google.com/spreadsheets/d/1RPJFmOFusUSS-Fu2nWids_SiH3CkAbKsml7IhgG-3Js/export?format=csv"
        df = pd.read_csv(lga)
        # df = _df[_df['Suburb/Town']]

        for i in range(df.shape[0]):
            data = df.iloc[i]
            suburb = data["Suburb/Town"].replace(u'\xa0', u' ').lstrip().capitalize()
            # print(suburb)
            council = data["Council Name"]
            council_check = council.split(' ')
            if council_check [-2] == 'City':
                lga_dic[suburb] = ' '.join(council_check[:-2])
    return lga_dic
    # print('test')
    # print(lga_dic)


def build_suburb_list():
    lga_dic = get_lga()
    ll = sorted((lga_dic.keys()))
    # print(ll)
    return ll


def typo_check(token):
    '''
    :param token
    :return: the correction of potential typo: string
    '''
    err = 100
    correction = ''
    sub_list = build_suburb_list()

    # token = input("input suburb with error!\n")

    for i in sub_list:
        if err > nltk.edit_distance(token, i):
            err = nltk.edit_distance(token, i)
            correction = i

    # print(f'Do you mean {correction}?')
    return correction


# get_lga()
# print(build_suburb_list())
# typo_check()
