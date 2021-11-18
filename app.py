from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "eyJraWQiOiIyMDIxMTAxODA4MTkiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC01NTAwMDQ4Szg0IiwiaWQiOiJJQk1pZC01NTAwMDQ4Szg0IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiNDJhZGQ0ZWYtYWE0MS00ZjRlLThlZjItMDdkODM1ZDZmOTRhIiwiaWRlbnRpZmllciI6IjU1MDAwNDhLODQiLCJnaXZlbl9uYW1lIjoiUC5NLiIsImZhbWlseV9uYW1lIjoiU2hyZWVuaWRoaSIsIm5hbWUiOiJQLk0uIFNocmVlbmlkaGkiLCJlbWFpbCI6Im5pZGhpcHVyYW5pY21hdGgxM0BnbWFpbC5jb20iLCJzdWIiOiJuaWRoaXB1cmFuaWNtYXRoMTNAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoibmlkaGlwdXJhbmljbWF0aDEzQGdtYWlsLmNvbSIsImlhbV9pZCI6IklCTWlkLTU1MDAwNDhLODQiLCJuYW1lIjoiUC5NLiBTaHJlZW5pZGhpIiwiZ2l2ZW5fbmFtZSI6IlAuTS4iLCJmYW1pbHlfbmFtZSI6IlNocmVlbmlkaGkiLCJlbWFpbCI6Im5pZGhpcHVyYW5pY21hdGgxM0BnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJib3VuZGFyeSI6Imdsb2JhbCIsInZhbGlkIjp0cnVlLCJic3MiOiJiNmNiZGE3NDkxODE0MTljYTIzYWZhM2NjMTdlMzlmOCIsImZyb3plbiI6dHJ1ZX0sImlhdCI6MTYzNTgzMzc1NCwiZXhwIjoxNjM1ODM3MzU0LCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.Mk-RhqOcbXcuqoS2xXnhKkLVzZKYozAM06DnjadYRqaVFhup7ANCuDFTT1wpm1DyoYtji7WoON8JBaliMpwODl0y2vsgNWS3VjTGuXI6qUL3FISqSMw4AqCLDVqE7Knc99gSCUVi0OH85hmtatlNNuiFMg4TlGzmn7Z3GYuEUbX4j7oLMfdFJixijt_AWwJQKJZes6Yd_3bwQvNW_ylXOfQFtdBmmuwPoOFu6LvZVLK0PXOazRNNHF7Y2MNldElYzDEU_xw6XbBK4NeS_Xkl4bUi5yuslzRafNqznKFl0QbjCRlA1ChJ7WWqL8oafPS6DVRbeqSfSy6-2_nmuxC3wQ"}

        if(form.bmi.data == None): 
          python_object = []
        else:
          python_object = [form.age.data, form.sex.data, float(form.bmi.data),
            form.children.data, form.smoker.data, form.region.data]
        #Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["age", "sex", "bmi",
          "children", "smoker", "region"], "values": userInput }]}

        response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2ad7e414-a6b9-4530-9d99-b12867a1bd86/predictions?version=2020-09-01", json=payload_scoring, headers=header)

        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]
        
        roundedCharge = round(bc[0][0],2)

  
        form.abc = roundedCharge # this returns the response back to the front page
        return render_template('index.html', form=form)