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

def get_loan_approval(gender, married, educated, employment, income, coapplicantincome, amount, cred_hist, dependants, property_area,  term):
    x = np.zeros(len(__data_columns))
    x[0] = 0 if gender == "Female" else 1

    x[1] = 1 if married == "Married" else 0

    x[2] = 1 if educated == "Graduate" else 0

    x[3] = 1 if employment == "Yes" else 0

    x[4] = income

    x[5] = coapplicantincome

    x[6] = amount

    x[7] = 1 if cred_hist == "Yes" else 0

    if dependants == 0:
        x[8] = 1
    elif dependants == 1:
        x[9] = 1
    elif dependants == 2:
        x[10] = 1
    else:
        x[11] = 1


    if property_area == "Rural":
        x[12] = 1
    elif property_area == "Semi-Urban":
        x[13] = 1
    else:
        x[14]=1

    if term == 180:
        x[15] = 1
    elif term == 300:
        x[16] = 1
    elif term == 360:
        x[17] = 1
    elif term == 480:
        x[18] = 1
    else:
        x[19] = 1


    return "Approved" if __model.predict([x])[0] else "Rejected"


def load_saved_artifacts():
    print("Loading saved artifacts....")
    global __data_columns
    global __model

    with open("./loan_application_columns_deployment.json", 'r') as f:
        __data_columns = json.load(f)["data_columns"]
    with open("./loan_application_model_deployment.pickle", "rb") as f:
        __model = pickle.load(f)
    print("Saved Artifacts loaded")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/application_predict', methods=['POST'])
def predict_loan_application():
    gender = request.form['gender']
    married = request.form['married']
    educated = request.form['educated']
    employment = request.form['employment']
    income = int(request.form['income'])
    coapplicantincome = int(request.form['coapplicantincome'])
    amount = int(request.form['amount'])
    cred_hist = request.form['cred_hist']
    dependants = int(request.form['dependants'])
    property_area = request.form['property_area']
    term = int(request.form['term'])

    load_saved_artifacts()
    response = jsonify({
        "Apporval_Prediction": get_loan_approval(gender, married, educated, employment, income, coapplicantincome, amount, cred_hist, dependants, property_area,  term)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



if __name__ == '__main__':
    print("Starting Server for Loan Prediction...")
    app.run(debug=True)
