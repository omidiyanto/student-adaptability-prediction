from flask import Flask, request, render_template
import requests
from requests.structures import CaseInsensitiveDict
from flask import json
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_data = False

    if request.method == 'POST':
        print(request.form['gender'])
        print(request.form['age'])
        print(request.form['education'])
        print(request.form['institution'])
        print(request.form['it'])
        print(request.form['location'])
        print(request.form['load'])
        print(request.form['financial'])
        print(request.form['internet'])
        print(request.form['network'])
        print(request.form['class'])
        print(request.form['self'])
        print(request.form['device'])
        gender_value = request.form['gender']
        age_value = request.form['age']
        education_value = request.form['education']
        institution_value = request.form['institution']
        it_value = request.form['it']
        location_value = request.form['location']
        load_value = request.form['load']
        financial_value = request.form['financial']
        internet_value = request.form['internet']
        network_value = request.form['network']
        class_value = request.form['class']
        self_value = request.form['self']
        device_value = request.form['device']

        access_token = get_access_token()

        prediction_value = get_prediction(
            access_token,
            gender_value, age_value, education_value, institution_value, it_value, location_value,
            load_value, financial_value, internet_value, network_value, class_value,
            self_value, device_value
        )

        prediction_data = prediction_value
    return render_template('index.html', prediction = prediction_data)

def get_access_token():
    url = "https://iam.cloud.ibm.com/oidc/token"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=6G7tkcAly7v1NShdtsmJpgQWw7pqLI7iMV7u4Ek0imQR"
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code == 200:
        json_resp = resp.json()
        return json_resp.get('access_token')
    else:
        return None

def get_prediction(access_token, *input_values):
    url = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/ee78d48e-144c-43a7-8966-bf3c9893ac70/predictions?version=2021-05-01"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + access_token

    data = {
        "input_data": [
            {
                "fields": [
                    "Gender", "Age", "Education Level", "Institution Type", "IT Student", "Location",
                    "Load-shedding", "Financial Condition", "Internet Type", "Network Type",
                    "Class Duration", "Self Lms", "Device"
                ],
                "values": [list(input_values)]
            }
        ]
    }

    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code == 200:
        predictions = resp.json()
        prediction_value = predictions['predictions'][0]['values'][0][0]
        output = json.loads(resp.text)
        print("output >>", output)
        return prediction_value
    else:
        return None
#Run below code if you host it locally
#if __name__ == '__main__':
#    app.run(debug=False,host='0.0.0.0')
#omidiyanto
