from flask import Flask, request, jsonify
from . import predict

app = Flask(__name__)


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
    predict.load_saved_artifacts()
    response = jsonify({
        "Apporval_Prediction": predict.get_loan_approval(cred_hist, dependants, educated, term, married, property_area)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':
    print("Starting Server for Loan Prediction...")
    app.run(debug=True)
