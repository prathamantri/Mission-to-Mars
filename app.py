from flask import Flask, render_template, redirect
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set route
@app.route('/')
def index():
    mars_list = mongo.db.mars_db.find_one()
    return render_template("index.html", mars_list=mars_list)

# Import the distcionary in the database

@app.route('/scrape/')
def scrape():
    mission_to_mars = mongo.db.mars_db
    #Call the scrape function from the scrape_mars.py file
    result = scrape_mars.scrape_mars()
    #Store/Write the result disctionary into MongoDB
    #db.mission_to_mars.update(result)
    mission_to_mars.update({}, result, upsert=True)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
