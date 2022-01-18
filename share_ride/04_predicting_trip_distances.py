

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

np.random.seed(42)


############################################################   1. load files     #####################################################################################

#load april data
df = pd.read_csv("share_ride_data.csv")


#############################################################    2. features engineering      ########################################################################


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
X = features
# label
y = df["Trip Miles"]

# split into 0.8 training dataset and 0.2 test dataset
X_t, X_test, y_t, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

# #split into 0.6 training dataset 0.2 validation dataset 
X_train, X_val, y_train,y_val = train_test_split(X_t, y_t, test_size=0.2, random_state=42)

########################################################   4. Hyperparameter tuning Random Forest           ############################################################

# Hyperparameter tuning for random forest 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score, mean_squared_error, make_scorer

def RMSE(y_true,y_pred):
    rmse = mean_squared_error(y_true, y_pred)
    return rmse

def R2(y_true,y_pred):    
    r2 = r2_score(y_true, y_pred)
    return r2

def two_score(y_true,y_pred):    
    RMSE(y_true,y_pred) #set score here and not below if using MSE in GridCV
    score = R2(y_true,y_pred)
    return score

def two_scorer():
    return make_scorer(two_score, greater_is_better=True) # change for false if using MSE

# Hyperparameter tuning for random forest 
parameters = {'max_depth': np.arange(2,5), 'min_samples_split': np.arange(2,50,10), 'min_samples_leaf': np.arange(1,50,10)}
model = RandomForestRegressor()
clf = GridSearchCV(model, parameters, cv=5, scoring=two_scorer())
clf.fit(X_t, y_t)
best_max_depth = clf.best_params_['max_depth']
best_min_samples_split = clf.best_params_['min_samples_split']
best_min_samples_leaf = clf.best_params_['min_samples_leaf']



# model w/ best C
forest_best =RandomForestRegressor( max_depth= best_max_depth, min_samples_split= best_min_samples_split, min_samples_leaf = best_min_samples_leaf)
forest_best.fit(X_t, y_t)

########################################################   5. Evaluation for best Random Forest              ############################################################

# y_pred_forest_best = forest_best.predict(X_test)
# y_test_prob_forest_best = forest_best.predict_proba(X_test)
# print('Train Accuracy:', round(forest_best.score(X_t, y_t),3))
# print('Test Accuracy:', round(forest_best.score(X_test, y_test),3))
# print('Test Precision:', round(recall_score(y_test, y_pred_forest_best),3))
# print('Test Recall:', round(precision_score(y_test, y_pred_forest_best),3))
# print('Test F1 score:', round(f1_score(y_test, y_pred_forest_best),3))

#plot confusio matrix
# plot_confusion_matrix(forest_best, X_test, y_test, values_format='d')
# plt.title('Random forest: confusion matrix of test data');

########################################################   6.Get prediction result            #############################################################################
y_result = pd.DataFrame(forest_best.predict(X))
X_result =  df[["pickupHour","pickDayofweek","Pickup Community Area","Dropoff Community Area","Pickup Centroid Latitude","Pickup Centroid Longitude"]]

# #output for visulaization
visual_df = pd.concat([X_result.reset_index(),y_result.reset_index()],axis=1)
visual_df.drop_duplicates(inplace=True)
# #ship the output
visual_df.to_csv("trip_dist_pred.csv", sep=",")

