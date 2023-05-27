import joblib
import pandas as pd
from Projects import hotel_pipeline as hp

hotel_reserv = pd.read_csv("Projects/Hotel Reservations.csv")
df = hotel_reserv.copy()
X, y = hp.booking_stat_data_prep(df)
random_user = df.sample(1, random_state=12)
new_model = joblib.load("final_model.pkl")
predictions = new_model.predict(random_user)

import joblib
import pandas as pd
import hotel_pipeline as hp

# new_data =[]
hotel_reserv = pd.read_csv("data/Hotel Reservations.csv")
df = hotel_reserv.copy()
X, y = hp.booking_stat_data_prep(df)
new_X, low_importance_features = hp.low_impoortance(X, y)
random_user = (new_X.sample(1, random_state=12))
df = pd.concat([df, random_user], ignore_index=True)
new_model = joblib.load("C:/Users/User\Desktop\Project\Final/final_model1.pkl")
new_X, low_importance_features = hp.low_impoortance(X, y)
last_user = new_X.iloc[-1].values.reshape(1, -1)
prediction = new_model.predict(last_user)
print(prediction)
