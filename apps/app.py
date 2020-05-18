# imports flask dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping
import challenge

app = Flask(__name__)

# Setting up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# finds created mars collection and returns html template using index.html file
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars = mars)

# defines flask route, accesses database, scrapes data and stores it
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = challenge.scrape_all()
   mars.update({}, mars_data, upsert = True)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run()