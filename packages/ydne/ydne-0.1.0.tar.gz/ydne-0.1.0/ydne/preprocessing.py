# ydne/preprocessing.py
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class DataPreprocessor:
    """
    A class to handle common data preprocessing tasks.
    """
    
    @staticmethod
    def scale_features(X, method='standard'):
        """
        Scale features using different methods.
        
        Args:
            X (numpy.ndarray or pandas.DataFrame): Input features
            method (str, optional): Scaling method. Defaults to 'standard'.
        
        Returns:
            numpy.ndarray: Scaled features
        """
        if method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError("Unsupported scaling method")
        
        return scaler.fit_transform(X)
    
    @staticmethod
    def handle_missing_values(df, strategy='mean'):
        """
        Handle missing values in a DataFrame.
        
        Args:
            df (pandas.DataFrame): Input DataFrame
            strategy (str, optional): Strategy to handle missing values. Defaults to 'mean'.
        
        Returns:
            pandas.DataFrame: DataFrame with handled missing values
        """
        if strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'median':
            return df.fillna(df.median())
        elif strategy == 'drop':
            return df.dropna()
        
        raise ValueError("Unsupported missing value strategy")
