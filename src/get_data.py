import requests
import pandas as pd
import numpy as np
import time
import pprint as pp
from tqdm import tqdm
import time
import psutil
import sys

#Collect zip codes and categories
zip_codes = [line.rstrip('\n') for line in open('zips copy.txt')]
categories = [line.rstrip('\n') for line in open('categories.txt')]

#Define the API Key, Endpoint, and Header
API1=#APIKey1
API2=#APIKey2
API3=#APIKey3
API4=#APIKey4
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API1}

#Create a copy of zip_codes
zip_codes_remaining = zip_codes.copy()

#Initialize lists for collecting data
name = []
url = []
phone = []
address = []
city = []
state = []
czip = []
rating = []
review_count = []
vertical = []
search = []
yelp_id = []

#Ask user for page number to collect from
print('Page Number:')
page_number = int(input())
page_number = (page_number-1)*50

#Ask user for number of zip codes // There are 1647 available ZIPs rn
print('How many zip codes:')
num_zips = int(input())

#Create getter for yelp API
#TQDM for measuring progress
#putil for measuring bandwidth usage
count = 0
for zips in tqdm(np.random.choice(zip_codes_remaining,num_zips)):
    try:
        zip_codes_remaining.remove(zips)
    except:
        print(zips)
    for cat in categories:
        if cat in ['Contractors','Landscapers','Plumbers','Movers']:
            count+=1
            try:
                PARAMETERS = {'location':str(zips), 
                          'term': cat,
                          'limit': 50,
                          'offset':page_number-50}
                if 5000<=count<=9999:
                    HEADERS = {'Authorization': 'bearer %s' % API2}
                if 10000<=count<=14999:
                    HEADERS = {'Authorization': 'bearer %s' % API3}
                if 15000<=count<=19999:
                    HEADERS = {'Authorization': 'bearer %s' % API4}
                if 20000<=count<=24999:
                    HEADERS = {'Authorization': 'bearer %s' % API1}
                if 25000<=count:
                    print('Used up all API requests available')
                    pass
                response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)
                if response.status_code!=200:
                    print('Error: response status code not 200')
                    time.sleep(5)
                    sys.exit(0)
                business_data = response.json()
                for business in business_data['businesses']:
                    name = name + [business['name']]
                    url = url + [business['url']]
                    address = address + [business['location']['address1']]
                    city = city + [business['location']['city']]
                    state = state + [business['location']['state']]
                    czip = czip + [business['location']['zip_code']]
                    phone = phone + [business['phone']]
                    search = search + [cat]
                    yelp_id = yelp_id + [business['id']]
                    industries = str()
                    for i in business['categories']:
                        industries = industries+', '+str(i['title'])
                    vertical = vertical + [industries[2:]]
                    rating = rating + [business['rating']]
                    review_count = review_count + [business['review_count']]
            except:
	            pass
        count+=1
        try:
            PARAMETERS = {'location':str(zips), 
                          'term': cat,
                          'limit': 50,
                          'offset':page_number}
            if 5000<=count<=9999:
                HEADERS = {'Authorization': 'bearer %s' % API2}
            if 10000<=count<=14999:
                HEADERS = {'Authorization': 'bearer %s' % API3}
            if 15000<=count<=19999:
                HEADERS = {'Authorization': 'bearer %s' % API4}
            if 20000<=count<=24999:
                HEADERS = {'Authorization': 'bearer %s' % API1}
            if 25000<=count:
                print('Used up all API requests available')
                pass
            response = requests.get(url = ENDPOINT, params = PARAMETERS, headers = HEADERS)
            if response.status_code!=200:
                print('Error: response status code not 200')
                time.sleep(5)
                sys.exit(0)
            business_data = response.json()
            for business in business_data['businesses']:
                name = name + [business['name']]
                url = url + [business['url']]
                address = address + [business['location']['address1']]
                city = city + [business['location']['city']]
                state = state + [business['location']['state']]
                czip = czip + [business['location']['zip_code']]
                phone = phone + [business['phone']]
                search = search + [cat]
                yelp_id = yelp_id + [business['id']]
                industries = str()
                for i in business['categories']:
                    industries = industries+', '+str(i['title'])
                vertical = vertical + [industries[2:]]
                rating = rating + [business['rating']]
                review_count = review_count + [business['review_count']]
        except:
            pass


#Create dataframe to aggregate all of the data collected
result = pd.DataFrame({
    'Name':name,
    'URL':url,
    'Phone':phone,
    'Address':address,
    'City':city,
    'State':state,
    'ZIP':czip,
    'Vertical':vertical,
    'Rating':rating,
    'Review Count':review_count,
    'Search':search,
    'YelpID':yelp_id
})
print('Original length of collected data: '+str(len(result))+' leads.')

#Reformat phone numbers
result['Phone'] = result['Phone'].apply(lambda x: x[2:])

#Drop duplicates
result = result.drop_duplicates(subset=['Name'], keep='first')

sys.exit(0)