from app import app
import os
from flask import Flask, render_template, request, jsonify, url_for, redirect
# from ibm-watson import VisualRecognitionV3

from watson_developer_cloud import VisualRecognitionV3

##### for form login/sign up
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
#####For charts
import json
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json

######Config values
app.config['SECRET_KEY'] = 'any secret string'
UPLOAD_FOLDER = '/app/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

##Instantiation of watson visual recognition service 
visual_recognition = VisualRecognitionV3(#class of watson_developer_cloud constructor class of visual recognition take credential to estazblish connection with watson

    version ='2019-10-23',
    iam_apikey = 'ZaEE8NX0eptswf3pMcMg9Tc_xMnKP5tTHFhhMi2gVnfw'


  )
##max function to use for display of the relevant class
def get_max_i(arr):
	max_i = 0
	for i in range(1,len(arr)):
		if arr[i] > arr[max_i]:
			max_i=i
	return max_i

###classifier function for xray model####
#########################################

def get_cl(path_to_img):#get classifier return table of 
  with open(path_to_img,'rb') as images_file:
    datastore = visual_recognition.classify(#function of visualgecognitionV3 
      images_file,
      threshold='0.0',
      classifier_ids='Chest_xray_998732449').get_result()
      #print(type(datastore))
  # print(datastore)
  datastore = str(json.dumps(datastore["images"])).split("classes")[1].split("image")[0]
  normal_score = datastore.split("class")[1].split("score")[1].split("}")[0].split(":")[1]
  bact_score = datastore.split("class")[2].split("score")[1].split("}")[0].split(":")[1]
  virus_score = datastore.split("class")[3].split("score")[1].split("}")[0].split(":")[1]
  scores = []
  scores.append(normal_score)
  scores.append(bact_score)
  scores.append(virus_score)
  return scores
##############Set up for Potatoes leaf model#########
#####################################################################
visual_recognition_1 = VisualRecognitionV3(#class of watson_developer_cloud constructor class of visual recognition take credential to estazblish connection with watson

    version ='2019-12-04',
    iam_apikey = 'Kat5Zy9diPqjuDDQRObZ1s7I3OzRwJ1hO6hvEXcN4s8r'


  )

def get_cl_1(path_to_img):#get classifier return table of 
  with open(path_to_img,'rb') as images_file:
    datastore = visual_recognition_1.classify(#function of visualgecognitionV3 
      images_file,
      threshold='0.0',
      classifier_ids='DefaultCustomModel_857864035').get_result()
  datastore = str(json.dumps(datastore["images"])).split("classes")[1].split("image")[0]
  normal_score = datastore.split("class")[1].split("score")[1].split("}")[0].split(":")[1]
  bact_score = datastore.split("class")[2].split("score")[1].split("}")[0].split(":")[1]
  virus_score = datastore.split("class")[3].split("score")[1].split("}")[0].split(":")[1]
  scores = []
  scores.append(normal_score)
  scores.append(bact_score)
  scores.append(virus_score)
  return scores

# ###################I.D detector model set up###########################
#########################################################################


visual_recognition3 = VisualRecognitionV3(#class of watson_developer_cloud constructor class of visual recognition take credential to estazblish connection with watson

    version ='2019-11-08',
    iam_apikey = 'FgTd8T3Nf4WCQ1jbOyllfaAyz7BcRbGS5xaZLYq7i_wX'


  )

def get_cl3(path_to_img):#get classifier return table of 
  with open(path_to_img,'rb') as images_file:
    datastore = visual_recognition3.classify(#function of visualgecognitionV3 
      images_file,
      threshold='0.0',
      classifier_ids='TelegramCIN_91674743').get_result()


  print(type(datastore))
  print(datastore)
  datastore = str(json.dumps(datastore["images"])).split("classes")[1].split("image")[0]
  cin_score = datastore.split("class")[1].split("score")[1].split("}")[0].split(":")[1]
  cinverso_score = datastore.split("class")[2].split("score")[1].split("}")[0].split(":")[1]
  permis_score = datastore.split("class")[3].split("score")[1].split("}")[0].split(":")[1]
  scores = []
  scores.append(cin_score)
  scores.append(cinverso_score)
  scores.append(permis_score)
  print(scores)
  return scores

###########################################################
###########################################################

########Different functions to use in the routes##########
##########################################################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

############# functions to serve plotly js with data############################
################################################################################

######################Function for xray model to serve plotly js data ###########

def create_plot_xray(y=[0,0,0], x=['Normal X-Ray','Bacterial Pneumonia','Viral Pneumonia']):

       
       x = np.array(x)
       y = np.array(y)
       df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe

       data = [go.Bar(x=df['x'], # assign x as the dataframe column 'x'
                        y=df['y'])]

       graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

       return graphJSON

