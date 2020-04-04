# main.py

from flask import Flask
from flask import render_template

# create an app instance
app = Flask(__name__)

@app.route("/")  # at the endpoint "/" (aka home page)
# call method home() 
def home():                    
    return render_template("home.html") # which renders "home.html" from "templates" folder 

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def example():
    return "another example page :)"

#@app.route("/<name>")              # at the end point /<name>
#def hello_name(name):              # call method hello_name
#    return "Hello "+ name          # which returns "hello + name  

if __name__ == "__main__":     # on running $ python app.py (bc __name__ means this current file, in this case main.py)
    app.run(debug=True)        # run the flask app (note- debug=True makes it preprod environment)
