import pandas as pd
import numpy as np
from fastFM import sgd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix, hstack, csc_matrix
from fastFM import als
from sklearn.metrics.pairwise import cosine_similarity
from viturka.utils import handle_missing_values

def find_similar_items(model, dict_vectorizer, item_features, item_id, item_id_column, numerical_columns, categorical_columns, top_k=5):
    # Validate the item exists
    if item_id not in item_features[item_id_column].values:
        raise ValueError(f"Item ID {item_id} not found in the dataset.")

    # Combine categorical and numerical features
    categorical_features = dict_vectorizer.transform(item_features[categorical_columns].to_dict(orient="records"))
    numerical_features = csc_matrix(item_features[numerical_columns].values)

    # Concatenate features
    item_matrix = hstack([categorical_features, numerical_features])
    item_matrix = csc_matrix(item_matrix)  # Convert to CSC format

    # Derive item latent vectors
    item_latent_vectors = item_matrix @ model.V_.T

    # Find the index of the item
    item_index = item_features[item_features[item_id_column] == item_id].index[0]

    # Compute cosine similarity
    item_latent_vector = item_latent_vectors[item_index].reshape(1, -1)
    similarities = cosine_similarity(item_latent_vector, item_latent_vectors).flatten()

    # Retrieve top-k similar items
    similar_indices = similarities.argsort()[::-1][:top_k + 1]  # Include itself
    similar_items = [
        (item_features.iloc[i][item_id_column], similarities[i]) for i in similar_indices if i != item_index
    ]

    return similar_items[:top_k]

def train_model(
    file,
    target_column,
    numerical_columns,
    categorical_columns,
    n_iter=100,
    rank=8,
    init_stdev=0.01,
    step_size=0.01,
    l2_reg_w=0.001,
    l2_reg_V=0.001,
    test_size=0.2,
    vectorizer=None,
    pre_process = False,
    advanced_imputation = None
):
    """
    Train a factorization machine (FM) model on any dataset while avoiding data leakage.
    """
    # Load the dataset from CSV
    df = pd.read_csv(file)

    if pre_process:
        df = handle_missing_values(df, drop_threshold=0.7, fill_threshold=0.3, advanced_imputation=advanced_imputation)

    # Validate required columns
    required_columns = set([target_column] + numerical_columns + categorical_columns)
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in dataset: {missing_columns}")

    # Ensure categorical columns are strings
    df[categorical_columns] = df[categorical_columns].astype(str)

    # Ensure numerical columns are floats
    df[numerical_columns] = df[numerical_columns].astype(float)

    # Split the dataset into training and testing sets
    X = df[numerical_columns + categorical_columns]
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Scale numerical features
    scaler = MinMaxScaler()
    X_train[numerical_columns] = scaler.fit_transform(X_train[numerical_columns])
    X_test[numerical_columns] = scaler.transform(X_test[numerical_columns])

    # Encode categorical features
    if vectorizer is None:
        vectorizer = DictVectorizer(sparse=True)
        categorical_features_train = vectorizer.fit_transform(X_train[categorical_columns].to_dict(orient="records"))
    else:
        # Combine the vocabulary of the provided vectorizer with the training data
        combined_vocab = set(vectorizer.feature_names_)
        temp_vectorizer = DictVectorizer(sparse=True)
        temp_vectorizer.fit(X_train[categorical_columns].to_dict(orient="records"))
        combined_vocab.update(temp_vectorizer.feature_names_)

        # Create a new vectorizer with the combined vocabulary
        new_vectorizer = DictVectorizer(sparse=True)
        new_vectorizer.fit([{key: 0 for key in combined_vocab}])
        vectorizer = new_vectorizer

    categorical_features_train = vectorizer.transform(X_train[categorical_columns].to_dict(orient="records"))
    categorical_features_test = vectorizer.transform(X_test[categorical_columns].to_dict(orient="records"))

    # Combine numerical and categorical features
    numerical_features_train = csr_matrix(X_train[numerical_columns].values)
    numerical_features_test = csr_matrix(X_test[numerical_columns].values)
    X_train_combined = hstack([categorical_features_train, numerical_features_train])
    X_test_combined = hstack([categorical_features_test, numerical_features_test])

    # Scale the combined feature matrix
    max_abs_scaler = MaxAbsScaler()
    X_train_combined = max_abs_scaler.fit_transform(X_train_combined)
    X_test_combined = max_abs_scaler.transform(X_test_combined)

    # Scale the target variable
    scaler_target = MinMaxScaler()
    y_train_scaled = scaler_target.fit_transform(y_train.values.reshape(-1, 1)).flatten()
    y_test_scaled = scaler_target.transform(y_test.values.reshape(-1, 1)).flatten()

    # Train the FM model
    model = als.FMRegression(
        n_iter=n_iter,
        init_stdev=init_stdev,
        l2_reg_w=l2_reg_w,
        l2_reg_V=l2_reg_V,
        rank=rank,
    )
    model.fit(X_train_combined, y_train_scaled)

    return model, X_train_combined, X_test_combined, y_test_scaled, vectorizer, scaler_target, df

def evaluate_model(model, X_test, y_test, scaler_target):
    """
    Evaluate the FM model using mean squared error while ensuring proper handling of the test set.
    """
    # Predict and inverse transform
    pred_scaled = model.predict(X_test)
    pred = scaler_target.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()
    y_test_original = scaler_target.inverse_transform(y_test.reshape(-1, 1)).flatten()

    # Filter valid predictions
    valid_indices = ~np.isnan(y_test_original) & ~np.isnan(pred)
    y_test_filtered = y_test_original[valid_indices]
    pred_filtered = pred[valid_indices]

    # Compute MSE
    mse = mean_squared_error(y_test_filtered, pred_filtered)
    return pred_filtered, mse, y_test_filtered
