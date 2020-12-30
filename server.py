from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pickle
import numpy as np
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
__data_columns = None
__model = None

def get_loan_approval(cred_hist, dependants, educated, term, married, property_area):
    x = np.zeros(len(__data_columns))
    x[0] = 1 if cred_hist == "Yes" else 0

    if dependants == 1:
        x[1] = 1
    elif dependants == 2:
        x[2] = 1

    x[3] = 1 if educated == "Graduate" else 0

    if term == 180:
        x[4] = 1
    elif term == 480:
        x[5] = 1
    elif term != 360 or term != 300:
        x[6] = 0

    x[7] = 1 if married == "Married" else 0

    if property_area == "Rural":
        x[7] = 1
    elif property_area == "Semi-Urban":
        x[8] = 1

    return "Approved" if __model.predict([x])[0] else "Rejected"


def load_saved_artifacts():
    print("Loading saved artifacts....")
    global __data_columns
    global __model

    with open("./loan_application_columns.json", 'r') as f:
        __data_columns = json.load(f)["data_columns"]
    with open("./loan_application_model_ver24.pickle", "rb") as f:
        __model = pickle.load(f)
    print("Saved Artifacts loaded")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/application_predict', methods=['POST'])
def predict_loan_application():
    cred_hist = request.form['cred_hist']
    dependants = int(request.form['dependants'])
    educated = request.form['educated']
    term = int(request.form['term'])
    married = request.form['married']
    property_area = request.form['property_area']
    load_saved_artifacts()
    response = jsonify({
        "Apporval_Prediction": get_loan_approval(cred_hist, dependants, educated, term, married, property_area)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



if __name__ == '__main__':
    print("Starting Server for Loan Prediction...")
    app.run(debug=True)
