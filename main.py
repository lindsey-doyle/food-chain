# main.py

from flask import Flask
from flask import render_template, url_for, request

import pandas as pd

######
# copied from run.py
import sys
import json
import shutil
import time
import pickle

sys.path.insert(0, 'src') # add library code to path

from get_data import etl
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
    return render_template("home.html", data=[
                                        {'name':'Option 1'},
                                        {'name':'Option 2'}, 
                                        {'name':'Option 3'}, 
                                        {'name':'etc.'}
                                        ])


@app.route("/result", methods=['GET', 'POST'])
def result():
    #data = []
    error = None
    
    if request.method == 'POST':
        	#comment = request.form['comment']
		#data = [comment]
		#vect = cv.transform(data).toarray()
		#my_prediction = clf.predict(vect)
        my_prediction = 0
        #data = [{'name':'Option 1'}, {'name':'Option 2'}, {'name':'etc.'}]

        df = pd.read_csv('test/test_data/out/recommendations.csv')
        data2 = []
        for restaurant in list(df['Name']):
            data2.append({'Name': restaurant})

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
            
    
    return render_template('result.html', prediction = my_prediction, data=data, error=error)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def example():
    return "another example page :)"
     

if __name__ == "__main__":
    app.run(debug=True)     
