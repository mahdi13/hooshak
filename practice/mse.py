import numpy as np
from sklearn import linear_model, datasets

if __name__ == '__main__':
    data_x = np.array([[1], [5], [1], [5], [5], [5], [5], [5], [5], [5], [1], [5], [1], [5], [5], [1], [5], [1], [5], [5], [1], [5], [1], [5], [5]])
    data_y = np.array([[1], [1], [5], [5], [5], [5], [5], [5], [5], [1], [5], [1], [5], [5], [1], [5], [1], [5], [5], [1], [5], [1], [5], [5], [4]])

    to_predict_data_x = np.array([[10]])
    to_compare_data_y = np.array([[2400]])

    diabetes = datasets.load_diabetes()
    diabetes_X = diabetes.data[:, np.newaxis, 2]

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(data_x, data_y)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % np.mean((regr.predict(data_x) - data_y) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(data_x, data_y))
