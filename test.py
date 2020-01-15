import os
from watson_developer_cloud import VisualRecognitionV3
import json
visual_recognition = VisualRecognitionV3(

    version ='2019-10-23',
    iam_apikey = 'ZaEE8NX0eptswf3pMcMg9Tc_xMnKP5tTHFhhMi2gVnfw'


  )

with open(r'C:\Users\virus\Desktop\Testing\test_xray\person1_virus_6.jpeg','rb') as images_file:
  classes = visual_recognition.classify(
    images_file,
    threshold='0.1',
    classifier_ids='Chest_xray_998732449').get_result()
print(json.dumps(classes, indent=2))