#######Function for plant diseases detector model to serve plotly js data ####

def create_plot_plant(y=[0,0,0], x=['Early Blight','Late Blight','Healthy']):

       
       x = np.array(x)
       y = np.array(y)
       df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


       data = [go.Bar(x=df['x'], # assign x as the dataframe column 'x'
                        y=df['y'])]


       graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

       return graphJSON

######################Function for ID model to serve plotly js data ###########


def create_plot_id(y=[0,0,0], x=['CIN Front','CIN Back','Driver License']):

       
       x = np.array(x)
       y = np.array(y)
       df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


       data = [go.Bar(x=df['x'], # assign x as the dataframe column 'x'
                        y=df['y'])]


       graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

       return graphJSON

#########Alchemy package for mapping model with Sqlite db for login and sign up#########################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\project\\Test_xray\\chestxray\\app\\static\\db\\database.db'


db = SQLAlchemy(app)

class User(db.Model):

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(15), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(80))

class LoginForm(FlaskForm):

    username = StringField('username', validators=[InputRequired(), Length(min=8, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=20)])

class RegisterForm(FlaskForm):

    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=20)])
    username = StringField('username', validators=[InputRequired(), Length(min=8, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

####################################################################################
########################Different routes############################################
####################################################################################

##############index route##################

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')

#############login route###############

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>'+form.username.data + form.password.data + '</h1>'

    return render_template('login.html', form=form)

############route sign up################

@app.route('/signup', methods=['GET','POST'])
def signup():

    form = RegisterForm()

    if form.validate_on_submit():
    	        return '<h1>'+form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
        # new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
    return render_template('sign_up.html', form=form)

################xray results################

@app.route('/xrayresults', methods=['GET', 'POST'])
def Dashboardxray():
    chest_xray = request.files['cin_front']
    if chest_xray and allowed_file(chest_xray.filename):
        
          chest_xray.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, chest_xray.filename))

    
          m_xray = get_cl(os.path.join(os.getcwd()+UPLOAD_FOLDER,chest_xray.filename))

          bar = create_plot_xray(m_xray)

          return render_template('xrayresults.html',
                                   msg=m_xray[0],
                                    cin_front_img ='uploads/'+ chest_xray.filename)#add attribute you define earlier to upload.html
                              
    elif request.method == 'GET':
        return render_template('xrayresults.html')

####################xray image upload route##################

@app.route('/upload_xray', methods=['GET', 'POST'])
def load_page():
    
    if request.method == 'POST':

        if 'cin_front' not in request.files:
         
          return render_template('upload.html', msg='No file selected')
        chest_xray = request.files['cin_front']

        if chest_xray and allowed_file(chest_xray.filename):
        
          chest_xray.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, chest_xray.filename))

    
          m_xray = get_cl(os.path.join(os.getcwd()+UPLOAD_FOLDER,chest_xray.filename))
          i_max=get_max_i(m_xray)

          bar = create_plot_xray(m_xray)
          return render_template('xrayresults.html',
                                   msg=m_xray,
                                   cin_front_img ='uploads/'+ chest_xray.filename,i_max=i_max)#add attribute you define earlier to upload.html
                              
    elif request.method == 'GET':
        return render_template('upload.html')

###############plant image upload route####################


@app.route('/upload_plant', methods=['GET', 'POST'])
def load_page_1():
    if request.method == 'POST':

        if 'cin_front' not in request.files:
         
          return render_template('upload_plant.html', msg='No file selected')
        plant = request.files['cin_front']

        if plant and allowed_file(plant.filename):
        
          plant.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, plant.filename))

   
          m = get_cl_1(os.path.join(os.getcwd()+UPLOAD_FOLDER,plant.filename))
          print(m)
          bar = create_plot_plant(m)

          return render_template('plantresults.html',
                                   msg=m,
                                   cin_front_img ='uploads/'+ plant.filename, i_max=get_max_i(m))#add attribute you define earlier to upload.html
                              
    elif request.method == 'GET':
        return render_template('upload_plant.html')

##################ID image upload route#######################

@app.route('/upload_ID', methods=['GET', 'POST'])
def load_page_2():

    if request.method == 'POST':

        if 'cin_front' not in request.files:
         
          return render_template('upload_id.html', msg='No file selected')
        cin = request.files['cin_front']

        if cin and allowed_file(cin.filename):
        
          cin.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, cin.filename))

    
          m1 = get_cl3(os.path.join(os.getcwd()+UPLOAD_FOLDER,cin.filename))


          bar = create_plot_xray(m1)
          return render_template('idresults.html',
                                   msg=m1,
                                   cin_front_img ='uploads/'+ cin.filename,i_max=get_max_i(m1))#add attribute you define earlier to upload.html
                              
    elif request.method == 'GET':
        return render_template('upload_id.html')