import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import IsolationForest
from cleaning import load_clean_csv


class ML:
    def __init__(self,data):
        self.data = data

    def linear_regression(self, x_cols, y_col, degree):
        x = self.data[x_cols]
        y = self.data[y_col]

        poly = PolynomialFeatures(degree=degree)

        model = LinearRegression()
        # split original x for plotting, x_poly for training
        x_train_idx, x_test_idx, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        x_poly_train = poly.fit_transform(x_train_idx)
        x_poly_test = poly.transform(x_test_idx)

        model.fit(x_poly_train, y_train)

        train_score = model.score(x_poly_train, y_train)
        test_score = model.score(x_poly_test, y_test)

        print(f'Coefficients: {model.coef_}')
        print(f'Intercept: {model.intercept_:.2f}')
        print(f'Train R²: {train_score:.2f}')
        print(f'Test R²: {test_score:.2f}')

        # plot using original x
        plt.scatter(x_test_idx, y_test, color='blue', label='Test data')
        plt.scatter(x_train_idx, y_train, color='red', label='Train data')

        # plot the fit line
        x_smooth = np.linspace(x.min().values[0], x.max().values[0], 100).reshape(-1, 1)
        x_smooth_poly = poly.transform(x_smooth)
        y_smooth = model.predict(x_smooth_poly)
        coeffs = np.round(model.coef_, 3)
        intercept = round(model.intercept_, 3)
        poly_str = np.poly1d(coeffs[::-1])
        plt.plot(x_smooth, y_smooth, color='green',
                 label=f'Fit: {poly_str} + {intercept}')

        plt.legend()
        fig = plt.gcf()

        return {'coefficients': model.coef_,'intercept': model.intercept_,'train_r2': train_score,'test_r2': test_score,'fig': fig}
    def Anomalie(self,x_cols,y_col,contamination=0.1):
        x = self.data[x_cols]
        y = self.data[y_col]
        xy = pd.concat([x,y], axis=1)
        model = IsolationForest(contamination=contamination, random_state=42)
        model_anomalies = model.fit_predict(xy)
        normal_mask = model_anomalies == 1
        anomaly_mask = model_anomalies == - 1

        plt.scatter(x[normal_mask].values, y[normal_mask], color='blue', label='Normal')
        plt.scatter(x[anomaly_mask].values,y[anomaly_mask], color='red', label='Anomaly')
        plt.xlabel(x_cols)
        plt.ylabel(y_col)
        plt.legend()
        fig = plt.gcf()
        return {
            'normal_count': normal_mask.sum(),
            'anomaly_count': anomaly_mask.sum(),
            'fig': fig
        }








