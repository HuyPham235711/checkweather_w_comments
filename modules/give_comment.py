import joblib
import pandas as pd

#Download the model
model = joblib.load('randomforest_model/weather_model.pkl')
vectorizer = joblib.load('randomforest_model/vectorizer.pkl')
label_encoder = joblib.load('randomforest_model/label_encoder.pkl')

def preprocess_input(temp, time, sky):
    temp = int(temp[:-2])
    hour = time.split()[2].split(':')[0]
    
    
    if hour == -1:
        raise ValueError("Thời gian không hợp lệ")
    
    sky_features = vectorizer.transform([sky]).toarray()
    sky_features = pd.DataFrame(sky_features)
    sky_features.columns = sky_features.columns.astype(str)

    input_features = pd.DataFrame([[temp, hour]], columns=['temp', 'hour'])
    input_data = pd.concat([input_features, pd.DataFrame(sky_features)], axis=1)
    
    return input_data

# predict func
def predict_weather(temp, time, sky):
    input_data = preprocess_input(temp, time, sky)
    prediction = model.predict(input_data)
    prediction_label = label_encoder.inverse_transform(prediction)
    return prediction_label[0]
