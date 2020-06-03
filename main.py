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

# create app instance
app = Flask(__name__)

@app.route("/")  # endpoint "/" (home page)
def home():
    #metapaths = [{'name': 'CAC', 'name': 'etc.'}]                    
    return render_template("home.html", data=[
                                        {'name':'Metapath Option 1'},
                                        {'name':'Option 2'}, 
                                        {'name':'Option 3'}, 
                                        {'name':'etc.'}])


@app.route("/result", methods=['GET', 'POST'])
def result():
    #data = []
    meta_dict = {'Metapath Option 1': "CAC", 'Option 2': "CAC",  'Option 3': "CAC",  'etc.': "CAC"}
    error = None
    
    if request.method == 'POST':
        listing = request.form['listing']
        city = request.form['city']

        metapath_key = request.form.get('comp_select')
        metapath = meta_dict[metapath_key]

        #print(listing)
        # TODO - confirm valid input
        listing_name = listing.strip()
        listing_city = city.strip()

        #listing_name = listing[0].strip()
        #listing_city = listing[1].strip()
        # TODO - confirm valid input

        ##!!!!!!!(api key)
        api = "ds5abV86lpgzBp767VpgjncvxHLDI64ZqZQABokWL-sRtu6II83zKSLuvhxZNEaHJ_tJ5aUFJRdlIMGnudVKQv61YUkS_vq8AuGeJOz9oPGfyvELw3rDVAVyUWdpXXYx"
        
        nxt, cat = verify_listing(listing_name, listing_city, api)
        #print(nxt) # 'nxt' is dict of info of the verified input listing 
        #print('/n', '/n', nxt)



        # Update config with inputs
        with open("config/data-params.json", "r") as fp:
            params = json.load(fp)
            #params.update(new_data)
        params["listing_name"] = listing_name 
        params["listing_city"] = listing_city
        params["listing_cat"] = cat
        params["listing_info"] = nxt
        
        with open("config/data-params.json", "w") as fp:
            json.dump(params, fp)
		
        # TODO - confirm valid config before moving on!

        # Get Data (ETL)
        #cfg = load_params(DATA_PARAMS)
        #etl(**cfg)

        ##### MODELING PIPELINE
        # Update model-params with input listing ID
        with open("config/model-params.json", "r") as fp:
            m_params = json.load(fp)
        
        m_params["listing_id"] = nxt['id']
        m_params["metapath"] = metapath
        with open("config/model-params.json", "w") as fp:
            json.dump(m_params, fp)

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
                            prediction=my_prediction, data=data, error=error)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def example():
    return "another example page :)"
     

if __name__ == "__main__":
    app.run(debug=True)     
