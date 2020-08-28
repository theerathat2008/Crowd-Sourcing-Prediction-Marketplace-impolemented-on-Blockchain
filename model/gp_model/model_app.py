import numpy as np
from flask import Flask, request

from gp_algorithm import GPModel

model = None
app = Flask(__name__)
T_pred = None
E_actual = None

def load_model():
    global model
    model = GPModel()

@app.route('/')
def home_endpoint():
    return 'Model initialised'

@app.route('/train', methods=['POST'])
def train_model():
    if request.method == 'POST':
        ds, id, pred = None, None, None
        data = request.get_json()
        if "dataset_size" in data:
            ds = int(data["dataset_size"])
        elif "individual_data" in data:
            id = [int(i) for i in data["individual_data"]]
            pred = len(id)
        x, y= model.train(dataset_size=ds, data=id, pred_size=pred)
        global T_pred
        T_pred = x
        global E_actual
        E_actual = y
        return "Model trained\n"

@app.route('/predict', methods=['POST'])
def get_prediction():
    n = None
    if request.method == "POST":
        data = request.get_json()
        if "prediction_size" in data:
            n = int(data["prediction_size"])
    predictions, std_dev = model.predict(T_pred)
    res = []
    for p in range(n if n else len(predictions)):
        res.append(str(predictions[p]))
                                                                                                                                                                   1,13          Top
