import sys
import pandas as pd
from sklearn.svm import SVC
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import json 

file_path = '34708051.csv'  
data = pd.read_csv(file_path)
X = data[['temp', 'windspeed']]
y = data['rain']
location_name = sys.argv[1]

filtered_data = data[data['NAME'] == location_name]

if filtered_data.empty:
    res = "No data available. Unable to make predictions."
    res2 = {"message": res}
    print(json.dumps(res2))
else:
    threshold = 0.5
    y_filtered = (filtered_data['rain'] >= threshold).astype(int)  
    X_filtered = filtered_data[['temp', 'windspeed']]
    
    if len(X_filtered) < 2:
        res3 = "Not enough data available to make predictions."
        res4 = {"message": res3}
        print(json.dumps(res4))
    else:
        X_train, X_test, y_train, y_test = train_test_split(X_filtered, y_filtered, test_size=0.2, random_state=42)
        feature_imputer = SimpleImputer(strategy='mean')
        X_train = feature_imputer.fit_transform(X_train)
        clf = SVC(random_state=42)
        label_encoder = LabelEncoder()
        y_train = label_encoder.fit_transform(y_train)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(feature_imputer.transform(X_test))
        accuracy = accuracy_score(y_test, y_pred) * 100
        a = sys.argv[2]
        b = sys.argv[3]
        c = sys.argv[4]
        d = sys.argv[5]
        input_data = pd.DataFrame({'temp': [a], 'windspeed': [b]})
        input_data = feature_imputer.transform(input_data)
        predicted_rain = clf.predict(input_data)
        if predicted_rain == 1:
            prediction_message = "Rain is predicted."
        else:
            prediction_message = "No rain is predicted."
        response = {
        "message": f"{prediction_message}",
        "acc":f"{accuracy:.2f}%",
        "temp": a+" F",
        "rmse_temp":"RMSE: " +c,
        "windspeed": b+" km/h",
        "rmse_windspeed":"RMSE: " +d
        }
        print(json.dumps(response))
