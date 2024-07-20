from django.shortcuts import render;

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix



def Home(request):
    return render(request,"Home.html")

def Predict(request):
    return render(request,'Predict.html')
# template name should be the file name of the file should be accessed through

def Result(request):
    # return render(request,'Predict.html')
    le=LabelEncoder()
    oe=OneHotEncoder()
    

    public= pd.read_csv('Datasets\Public.csv')
    social= pd.read_csv('Datasets\Social.csv')
    environment= pd.read_csv('Datasets\Environmental.csv')

    merged_data = pd.merge(public, social, on='Date')
    environment= environment.drop(['Region'], axis=1)
    data= pd.merge(merged_data, environment, on='Date')
    
    Region_encoded=oe.fit_transform(data['Region'].values.reshape(-1,1))
    Disease_encoded=oe.fit_transform(data['Disease'].values.reshape(-1,1))
    Platform_encoded=oe.fit_transform(data['Platform'].values.reshape(-1,1))
    Hashtag_encoded=oe.fit_transform(data['Hashtag'].values.reshape(-1,1))
    Sentiment_encoded=le.fit_transform(data['Sentiment'])

    data['Region']=Region_encoded.toarray()
    data['Disease']=Disease_encoded.toarray()
    data['Platform']=Platform_encoded.toarray()
    data['Hashtag']=Hashtag_encoded.toarray()
    data['Sentiment']=Sentiment_encoded
    
    X=data.drop(['Outbreak','Date','Platform',"Hashtag","Count"],axis=1)
    y=data['Outbreak']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=40)
    RF=RandomForestClassifier(n_estimators=100,random_state=40)
    RF.fit(X_train,y_train)
        
    region=str(request.GET['n1'])
    disease=str(request.GET['n2'])
    cases=int(request.GET['n3'])
    deaths=int(request.GET['n4'])
    # platform=str(request.GET['n5'])
    air_quality_index=int(request.GET['n7'])
    temperature=float(request.GET['n8'])
    # sentiment=str(request.GET['n9'])
    humidity=float(request.GET['n10'])
    # count=int(request.GET['n11'])

    # Use Case 1: Early Warning System
    def early_warning_system(region, disease, cases, deaths, temperature, humidity, air_quality_index):
        input_data = pd.DataFrame({
            'Region': [region],
            'Disease': [disease],
            'Cases': [cases],
            'Deaths': [deaths],
            # 'Sentiment': [sentiment],
            'Temperature': [temperature],
            'Humidity': [humidity],
            'AirQualityIndex': [air_quality_index]
        })
        input_data = pd.get_dummies(input_data, columns=['Region', 'Disease'])

        # input_data = input_data[X.columns]
        input_data= input_data.reindex(columns=X.columns, fill_value=0)
        prediction = RF.predict(input_data)
        if prediction[0] == 1:
            return "Early warning: potential outbreak detected!"
        else:
            return "No early warning: no potential outbreak detected."
            
    p=early_warning_system(region, disease, cases, deaths,temperature, humidity, air_quality_index)

    return render(request,'Predict.html',{"result":p})
