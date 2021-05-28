import h5py
import numpy as np
from joblib import dump,load
h5_train_data          = "C:\\Users\\saipr\\Videos\\plant_disease_detection\\output\\train_data.h5"
h5_train_labels        = "C:\\Users\\saipr\\Videos\\plant_disease_detection\\output\\train_label.h5"

 # loading the data sets
h5f_data  = h5py.File(h5_train_data, 'r')
h5f_label = h5py.File(h5_train_labels, 'r')

global_features_string = h5f_data['dataset_1']
global_labels_string   = h5f_label['dataset_1']

global_features = np.array(global_features_string)
global_labels   = np.array(global_labels_string)

h5f_data.close()
h5f_label.close()

print(type(global_features))

from sklearn.ensemble import GradientBoostingClassifier
gradient_predictor=GradientBoostingClassifier(n_estimators=750,learning_rate=0.1)
gradient_predictor.fit(np.array(global_features),np.array(global_labels))
print("gradient_predictor_training_completed.....")

from sklearn.ensemble import RandomForestClassifier
random_forest_predictor=RandomForestClassifier(n_estimators=750,criterion='entropy',bootstrap=True,random_state=42)
random_forest_predictor.fit(np.array(global_features),np.array(global_labels))
print("random_forest_predictor_training_completed.....")
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier
hist_gradient_predictor=HistGradientBoostingClassifier(max_iter=750,learning_rate=0.1)
hist_gradient_predictor.fit(np.array(global_features),np.array(global_labels))
print("hist_gradient_predictor_training_completed.....")


dump([hist_gradient_predictor,random_forest_predictor,gradient_predictor],"model_predictor_saved.joblib",compress=1)
