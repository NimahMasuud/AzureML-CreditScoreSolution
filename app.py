from flask import Flask, request, render_template
import json
import urllib.request
import ssl
import os

app = Flask(__name__)

# Function to bypass self-signed certificate verification
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

# Azure endpoint and API key
url = ''
api_key = ''

def make_prediction(data):
    body = json.dumps(data).encode('utf-8')
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return json.loads(result.decode("utf-8"))  # Load JSON response
    except urllib.error.HTTPError as error:
        return f"Error: {error.code} - {error.read().decode('utf-8')}"

@app.route('/')
def index():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    # Collecting input data from the form
    id_ = request.form['ID']
    limit_bal = request.form['LIMIT_BAL']
    sex = request.form['SEX']
    education = request.form['EDUCATION']
    marriage = request.form['MARRIAGE']
    age = request.form['AGE']
    pay_1 = request.form['PAY_1']
    pay_2 = request.form['PAY_2']
    pay_3 = request.form['PAY_3']
    pay_4 = request.form['PAY_4']
    pay_5 = request.form['PAY_5']
    pay_6 = request.form['PAY_6']
    bill_amt1 = request.form['BILL_AMT1']
    bill_amt2 = request.form['BILL_AMT2']
    bill_amt3 = request.form['BILL_AMT3']
    bill_amt4 = request.form['BILL_AMT4']
    bill_amt5 = request.form['BILL_AMT5']
    bill_amt6 = request.form['BILL_AMT6']
    pay_amt1 = request.form['PAY_AMT1']
    pay_amt2 = request.form['PAY_AMT2']
    pay_amt3 = request.form['PAY_AMT3']
    pay_amt4 = request.form['PAY_AMT4']
    pay_amt5 = request.form['PAY_AMT5']
    pay_amt6 = request.form['PAY_AMT6']

    # Constructing the input data as required by the model
    data = {
        "input_data": {
            "columns": [
                "ID", "LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE",
                "PAY_1", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
                "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4",
                "BILL_AMT5", "BILL_AMT6", "PAY_AMT1", "PAY_AMT2",
                "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"
            ],
            "data": [[
                int(id_), float(limit_bal), int(sex), int(education),
                int(marriage), int(age), int(pay_1), int(pay_2),
                int(pay_3), int(pay_4), int(pay_5), int(pay_6),
                float(bill_amt1), float(bill_amt2), float(bill_amt3),
                float(bill_amt4), float(bill_amt5), float(bill_amt6),
                float(pay_amt1), float(pay_amt2), float(pay_amt3),
                float(pay_amt4), float(pay_amt5), float(pay_amt6)
            ]]
        }
    }

    prediction = make_prediction(data)
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
