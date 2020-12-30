import json
import pickle
import numpy as np

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

    with open("./artifacts/loan_application_columns.json", 'r') as f:
        __data_columns = json.load(f)["data_columns"]
    with open("./artifacts/loan_application_model_ver24.pickle", "rb") as f:
        __model = pickle.load(f)
    print("Saved Artifacts loaded")


if __name__ == '__main__':
    load_saved_artifacts()
    print(get_loan_approval("Yes", 1, "Graduate", 360, "married", "Urban"))
