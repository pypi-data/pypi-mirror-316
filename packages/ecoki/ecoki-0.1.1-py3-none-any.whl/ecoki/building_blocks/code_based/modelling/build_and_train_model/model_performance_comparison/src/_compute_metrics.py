from sklearn.model_selection import cross_val_score
from numpy import mean
import pandas as pd


class ComputeMetrics:

    def score(self):
        self.sc = mean(cross_val_score(self.model, self.X, self.Y, cv=self.kf))

    def mean_abs_err(self):
        self.mae = -mean(cross_val_score(self.model, self.X, self.Y, scoring='neg_mean_absolute_error', cv=self.kf))

    def root_mean_sq_err(self):
        self.rmse = -mean(cross_val_score(self.model, self.X, self.Y, scoring='neg_root_mean_squared_error', cv=self.kf))
    
    def r2(self):
        self.r_2 = mean(cross_val_score(self.model, self.X, self.Y, scoring='r2', cv=self.kf))
    
    def mean_abs_per_err(self):
        self.mape = -mean(cross_val_score(self.model, self.X, self.Y, scoring='neg_mean_absolute_percentage_error', cv=self.kf))
        
    def X_validate(self):
        # Cross validate the given model
        # model: model to be cross validated
        # X: dataframe containing all features
        # Y: dataframe containing all labels

        self.score()
        self.mean_abs_err()
        self.root_mean_sq_err()
        self.r2()
        self.mean_abs_per_err()

    def stats(self, name, df):
        # Prints the stats and appends df
        print(name + ' Scores: ')
        print('R2:', self.r_2)
        print('MAE: ', self.mae)
        print('RMSE: ', self.rmse)
        print("--------------------------")
        df = pd.concat([df, pd.DataFrame([{'Algorithm':name, 'Coeff. of Determination':self.r_2, 'Root Mean Square Error':self.rmse, 'Mean Absolute Error':self.mae, 'Mean Absolute % Error':self.mape}])], ignore_index=True)
        return df
