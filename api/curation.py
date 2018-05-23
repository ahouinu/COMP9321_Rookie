import pandas as pd
from collections import defaultdict
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

lga_dic = defaultdict(str)

def get_lga():
    print(lga_dic)
    if len(lga_dic) == 0:
        lga = "https://docs.google.com/spreadsheets/d/1RPJFmOFusUSS-Fu2nWids_SiH3CkAbKsml7IhgG-3Js/export?format=csv"
        df = pd.read_csv(lga)
        # df = _df[_df['Suburb/Town']]

        for i in range(df.shape[0]):
            data = df.iloc[i]
            suburb = data["Suburb/Town"]
            # print(suburb)
            council = data["Council Name"]
            council_check = council.split(' ')
            if council_check [-2] == 'City':
                lga_dic[suburb] = ' '.join(council_check[:-2])

    # print('Hello')
    # print('test')
    # print(lga_dic)

        # df = _df[_df['Suburb/Town'] == 'New South Wales']

    # for i in range(df.shape[0]):
    #     data = df.iloc[i]
    #     city = data["LGA region"]
    #     postcode = data["Postcode"]
        # print("HEY LISTEN!",type(postcode))
        # if city not in placelist:
        #     continue
        # if city in city_dict[postcode]:
        #     continue
        # else:
        #     city_dict[postcode].append(city)


get_lga()

