from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pickle
import numpy as np
import logging
import sys

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

__data_columns = None
__model = None

__data_columns_emp = None
__model_emp = None
__scalar_emp = None

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


def get_employee_prediction(satisfaction_level, last_evaluation, number_project, average_monthly_hours,
                            time_spend_company, work_accident, promotion_last_5years, salary, dept):
    x = np.zeros(len(__data_columns_emp))
    if 0 <= satisfaction_level <= 1:
        x[0] = satisfaction_level
    else:
        return "Invalid value for satisfaction level"

    if 0 <= last_evaluation <= 1:
        x[1] = last_evaluation
    else:
        return "Invalid value for last_evaluation"

    if isinstance(number_project, int):
        x[2] = number_project
    else:
        return "Invalid value for number_project"

    if isinstance(average_monthly_hours, int):
        x[3] = average_monthly_hours
    else:
        return "Invalid value for average_monthly_hours"

    if isinstance(time_spend_company, int):
        x[4] = time_spend_company
    else:
        return "Invalid value for time_spend_company"

    if work_accident.lower() == "yes":
        x[5] = 1
    elif work_accident.lower() == "no":
        x[5] = 0
    else:
        return "Invalid value for work accident"

    if promotion_last_5years.lower() == "yes":
        x[6] = 1
    elif promotion_last_5years.lower() == "no":
        x[6] = 0
    else:
        return "Invalid value for promotion_last_5years"

    if salary.lower() == "high":
        x[7] = 2
    elif salary.lower() == "med":
        x[7] = 1
    elif salary.lower() == "low":
        x[7] = 0
    else:
        return "Invalid value for salary"

    dept_list = ["it", "randd", "accounting", "hr", "management", "marketing", "product_mng", "sales", "support",
                 "technical"]
    if dept.lower() in dept_list:
        x[8 + dept_list.index(dept.lower())] = 1
    else:
        return "Invalid value for departments"

    x = __scalar_emp.transform([x])
    return " is likely leave" if __model_emp.predict(x)[0] else " is likely stay"



def load_saved_artifacts():
    print("Loading saved artifacts....")
    global __data_columns
    global __model

    with open("./loan_application_columns_deployment.json", 'r') as f:
        __data_columns = json.load(f)["data_columns"]
    with open("./loan_application_model_deployment.pickle", "rb") as f:
        __model = pickle.load(f)

    print("Saved Artifacts loaded")


def load_saved_artifacts_emp():
    print("Loading saved artifacts....")

    global __data_columns_emp
    global __model_emp
    global __scalar_emp

    with open("./Employee_attrition_columns_copy.json", 'r') as f:
        __data_columns_emp = json.load(f)["data_columns"]
    with open("./Employee_attrition_scaler.pickle", "rb") as f:
        __scalar_emp= pickle.load(f)
    with open("./Employee_attrition_model.pickle", "rb") as f:
        __model_emp = pickle.load(f)

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


@app.route('/employee_predict', methods=['POST'])
def predict_employee_attrition():
    satisfaction_level = float(request.form['satisfaction_level'])
    last_evaluation = float(request.form['last_evaluation'])
    number_project = int(request.form['number_project'])
    average_monthly_hours = int(request.form['average_monthly_hours'])
    time_spend_company = int(request.form['time_spend_company'])
    work_accident = request.form['work_accident']
    promotion_last_5years = request.form['promotion_last_5years']
    salary = request.form['salary']
    dept = request.form['dept']

    load_saved_artifacts_emp()
    response = jsonify({
        "Apporval_Prediction": get_employee_prediction(satisfaction_level, last_evaluation, number_project, average_monthly_hours, time_spend_company, work_accident, promotion_last_5years, salary, dept)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



if __name__ == '__main__':
    print("Starting Server for Loan Prediction...")
    app.run(debug=True)
