import pandas as pd 
import numpy as np 
from flask import Flask, render_template, url_for, jsonify, request, redirect
import mysql.connector 
import requests
from tensorflow import keras 
from sklearn.preprocessing import MinMaxScaler

dbku = mysql.connector.connect( 
    host = 'localhost', 
    port = '3306', 
    user = 'root', 
    passwd = 'tenebrae',
    database = 'testestes'
)

app = Flask(__name__) 

# model = keras.models.load_model('./model2/trained_heart_model.h5')

# ---Login---

@app.route('/', methods=['GET', 'POST']) 
def home():  
    if request.method == 'GET':
        return render_template('login.html') 
    elif request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']

        x = dbku.cursor(dictionary=True) 

        query = 'select * from ListUser' 
        x.execute(query) 

        tampungUser = list(x) 
        listUsername = []  
        listPassword = []  

        for i in tampungUser: 
            listUsername.append(i['Nama'])
            listPassword.append(i['Password'])

        if username in listUsername and password == listPassword[listUsername.index(username)]:
            return redirect(url_for('form', user=username))
            # return render_template('form.html')
        else:
            return render_template('error_login.html')

# ---Signup---

@app.route('/signup', methods=['GET', 'POST']) 
def signup():  
    if request.method == 'GET':
        return render_template('signup.html') 
    elif request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']

        x = dbku.cursor(dictionary=True) 

        query = 'select * from ListUser' 
        x.execute(query) 

        tampungUser = list(x) 
        listUsername = []  
        listPassword = []  

        for i in tampungUser: 
            listUsername.append(i['user'])

        if username in listUsername:
            return render_template('error_signup.html')
        else:
            dataUser = (username, password)
            query = 'CREATE TABLE IF NOT EXISTS ListUser (user varchar(50), password varchar(50));'
        
            x = dbku.cursor()
            x.execute(query) 

            queryku = 'insert into ListUser (user, Password) values(%s, %s)' 
            x.execute(queryku, dataUser) 
            dbku.commit()

            return render_template('proceed_signup.html')

# --Form--

@app.route('/form/<string:user>')
def form(user):
    return render_template('form.html', user=user) 

@app.route('/predict', methods=['POST'])
def predict():
    body = request.form 

    user = body['user']
    age = int(body['age'])
    sex = int(body['sex'])
    cp = int(body['cp'])
    trestbps = int(body['trestbps'])
    chol = int(body['chol'])
    fbs = int(body['fbs'])
    restecg = int(body['restecg'])
    thalach = int(body['thalach'])
    exang = int(body['exang'])
    oldpeak = float(body['oldpeak'])
    slope = int(body['slope'])
    ca = int(body['ca'])
    thal = int(body['thal']) 

    list_data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    tuple_data = (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)

    dfData = pd.DataFrame(list_data)

    print(list_data)
    # querytable = 'CREATE TABLE IF NOT EXISTS ListData (user varchar(50), age int, sex int, cp int, trestbps int, chol int, fbs int, restecg int, thalach int, exang int, oldpeak int, slope int, ca int, thal int, proba float);'
    # x = dbku.cursor()
    # x.execute(query) 

    # Prediksi

    scaler = MinMaxScaler() 

    data_scale = scaler.fit_transform(dfData) 
    list_data_scale = list(data_scale) 
    
    list_tampung = []
    for i in list_data_scale: 
        list_tampung.append(i[0])

    dfData_scale = pd.DataFrame([list_tampung])
    # print(list_tampung)
    print(dfData_scale)

    model = keras.models.load_model('./model2/trained_heart_model.h5')
    prediction = model.predict_classes(dfData_scale)
    probability = model.predict(dfData_scale) 

    print(prediction, probability)


    return "sukses"

if __name__ == '__main__': 
    app.run(debug=True)