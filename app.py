# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
# import scrape_mars_weather
import os


# Hidden authetication file
#import config 

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection through mLab
# app.config["MONGO_URI"] = os.environ.get('authentication')
# mongo = PyMongo(app)



# Use flask_pymongo to set up mongo connection locally 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    marsData = mongo.db.marsData.find_one()

    # Return template and data
    return render_template("index.html", marsData=marsData)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    marsData = mongo.db.marsData
    appMarsData = scrape_mars.marsNewsScrape()
    appMarsData = scrape_mars.marsImagesScrape()
    appMarsData = scrape_mars.marsWeatherScrape()
    appMarsData = scrape_mars.marsFacts()
    appMarsData = scrape_mars.marsHemiScrape()
    marsData.update({}, appMarsData, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)