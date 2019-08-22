from flask import Flask, render_template, redirect
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates; or creates a new one
db.mission_to_mars.drop()

# Import the distcionary in the database

@app.route('/scrape/')
def scrape():
    #Call the scrape function from the scrape_mars.py file
    result = scrape_mars.scrape_mars()
    #Store/Write the result disctionary into MongoDB
    #db.mission_to_mars.update(result)
    db.mission_to_mars.update({}, result, upsert=True)
    return redirect('/')

# Set route
@app.route('/')
def index():
    # Store the entire mars collection in a list
    mars_list = db.mission_to_mars.find()
    print(mars_list)

    # Return the template with the mars_list passed in
    return render_template('index.html', mars_list=mars_list)


if __name__ == "__main__":
    app.run(debug=True)
