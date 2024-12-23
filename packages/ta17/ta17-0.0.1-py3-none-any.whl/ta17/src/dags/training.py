import datetime

import pendulum
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator


def generate_data(params, **kwargs):
    import pandas as pd
    import sklearn.datasets

    print("Starting the process of generating a synthetic dataset...")
    print(f"Parameters for dataset generation: {params}")

    n_samples = params.get("n_samples", 1000)
    n_features = params.get("n_features", 20)
    n_informative = params.get("n_informative", 10)
    n_redundant = params.get("n_redundant", 5)
    n_classes = params.get("n_classes", 2)
    random_state = params.get("random_state", 42)
    target_column = params.get("target_column", "target")

    X, y = sklearn.datasets.make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_classes=n_classes,
        random_state=random_state,
    )

    dataset = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(n_features)])
    dataset[target_column] = y

    dataset.to_csv(
        params.get("synthetic_data_path", "/opt/airflow/data/raw/dataset_airflow.csv"), index=False
    )
    print(
        f"Synthetic dataset generation complete. Dataset saved to {params.get('synthetic_data_path', '/opt/airflow/data/raw/dataset_airflow.csv')}"
    )


def preprocess_data(params, **kwargs):
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    synthetic_data_path = params.get(
        "synthetic_data_path", "/opt/airflow/data/raw/dataset_airflow.csv"
    )
    processed_data_path = params.get(
        "processed_data_path", "/opt/airflow/data/processed/processed_data_airflow.pkl"
    )
    target_column = params.get("target_column", "target")

    print(f"Loading dataset from {synthetic_data_path}...")
    df = pd.read_csv(synthetic_data_path)
    print(f"Dataset shape: {df.shape}")
    print("Dataset loaded successfully.")

    X, y = df.drop(columns=[target_column]), df[target_column]

    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

    numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])
    categorical_transformer = Pipeline(steps=[("onehot", OneHotEncoder(handle_unknown="ignore"))])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    print("Fitting and transforming dataset...")
    X_processed = pd.DataFrame(preprocessor.fit_transform(X))
    print(f"Processed feature set shape: {X_processed.shape}")

    print("Splitting dataset into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42
    )

    processed_data = {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}
    with open(processed_data_path, "wb") as f:
        pd.to_pickle(processed_data, f)

    print(f"Processing dataset complete. Processed dataset saved to {processed_data_path}.")


def train_model(params, **kwargs):
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier

    processed_data_path = params.get(
        "processed_data_path", "/opt/airflow/data/processed/processed_data_airflow.pkl"
    )
    model_path = params.get("model_path", "/opt/airflow/models/model_airflow.pkl")
    model_type = params.get("model_type", "logistic")
    random_state = params.get("random_state", 42)
    logistic_default_params = {
        "penalty": "l2",
        "C": 1,
        "solver": "lbfgs",
        "max_iter": 100,
        "random_state": 42,
    }

    random_forest_default_params = {
        "n_estimators": 10,
        "max_depth": None,
        "random_state": 42,
        "n_jobs": -1,
    }

    decision_tree_default_params = {
        "criterion": "gini",
        "max_depth": 15,
        "random_state": 42,
        "min_samples_split": 2,
    }

    print(f"Loading processed data from {processed_data_path}...")
    with open(processed_data_path, "rb") as f:
        processed_data = pd.read_pickle(f)
    print("Processed data loaded successfully.")

    X_train, y_train = processed_data["X_train"], processed_data["y_train"]

    model_classes = {
        "logistic": (LogisticRegression, params.get("logistic_params", logistic_default_params)),
        "random_forest": (
            RandomForestClassifier,
            params.get("random_forest_params", random_forest_default_params),
        ),
        "decision_tree": (
            DecisionTreeClassifier,
            params.get("decision_tree_params", decision_tree_default_params),
        ),
    }

    if model_type not in model_classes:
        raise ValueError(f"Unknown model type: {model_type}")

    model_class, model_params = model_classes[model_type]
    print(f"Initializing the {model_type.capitalize()} model.")
    print(f"Parameters for model initialization: {model_params}")

    common_params = {"random_state": random_state}
    model = model_class(**{**common_params, **model_params})

    model.fit(X_train, y_train)
    print(f"{model_type.capitalize()} model fitting complete.")

    with open(model_path, "wb") as f:
        pd.to_pickle(model, f)
    print(f"Model saved to {model_path}.")


with DAG(
    "model_training_pipeline",
    description="A pipeline for model training and evaluation",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    params={
        "n_samples": 1000,
        "n_features": 20,
        "n_informative": 10,
        "n_redundant": 5,
        "n_classes": 2,
        "random_state": 42,
        "target_column": "target",
        "synthetic_data_path": "/opt/airflow/data/raw/dataset_airflow.csv",
        "processed_data_path": "/opt/airflow/data/processed/processed_data_airflow.pkl",
        "model_path": "/opt/airflow/models/model_airflow.pkl",
        "model_type": "logistic",
    },
) as dag:

    generate_data_task = PythonVirtualenvOperator(
        task_id="generate_data",
        python_callable=generate_data,
        op_args=[{"params": "{{ params }}"}],
        requirements=["scikit-learn", "pandas"],
        system_site_packages=False,
    )

    preprocess_data_task = PythonVirtualenvOperator(
        task_id="preprocess_data",
        python_callable=preprocess_data,
        op_args=[{"params": "{{ params }}"}],
        requirements=["scikit-learn", "pandas"],
        system_site_packages=False,
    )

    train_model_task = PythonVirtualenvOperator(
        task_id="train_model",
        python_callable=train_model,
        op_args=[{"params": "{{ params }}"}],
        requirements=["scikit-learn", "pandas"],
        system_site_packages=False,
    )

    generate_data_task >> preprocess_data_task >> train_model_task
