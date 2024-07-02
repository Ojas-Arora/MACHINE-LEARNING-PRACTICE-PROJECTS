from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer 
import re

class PrepProcesor(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
        self.ageImputer = SimpleImputer(strategy='mean')

    def fit(self, X, y=None):
        self.ageImputer.fit(X[['Age']])
        return self

    def transform(self, X, y=None):
        X = X.copy()
        X['Age'] = self.ageImputer.transform(X[['Age']])
        X['CabinClass'] = X['Cabin'].fillna('M').apply(lambda x: str(x).replace(" ", "")).apply(lambda x: re.sub(r'[^a-zA-Z]', '', x))
        X['CabinNumber'] = X['Cabin'].fillna('M').apply(lambda x: str(x).replace(" ", "")).apply(lambda x: re.sub(r'[^0-9]', '', x)).replace('', 0) 
        X['Embarked'] = X['Embarked'].fillna('M')
        X = X.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)
        
        # Ensure all columns are present in the final transformed dataframe
        for col in self.columns:
            if col not in X.columns:
                X[col] = 0  # or handle missing columns appropriately
        
        return X
