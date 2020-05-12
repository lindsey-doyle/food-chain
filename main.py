# main.py

from flask import Flask
from flask import render_template

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
    data = []
    error = None
    
    #select = request.form.get('comp_select')

    #resp = query_api(select)
    #pp(resp)
    #if resp:
        #data.append(resp)
        #if len(data) != 2:
            #error = 'Bad Response from API'
    
    return render_template('result.html', data=data, error=error)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def example():
    return "another example page :)"
     

if __name__ == "__main__":
    app.run(debug=True)     
