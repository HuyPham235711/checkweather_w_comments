import sys
import io
import random
import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib


# Set the default encoding to utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
#######################################################################################
#GENERATE WEATHER DATA------------------------------------------------------------------

def generate_random_time():
    
    hour = random.randint(0,23)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def generate_weather_data(num_samples):
    temps = [f"{temp}°C" for temp in range(15, 41)] #From 15 to 41 celcius
    days_of_week = ["Thứ hai","Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    sky_conditions = ["Nắng", "Mưa", "Nhiều mây", "Mây rải rác", "Sương mù", "Giông bão"]

    data = []
    for _ in range(num_samples):
        temp = random.choice(temps)
        day = random.choice(days_of_week)
        time = generate_random_time()
        sky = random.choice(sky_conditions)
        data.append({'temp': temp, 'time': f"{day} {time}", 'sky': sky})
    return data

def label_weather(data):
    comments = []
    for item in data:
        temp = int(item['temp'][:-2])
        sky = item['sky']
        if sky == "Nắng" and 20 <= temp <= 30:
            comments.append('What a wonderful day!')
        elif sky in ["Ít mây", "Nắng"] and 15 <= temp <= 35:
            comments.append('Hôm nay là một ngày đẹp')
        elif sky in ["Mây rải rác", "Nhiều mây"] or 10 <= temp <= 40:
            comments.append('Trời ổn')
        elif sky in ["Nhiều mây", "Sương mù"] or 5 <= temp <= 45:
            comments.append('Thời tiết xấu')
        else:
            comments.append('Thời tiết rất xấu')
    return comments


def generate_data_w_labels():
    #generate 1000 data samples for training
    weather_data = generate_weather_data(1000)
    labels = label_weather(weather_data)

    #convert to DataFrame
    df = pd.DataFrame(weather_data)
    df['label'] = labels
    return df

#------------------------------------------------------------------GENERATE WEATHER DATA
########################################################################################
#PREPROCESS-----------------------------------------------------------------------------
df = generate_data_w_labels()
#Encode features
vectorizer = CountVectorizer()
X_sky = vectorizer.fit_transform(df['sky']).toarray()
X_sky = pd.DataFrame(X_sky)
X_sky.columns = X_sky.columns.astype(str)

#Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['label'])


#convert temp and time features into numerical
df['temp'] = df['temp'].apply(lambda x: int(x[:-2]))
df['hour'] = df['time'].apply(lambda x: int(x.split()[2].split(':')[0]))

#concat the features
X = pd.concat([df[['temp', 'hour']], pd.DataFrame(X_sky)], axis=1)
#-----------------------------------------------------------------------------PREPROCESS
#######################################################################################
#TRAIN----------------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#train the RandomForest model
model = RandomForestClassifier(n_estimators = 100, random_state = 42)
model.fit(X_train, y_train)

#predict and evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test,y_pred,target_names = label_encoder.classes_))


# save model
joblib.dump(model, 'weather_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

#----------------------------------------------------------------------------------TRAIN
#######################################################################################