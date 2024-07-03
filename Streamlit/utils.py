import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class PrepProcesor:
    def __init__(self):
        self.ageImputer = SimpleImputer(strategy='mean')
        self.fareImputer = SimpleImputer(strategy='mean')
        self.encoder = OneHotEncoder()
        self.scaler = StandardScaler()

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='mean')),
                    ('scaler', StandardScaler())]), ['Age', 'Fare']),
                ('cat', Pipeline(steps=[
                    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore'))]), ['Sex', 'Embarked'])
            ])

    def fit(self, X):
        self.preprocessor.fit(X)

    def transform(self, X):
        return self.preprocessor.transform(X)
