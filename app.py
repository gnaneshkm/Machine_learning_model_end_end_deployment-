from flask import Flask,render_template, request, jsonify
import numpy as np
import traceback
import pickle
import pandas as pd
import utils
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import configparser
from sklearn import ensemble

# Read env variables
config = configparser.ConfigParser()
config.read('config.ini')

# App definition
app = Flask(__name__, template_folder='templates')

# Connect to DB
client = MongoClient(config.get('config','DB_URI'))
db = client.flask_mongodb_atlas
collection = db.prediction

# Importing models
with open('./trained-models/model.pkl', 'rb') as f:
    classifier = pickle.load(f)

with open('./trained-models/model_columns.pkl', 'rb') as f:
    model_columns = pickle.load(f)

def get_data(id):
    id_result=collection.find_one({'_id':ObjectId(id)})
    return id_result

def store_data(data):
    data["predictionTime"] = datetime.now()
    collection.insert_one(data)


@app.route('/', methods=['POST', 'GET'])
def fetchAll():
    if request.method == 'GET':
        #fetch all data from DB
        rows = []
        for doc in collection.find({}):
            rows.append((doc))
        print(rows)
        return  render_template('index.html', rows=rows)

    if request.method == 'POST':
        try:
            json_ = request.json
            print('user data: ',json_)
            query_ = pd.get_dummies(pd.DataFrame(json_,index=[0]))
            query = query_.reindex(columns=model_columns, fill_value=0)

            #query_null=utils.drop_null(query)
            #if query_null.shape[0]>1:
                #query_null=utils.duplicated_remove(query_null)
            #query_normalize=utils.Normalize(query_null)

            prediction = list(classifier.predict(query))

            if prediction[0]==0:
                prediction='STAR'
            elif prediction[0]==1:
                prediction='GALAXY'
            else:
                prediction ='QSO'

            #store result to sqlite db
            json_["prediction"]=str(prediction)
            store_data(json_)
            return jsonify({
                "prediction": str(prediction)
            })

        except:
            return jsonify({
                "trace": traceback.format_exc()
            })

@app.route('/predict')
def v_timestamp():
    return render_template('predict.html')


if __name__ == "__main__":
    app.run()
