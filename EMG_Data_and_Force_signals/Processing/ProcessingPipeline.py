import os
import sys
import numpy as np
#import preprocessing as prep
from scipy import signal
import scipy

class ProcessingPipeline:
    """Class used to perform a serie of processing over the data
    """
    def __init__(self, processing_list) -> None:
        """Class constructor to initialize the object

        Args:
            processing_list (list[callable]): list of callable object that accept two object as parameter
        """

        self.processingList = processing_list

    def __call__(self, x_data, y_data=None):
        """Apply the list of processing over the x_data and y_data

        Args:
            x_data (any): x_data to be processed
            y_data (any): y_data to be processed. Defaults to None.

        Returns:
            tuple[any, any]: the processed data 
            any: the processed x_data if the processed y_data == None
        """

        for p in self.processingList:

            x_data, y_data = p(x_data, y_data)

        if y_data is None:
            return x_data
        else:
            return x_data, y_data

    def getProcessingNameList(self):
        """Retrieve the names of the applied processing 

        Returns:
            list[str]: The list with the names
        """
        names = []
        for p in self.processingList:
            names.append(p.getName())
        
        return names
    
class Retification:
    """Class used to apply the retification filter over a matrix
    """

    def __init__(self) -> None:
        """Class constructor to initialize the object
        """
        self.name = 'Retification'

    def getName(self):
        """Retrieve the name of the preprocessing

        Returns:
            str: The string with the name
        """
        return self.name

    def __call__(self, x_data):
        """Perform the filter over the x_data

        Args:
            x_data (ndarray): n-D matrix to be processed
            y_data (any): y_data. Defaults to None.

        Returns:
            tuple[ndarray, any]: tuple with the filtered matrix in the first index
        """
        return np.abs(x_data)
    
class RMS:
    """ Class used to normalize individually the samples of a batch
    """
    
    def __init__(self) -> None:
        """Class constructor to initialize the object
        
        """
        
        self.name = 'DataRMS'
    def getName(self):
        """Retrieve the name of the preprocessing
        Returns:
            str: The string with the name
        """
        return self.name
    
    def __call__(self, x_data):
        """Performs the normalization of the values in x_data
        Args:
            x_data (ndarray): n-D matrix
        Returns:
            tuple[ndarray, any]: tuple with the normalized matrix in the first index
        """

        return np.sqrt(np.mean(np.power(x_data, 2),axis=-1,keepdims=True)) 

class MAV:
    """Class used to calculate the mean absolute value of a matrix
    """
    def __init__(self, n_channels=1) -> None:
        """Class constructor to initialize the object
        """
        self.name = 'MeanAbsoluteValue'
        self.n_channels= n_channels

    def getName(self):
        """Retrieve the name of the preprocessing

        Returns:
            str: The string with the name
        """
        return self.name

    def __call__(self, x_data):
        """Calculate the mean absolute value of x_data

        Args:
            x_data (ndarray): n-D matrix to be processed

        Returns:
            tuple[ndarray, any]: tuple with the processed matrix in the first index
        """
        
        return np.mean(np.abs(x_data), axis=-1, keepdims=True)
    
class NormMinMax:
    """ Class used to normalize a numpy 2D matrix to [0, 1]
    """
    
    def __init__(self, axis, minimum=0, maximum=1) -> None:
        """Class constructor to initialize the object
        
        Args:
            axis: axis to normalize
        """
        
        self.name = 'NormMinMax'
        self.axis = axis
        self.minimum = minimum
        self.maximum = maximum

    def getName(self):
        """Retrieve the name of the preprocessing

        Returns:
            str: The string with the name
        """
        return self.name

    def __call__(self, x_data):
        """Performs the normalization of the values in x_data

        Args:
            x_data (ndarray): 2D matrix
            y_data (any): y_data. Defaults to None.

        Returns:
            tuple[ndarray, any]: tuple with the normalized matrix in the first index
        """

