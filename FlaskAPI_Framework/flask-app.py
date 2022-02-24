#!/usr/bin/env python

# Flask is looking for certain "folders" that it holds certain data in. 
# Like a static folder for flat data files (like the gdp or nobel file)
# Also flask is looking for template folder which contains HTML files. 

# We are doing 2 things here. We are creating a flask app that is going 
# to have a basic website to show our data. And we are going to render it 
# in the HTML file.

# Building flask app to display our nobel file into index.html 
#  HOW TO BUILD A REST API THAT DOES BASIC CRUD FUNCTIONS

#pip install flask and specify what modules you need from library to make application smaller so it can go faster! 

# Flask = lets you create instance of app
# Json = cuz we will format it in json 
# render_template = cuz we are going to be rendering our data into 
#                   our template called HTML
# request = cuz we are going to accept data in the form of a request


from flask import Flask, json, render_template, request, send_file

# this allows flask to work with the folder structure
import os

#create instance of Flask app
# __name__ specifies what file this is, 
# name or file being called from another file
app = Flask(__name__)

@app.route("/")
def hello():
    #The is the information seen when user uses API on the home route
    #How to access the different endpoints below when you go to the homepage!
    text = f"go to /all to see all prizes <br> \
              and /year/(year) (with a specific year specified where the parenthesis are) to see prizes for that year <br> \
              and /add to add additional information"
    return text

# THE FOLLOWING IS HOW All OF THE NOBEL.JSON DATA FILE IS SHOWN IN LOCALHOST AND THE CLOUD(THRU AZURE)

# Decorator for a route: this is for the 'nobel' route.
# Flask is calling a function called route which lets us run the code we put underneath when we go to the: 
# forward slash route all: "/all"
@app.route("/all")

# create function called 'nobel'
def nobel():

    # This is how we are telling the flask app to go from where it is to
    # the nobel.json file: it is taking in the static folder by being 
    # referenced as 'app.static_folder' followed by the actual name of file 
    # (there is no path between those 2 things which is why we have "") 
    json_url = os.path.join(app.static_folder,"","nobel.json")
    
    # Now we can open this file and load it to a json format
    data_json = json.load(open(json_url))

    # Now we will use the render template: render will take any HTML file 
    # that we pass into it and render data_json into it (Look at data in HTML 
    # to see how the this py file and HTML file are connected)
    return render_template('index.html',html_page_text=data_json)

@app.route("/add")
def form():
    form_url = os.path.join("templates","form.html")
    # the send_file function lets us send the contents in the form to a client
    return send_file(form_url)

#Now, we will create a decorator to get the data based on year!
@app.route("/year/<year>",methods=['GET'])
def add_year1(year):
    json_url = os.path.join(app.static_folder,"","nobel.json")
    #The below line makes sure we can access the data inside the prizes key in the json file.
    data_json = json.load(open(json_url))
    #The below line gets the data passed into the route and converts it to a variable.
    data = data_json["prizes"]
    #Iterate through all the data in that list above to get the data for the year of interest 
    if request.method == 'GET':
        data_json = json.load(open(json_url))
        data = data_json["prizes"]
        year = request.view_args['year']
        output_data = [x for x in data if x['year']==year]

        return render_template('events.html',html_page_text=output_data)
#route is getting data (use GET) \ write some logic to get the POSTed data from the form
@app.route("/year/<year>",methods=['GET','POST'])
def add_year(year):
    json_url = os.path.join(app.static_folder,"","nobel.json")
    if request.method == 'GET':
        data_json = json.load(open(json_url))
        data = data_json['prizes']
        year = request.view_args['year']
        output_data = [x for x in data if x['year']==year]
        
        #render template is always looking in tempate folder
        return render_template('events.html',html_page_text=output_data)
    
    elif request.method == 'POST':

        #Lines 95 through 97 pull the data out of the form that’s posted. 
        #The code is referencing those elements by the names specified in the form.html attributes. 
        year = request.form['year']
        category = request.form['category']
        laureates = request.form['laureates']

        #Lines 101 through 104 put that data into a dictionary
        prize_yr= { "year":year,
                    "category":category,
                    "laureates":laureates,
                    }

        with open(json_url,"r+") as file:
            data_json = json.load(file)
            data_json["prizes"].append(prize_yr)
            json.dump(data_json, file)
        
        #Adding text
        text_success = "Data successfully added: " + str(prize_yr)
        return render_template('index.html', html_page_text=text_success)   
        
# this is checking: "if this is the main file that we are calling 
# (which it is) we want to do stuff otherwise we dont want to run it"
if __name__ == "__main__":
    app.run(debug=True)

# Now, we can run this by going to terminal and cd-ing into flaskAPI_framework. 
# And run the flask command: 

    # we are exporting our flask app to what we called our flask app: 'flask-app'
#      export FLASK_APP=flask-app
    # then we connect to our localhost thru 'flask run'
#      flask run  

# NOTES TO SELF: print(data) #--> if you want to see it in terminal for troubleshoot purposes!