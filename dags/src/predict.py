import joblib
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.model_selection import train_test_split
def model_linear(df, dfpredict):
    '''Handles the code to train with a Linear Regression, and test our cleaned dataset on.'''
    
    # Trying to load a saved model.
    try:
        reg = joblib.load('./output/reg.pkl')

    # If no model has been saved, below gets executed.
    except:
        # Instantiating our regressor(s).
        reg = LinearRegression()

        X = df.drop(['price'], axis=1).to_numpy()
        y = df['price'].to_numpy()

        # Reshaping 'y' to be 2D array. Optional. To get score from RandomForest, needs to be commented out.
        #y = y.reshape(-1, 1) 

        # Setting up 'train_test_split' to get standardized training/testing sets.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) # Random state can be added to get the same results every time.

        # Fitting our data to train the model.
        reg.fit(X_train, y_train)

        # Saving the fit data so it can be re-used.
        joblib.dump(reg, './output/reg.pkl')

    # Displaying score of Training variables.
    #print("Linear Training score:", reg.score(X_train, y_train)) 

    # Predicting the 'y' target value (Price).
    y_prediction = reg.predict(dfpredict)

    # Displaying the score of Testing variables
    #print("Linear Testing score:", reg.score(X_test, y_test), '\n')
    return y_prediction