#         samples_min = x_data.min(axis=self.axis,keepdims=True)
#         x_data = (x_data - samples_min)
#         samples_max = x_data.max(axis=self.axis,keepdims=True)
#         x_data = x_data / samples_max


        samples_min = x_data.min(axis=self.axis,keepdims=True) + sys.float_info.epsilon
        samples_max = x_data.max(axis=self.axis,keepdims=True)
        x_data = (x_data - samples_min) * (self.maximum - self.minimum)
        x_data = (x_data / (samples_max - samples_min) ) + self.minimum
        
        return x_data

class R2Calculator:
    """Class used to calculate the R-squared (R2) coefficient"""
    
    def __init__(self) -> None:
        """Class constructor to initialize the object"""
        self.name = 'R2Calculator'

    def getName(self):
        """Retrieve the name of the calculator
        
        Returns:
            str: The string with the name
        """
        return self.name

    def __call__(self, y, yest):
        """Calculate the R-squared (R2) coefficient
        
        Args:
            y (ndarray): Real output data
            yest (ndarray): Estimated output data
        
        Returns:
            float: The R-squared coefficient
        """
        y = np.array(y)
        yest = np.array(yest)

        # Calculate the squared error
        e = y - yest  # Error between the real output and the estimated output
        e2 = e ** 2  # Squared error
        SEQ = np.sum(e2)  # Sum of squared errors

        # Calculate the Multiple Correlation Coefficient (RMS)
        m1 = np.sum((y - np.mean(yest)) ** 2)  # Sum of squared differences between each sample and the mean of the samples
        R2 = 1 - (SEQ / m1)  # Multiple correlation coefficient

        return R2

class NRMSECalculator:
    """Class used to calculate the Normalized Root Mean Square Error (NRMSE)"""
    
    def __init__(self) -> None:
        """Class constructor to initialize the object"""
        self.name = 'NRMSECalculator'

    def getName(self):
        """Retrieve the name of the calculator
        
        Returns:
            str: The string with the name
        """
        return self.name

    def __call__(self, y, yest):
        """Calculate the Normalized Root Mean Square Error (NRMSE)
        
        Args:
            y (ndarray): Real output data
            yest (ndarray): Estimated output data
        
        Returns:
            float: The NRMSE value
        """
        y = np.array(y)
        yest = np.array(yest)

        # Calculate the squared error
        e = y - yest  # Error between the real output and the estimated output
        e2 = e ** 2  # Squared error
        SEQ = np.sum(e2)  # Sum of squared errors
        
        y_mean = np.mean(y)

        # Calculate the numerator of RMSE (root of squared error sum)
        num = np.sqrt(SEQ)

        # Calculate the denominator (root of sum of squared differences from the mean)
        den = np.sqrt(np.sum((y - y_mean) ** 2))

        # Calculate RMSE
        rmse = num / den

        # Calculate NRMSE
        nrmse = 1 - rmse
        
        return nrmse

class DLQRCalculator:
    """Class used to calculate the Discrete Linear Quadratic Regulator (DLQR) gain"""

    def __init__(self) -> None:
        """Class constructor to initialize the object"""
        self.name = 'DLQRCalculator'

    def getName(self):
        """Retrieve the name of the calculator

        Returns:
            str: The string with the name
        """
        return self.name

    def __call__(self, A, B, Q, R):
        """Solve the discrete time LQR controller
        
        Args:
            A (ndarray): State transition matrix
            B (ndarray): Control input matrix
            Q (ndarray): State cost matrix
            R (ndarray): Control input cost matrix
        
        Returns:
            tuple[ndarray, ndarray, ndarray]: 
                K (ndarray): The DLQR gain
                X (ndarray): Solution to the discrete-time algebraic Riccati equation
                eigVals (ndarray): Eigenvalues of the closed-loop system
        """
        # Solve the discrete-time algebraic Riccati equation
        #X = np.matrix(scipy.linalg.solve_discrete_are(A, B, Q, R))

        # Recursive Riccati Difference Equation (RDE)
        P = 100*np.eye(4)

        for k in range(1000):
            term = np.linalg.inv(np.array([B @ P @ B.T + R]).reshape(-1,1))
            P = A @ P @ A.T - (A @ P @ B.T * term) @ B @ P @ A.T + Q

        # Compute the Kalman gain
        L = (np.linalg.inv(B @ P @ B.T + R) @ B @ P @ A.T).T
        return L, P