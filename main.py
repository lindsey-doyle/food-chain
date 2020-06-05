# main.py

from flask import Flask
from flask import render_template, url_for, request

import pprint as pp
import pandas as pd

######
# copied from run.py
import sys
import json
import shutil
import time
import pickle

sys.path.insert(0, 'src') # add library code to path

from get_data import etl, verify_listing
from model import driver 

DATA_PARAMS = 'config/data-params.json'
MODEL_PARAMS = 'config/model-params.json'
TEST_PARAMS = 'config/test-params.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)

    return param

######

META_DICT = {
    "CAC label": "CAC", 
    "CWC label": "CWC",  
    "CDCACDC label": "CDCACDC"}

META_DICT = {
            'Serve the same cuisine as your favorite restaurant': 'A',
            'Are within a 15 minute driving distance from your favorite restaurant': 'D',
            'Serve the same specialty items as your favorite restaurant': 'W',
            'Have reviews that talk about the same food served at your favorite restaurant':'S',
            'Are as popular as your favorite restaurant': 'R',
            'Have the same overall satisfaction as your favorite restaurant': 'P'}

# create app instance
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    
    boxes = []
    for label in META_DICT.keys():
        d = {}
        d['name'] = label
        boxes.append(d) 
        
    # boxes = [{'name': "CAC label"}, {'name': "CWC label"}]
    #if request.method == 'POST': 
        #print(request.form.getlist('mycheckbox'))
        #return 'Done'

    return render_template("home.html", data=boxes)


@app.route("/result", methods=['GET', 'POST'])
def result():
    #data = []
    #meta_dict = {"CAC label": "CAC", "CWC label": "CWC",  "CDCACDC label": "CDCACDC"}
    error = None
    
    if request.method == 'POST':
        
        ##!!!!!!!(api key)
        api = "ds5abV86lpgzBp767VpgjncvxHLDI64ZqZQABokWL-sRtu6II83zKSLuvhxZNEaHJ_tJ5aUFJRdlIMGnudVKQv61YUkS_vq8AuGeJOz9oPGfyvELw3rDVAVyUWdpXXYx"
        
        # Get restaurant Name and Location
        listing = request.form['listing']
        listing_name = listing.strip()

        city = request.form['city']
        listing_city = city.strip()

        # TODO - confirm valid input
        if (len(listing_name) < 1) or (len(listing_name) < 1):
            return "No restaurant entered."

        # Get listing info and category from Yelp 
        nxt, cat = verify_listing(listing_name, listing_city, api) # 'nxt' is dict of info of the verified input listing 

        # Get Metapath Choice 
        #metapath_key = request.form.get('comp_select')
        checked = request.form.getlist('mycheckbox')
        mtrx_lst = []
        for m in checked:
            mtrx_lst.append(META_DICT[m])

        print(mtrx_lst)

        def get_metapath(lets):
            mid = "C".join(lets)
            res = 'C' + mid 
            return res + res[-2::-1]

        metapath = get_metapath(mtrx_lst)
        print(metapath)
        #metapath = "CWC" 


        # Update data-params 
        with open("config/data-params.json", "r") as fp:
            params = json.load(fp)
            #params.update(new_data)
        
        params["listing_name"] = listing_name 
        params["listing_city"] = listing_city
        params["listing_cat"] = cat
        params["listing_info"] = nxt
        
        with open("config/data-params.json", "w") as fp:
            json.dump(params, fp)

        # Update model-params 
        with open("config/model-params.json", "r") as fp:
            m_params = json.load(fp)
        
        m_params["listing_id"] = nxt['id']
        m_params["metapath"] = metapath
        with open("config/model-params.json", "w") as fp:
            json.dump(m_params, fp)
		
        # TODO - confirm valid config before moving on!

        # Get Data (ETL)
        #cfg = load_params(DATA_PARAMS)
        #etl(**cfg)
        #print('ETL Complete.')

        

        # Run model driver
        # NOTE!! - instead call 'run.py' with 'model' target!!??
        cfg = load_params(MODEL_PARAMS)
        driver(**cfg)

        # DISPLAY RECOMMENDATIONS
        df = pd.read_csv('data/out/recommendations.csv')
        #data2 = []
        #for restaurant in list(df['Name']):
            #data2.append({'Name': restaurant})

        dct = df.transpose().to_dict()
        data = []
        for val in dct.values():
            data.append(val)
    #select = request.form.get('comp_select')

    #resp = query_api(select)
    #pp(resp)
    #if resp:
        #data.append(resp)
        #if len(data) != 2:
            #error = 'Bad Response from API'
            
    my_prediction = 0
    #data = [{'name':'Option 1'}, {'name':'Option 2'}, {'name':'etc.'}]
    return render_template('result.html', 
                            prediction=my_prediction, data=data, num=len(data), error=error)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def example():
    return "another example page :)"
     

if __name__ == "__main__":
    app.run(debug=True)     
