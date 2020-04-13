# main.py

from flask import Flask
from flask import render_template

# create app instance
app = Flask(__name__)

@app.route("/")  # endpoint "/" (home page)
def home():                    
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/example")
def example():
    return "another example page :)"

#@app.route("/<name>")              # at the end point /<name>
#def hello_name(name):              # call method hello_name
#    return "Hello "+ name           

if __name__ == "__main__":
    app.run(debug=True)     
