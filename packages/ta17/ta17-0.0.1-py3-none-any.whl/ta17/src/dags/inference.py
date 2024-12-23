import pendulum
from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
from airflow.sensors.filesystem import FileSensor


def load_and_predict(model_path, input_file, output_file, **kwargs):
    import os

    import pandas as pd

    with open(model_path, "rb") as f:
        model = pd.read_pickle(f)

    df = pd.read_csv(input_file)

    X_new = df.drop(columns=["target"])
    predictions = model.predict(X_new)
    df["predictions"] = predictions

    df.to_csv(output_file, index=False)

    if os.path.exists(input_file):
        os.remove(input_file)


with DAG(
    "batch_inference_pipeline",
    description="Batch inference pipeline for new data",
    schedule="@daily",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    params={
        "model_path": "/opt/airflow/models/model_airflow.pkl",
        "input_file_path": "/opt/airflow/data/external/new_data.csv",
        "output_file_path": "/opt/airflow/data/predictions/predictions.csv",
    },
) as dag:

    wait_for_new_data = FileSensor(
        task_id="wait_for_new_data",
        filepath="{{ params.input_file_path }}",
        poke_interval=10,
        timeout=600,
        mode="poke",
    )

    run_inference = PythonVirtualenvOperator(
        task_id="run_inference",
        python_callable=load_and_predict,
        op_args=[
            "{{ params.model_path }}",
            "{{ params.input_file_path }}",
            "{{ params.output_file_path }}",
        ],
        provide_context=True,
        requirements=["scikit-learn", "pandas"],
        system_site_packages=False,
    )

    wait_for_new_data >> run_inference
