import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.linear_model import LinearRegression
from scipy.sparse import hstack, csc_matrix

import hashlib


def obfuscate_user_id(user_id, client_key):
    """
      Obfuscates or encrypts a user ID into a unique string.

      Parameters:
      user_id (str): The user ID to obfuscate.
      client_key (str): A unique key for the client (serves as a salt).

      Returns:
      str: The obfuscated user ID as a unique string.
    """
    # Combine the user_id and client_key to create a unique input
    combined = f"{client_key}:{user_id}"

    # Use a cryptographic hash function (e.g., SHA-256) to generate a unique hash
    hash_object = hashlib.sha256(combined.encode('utf-8'))

    # Convert the hash to a hexadecimal string
    obfuscated_id = hash_object.hexdigest()

    return obfuscated_id

def combine_dat_files_general(ratings_file, users_file, items_file, output_file,
                              ratings_columns, users_columns, items_columns,
                              user_id_col, item_id_col):
    """
    Combines ratings, users, and items .dat files into a single CSV file with customizable column names.

    Parameters:
    - ratings_file (str): Path to the ratings file.
    - users_file (str): Path to the users file.
    - items_file (str): Path to the items file.
    - output_file (str): Path to save the combined CSV file.
    - ratings_columns (list of str): Column names for the ratings dataset.
    - users_columns (list of str): Column names for the users dataset.
    - items_columns (list of str): Column names for the items dataset.
    - user_id_col (str): Name of the column in all datasets that represents the user ID.
    - item_id_col (str): Name of the column in all datasets that represents the item ID.

    Returns:
    - None
    """
    try:
        # Load ratings file
        ratings = pd.read_csv(
            ratings_file,
            delimiter="::",
            header=None,
            names=ratings_columns,
            engine="python",
            encoding="ISO-8859-1",  # Specify encoding here
        )

        # Load users file
        users = pd.read_csv(
            users_file,
            delimiter="::",
            header=None,
            names=users_columns,
            engine="python",
            encoding="ISO-8859-1"  # Specify encoding here
        )

        # Load items file
        items = pd.read_csv(
            items_file,
            delimiter="::",
            header=None,
            names=items_columns,
            engine="python",
            encoding="ISO-8859-1"
        )

        # Merge datasets: ratings + users
        ratings_users = pd.merge(ratings, users, on=user_id_col)

        # Merge the result with items
        combined_data = pd.merge(ratings_users, items, on=item_id_col)

        # Save the combined data to a CSV file
        combined_data.to_csv(output_file, index=False)

        print(f"Combined dataset saved to: {output_file}")
    except Exception as e:
        print(f"Error combining datasets: {e}")

def handle_missing_values(df, drop_threshold=0.3, fill_threshold=0.7, advanced_imputation=None):
    """
    Handles missing values in a DataFrame by dropping or imputing columns based on the percentage of NaN values.
    Includes options for KNN or Regression-based imputation for numerical features.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        drop_threshold (float): Percentage of missing values above which columns are dropped (default: 0.7).
        fill_threshold (float): Percentage of missing values below which columns are imputed (default: 0.3).
        advanced_imputation (str or None): Type of advanced imputation for numerical features ('knn', 'regression', or None).

    Returns:
        pd.DataFrame: A DataFrame with missing values handled.
    """
    df_cleaned = df.copy()
    missing_percentages = df_cleaned.isna().mean()

    # Drop columns with missing values above the drop_threshold
    to_drop = missing_percentages[missing_percentages > drop_threshold].index
    df_cleaned = df_cleaned.drop(columns=to_drop)
    print(f"Dropped columns: {list(to_drop)}")

    # Handle remaining columns
    for column in df_cleaned.columns:
        missing_percentage = missing_percentages[column]
        if 0 < missing_percentage <= fill_threshold:
            if df_cleaned[column].dtype in ['float64', 'int64']:
                # Use mean or median based on skewness
                skewness = df_cleaned[column].skew()
                strategy = 'median' if abs(skewness) > 1 else 'mean'
                imputer = SimpleImputer(strategy=strategy)
                df_cleaned[column] = imputer.fit_transform(df_cleaned[[column]])
                print(f"Imputed column '{column}' using {imputer.strategy}.")
            else:
                # Use mode for categorical data
                imputer = SimpleImputer(strategy='most_frequent')
                df_cleaned[column] = imputer.fit_transform(df_cleaned[[column]]).ravel()
                print(f"Imputed column '{column}' using most_frequent strategy.")
        elif fill_threshold < missing_percentage <= drop_threshold:
            if df_cleaned[column].dtype in ['float64', 'int64'] and advanced_imputation:
                if advanced_imputation == "knn":
                    print(f"Imputing column '{column}' using KNNImputer.")
                    knn_imputer = KNNImputer(n_neighbors=5)
                    df_cleaned[column] = knn_imputer.fit_transform(df_cleaned[[column]])
                elif advanced_imputation == "regression":
                    print(f"Imputing column '{column}' using Regression Imputation.")
                    df_cleaned = _regression_imputation(df_cleaned, column)
            else:
                # Use mode for categorical data
                imputer = SimpleImputer(strategy='most_frequent')
                df_cleaned[column] = imputer.fit_transform(df_cleaned[[column]]).ravel()
                print(f"Imputed column '{column}' using most_frequent strategy.")

    return df_cleaned


def _regression_imputation(df, target_column):
    """
    Performs regression-based imputation for a column with missing values.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the column to be imputed.
        target_column (str): The column to be imputed.

    Returns:
        pd.DataFrame: The DataFrame with the target column imputed.
    """
    # Separate rows with and without missing values in the target column
    missing_rows = df[df[target_column].isna()]
    complete_rows = df[~df[target_column].isna()]

    # Separate features and target
    X_complete = complete_rows.drop(columns=[target_column])
    y_complete = complete_rows[target_column]
    X_missing = missing_rows.drop(columns=[target_column])

    # Drop columns with NaNs in features
    X_complete = X_complete.dropna(axis=1)
    X_missing = X_missing[X_complete.columns]

    # If sufficient features are available for regression
    if not X_complete.empty and not X_missing.empty:
        # Train a regression model
        model = LinearRegression()
        model.fit(X_complete, y_complete)

        # Predict missing values
        predicted_values = model.predict(X_missing)
        df.loc[missing_rows.index, target_column] = predicted_values
        print(f"Regression imputed column '{target_column}' with {len(predicted_values)} values.")

    return df

def correlation_matrix(file, selected_columns):
    df = pd.read_csv(file).dropna()
    data = df[selected_columns]
    correlation_matrix = data.corr()

    # Plot the correlation matrix using seaborn
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix of Selected Features')
    plt.show()

