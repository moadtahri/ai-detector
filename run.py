from app import app
import os
from watson_developer_cloud import VisualRecognitionV3
from flask import Flask, render_template, request, jsonify, url_for
import json

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

visual_recognition = VisualRecognitionV3(#class of watson_developer_cloud constructor class of visual recognition take credential to estazblish connection with watson

    version ='2019-10-23',
    iam_apikey = 'ZaEE8NX0eptswf3pMcMg9Tc_xMnKP5tTHFhhMi2gVnfw'


  )

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

app.config.from_pyfile('config.py')
if __name__ == '__main__':
    app.run(debug = True)
