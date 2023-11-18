import sys
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import json
file_path = '34708051.csv'
data = pd.read_csv(file_path)
location_name = sys.argv[1]
filtered_data = data[data['NAME'] == location_name]
if filtered_data.empty:
    res = "No data available. Unable to make predictions."
    res2 = {"message": res}
    print(json.dumps(res2))
else:
    X_temp = filtered_data[['date2']]
    y_temp = filtered_data['temp']

    if len(X_temp) < 2:
        res5 = "Not enough data available to make temperature predictions."
        res6 = {"message": res5} 
        print(json.dumps(res6))
    else:
        X_temp_train, X_temp_test, y_temp_train, y_temp_test = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42)
        lr_temp = LinearRegression()
        lr_temp.fit(X_temp_train, y_temp_train)
        day_temp = lr_temp.predict(X_temp_test)
        rmse_temp = np.sqrt(mean_squared_error(y_temp_test, day_temp))
        predict_temp = pd.DataFrame({'date2': [213]})
        predicted_temp = lr_temp.predict(predict_temp)
    X_windspeed = filtered_data[['temp', 'date2']]
    y_windspeed = filtered_data['windspeed']

    if len(X_windspeed) < 2:
        res3 = "Not enough data available to make wind speed predictions."
        res4 = {"message": res3}
        print(json.dumps(res4))
    else:
        X_ws_train, X_ws_test, y_ws_train, y_ws_test = train_test_split(X_windspeed, y_windspeed, test_size=0.2, random_state=42)
        lr_windspeed = LinearRegression()
        lr_windspeed.fit(X_ws_train, y_ws_train)
        day_windspeed = lr_windspeed.predict(X_ws_test)
        rmse_windspeed = np.sqrt(mean_squared_error(y_ws_test, day_windspeed))
        predict_windspeed = pd.DataFrame({'temp': [predicted_temp[0]], 'date2': [213]})
        predicted_windspeed = lr_windspeed.predict(predict_windspeed)
        output_data = {"temp": predicted_temp[0], "windspeed": predicted_windspeed[0], "rmse_temp": rmse_temp, "rmse_windspeed": rmse_windspeed}
        print(json.dumps(output_data))
