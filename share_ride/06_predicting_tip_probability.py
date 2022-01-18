# Import libraries
import numpy as np
import pandas as pd


from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import normalize
import datetime as dt
from sklearn.linear_model import LogisticRegression

np.random.seed(42)


############################################################   1. load files     #####################################################################################

#load april data
df = pd.read_csv("share_ride_data.csv")


#############################################################    2. features engineering      ########################################################################

# create binary feature tipPay
df["tipPay"] = (df['Tip'] != 0).astype(int)

# use OneHotEncoding add features describe day of the week; time of the day
from sklearn.preprocessing import OneHotEncoder
df["pickupHour"] = pd.to_datetime(df["Trip Start Timestamp"], format='%m/%d/%Y %I:%M:%S %p').dt.hour
df["pickDayofweek"] = pd.to_datetime(df["Trip Start Timestamp"], format='%m/%d/%Y %I:%M:%S %p').dt.strftime("%A")
df.drop_duplicates(subset=["pickupHour","pickDayofweek","Pickup Community Area","Dropoff Community Area",'Pickup Centroid Latitude','Pickup Centroid Longitude'], inplace= True, keep='last')

encoder = OneHotEncoder(sparse=False)
onehot_encoded = encoder.fit_transform(df[["pickupHour","pickDayofweek","Pickup Community Area","Dropoff Community Area"]])
onehot_encoded_frame = pd.DataFrame(onehot_encoded,columns = encoder.get_feature_names(['hourofday', 'dayofweek','pickuparea','dropoffarea']))


#%%
# combine original features and onehot_encoded_frame
fea = df[['Pickup Centroid Latitude','Pickup Centroid Longitude']]

features = pd.concat([onehot_encoded_frame.reset_index(),fea.reset_index()], axis=1)

#########################################################    3. split data into training and tesing  ###################################################################

# features
X = normalize(features)
# label
y = df["tipPay"]

# split into 0.8 training dataset and 0.2 test dataset
X_t, X_test, y_t, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

# #split into 0.6 training dataset 0.2 validation dataset 
X_train, X_val, y_train,y_val = train_test_split(X_t, y_t, test_size=0.2, random_state=42)

########################################################   4. Hyperparameter tuning Logistic regression           ############################################################

# Hyperparameter tuning for logistic regression
parameters = {'C': np.linspace(.001,1,20)}
model = LogisticRegression(class_weight='balanced')
clf = GridSearchCV(model, parameters, cv=5)
clf.fit(X_t, y_t)
best_C = np.linspace(.001,1,20)[clf.cv_results_['rank_test_score'].argmin()]

# model w/ best C
logit_best = LogisticRegression(C=best_C,class_weight='balanced')
logit_best.fit(X_t, y_t)





########################################################   5. Evaluation for best Logistic regression              ############################################################

# same feature engineering has applied in earlier part the test data
# logistic regression prediction
#y_pred_logit_best = logit_best.predict(X_test)
#y_test_prob_logit_best =logit_best.predict_proba(X_test)
#print('Train Accuracy:', round(logit_best.score(X_t, y_t),3))
#print('Test Accuracy:', round(logit_best.score(X_test, y_test),3))
#print('Test Precision:', round(recall_score(y_test, y_pred_logit_best),3))
#print('Test Recall:', round(precision_score(y_test, y_pred_logit_best),3))
#print('Test F1 score:', round(f1_score(y_test, y_pred_logit_best),3))

########################################################   6.Get prediction result            #############################################################################
y_result = pd.DataFrame(logit_best.predict_proba(X)[:,1])
X_result =  df[["pickupHour","pickDayofweek","Pickup Community Area","Dropoff Community Area","Pickup Centroid Latitude","Pickup Centroid Longitude"]]

# #output for visulaization
visual_df = pd.concat([X_result.reset_index(),y_result.reset_index()],axis=1)
visual_df.drop_duplicates(inplace=True)
# #ship the output
visual_df.to_csv("tip_prob.csv", sep=",")

