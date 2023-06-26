import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

data = pd.read_csv('climate.csv')
X = data[['precipitation', 'temp_max', 'temp_min', 'wind']]
y = data['weather']

classifier = DecisionTreeClassifier()
classifier.fit(X, y)

joblib.dump(classifier, 'dtm.joblib')
