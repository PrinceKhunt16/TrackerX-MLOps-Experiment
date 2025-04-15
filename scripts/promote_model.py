import os
import mlflow

def promote_model():
    dagshub_token = os.getenv("CAPSTONE_TEST")
    
    if not dagshub_token:
        raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = "princekhunt"
    repo_name = "TrackerX-MLOps-Experiment"

    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    client = mlflow.MlflowClient()
    model_name = "tx_model"
    latest_version_staging = client.get_latest_versions(model_name, stages=["Staging"])[0].version
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    
    for version in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage="Archived"
        )

    client.transition_model_version_stage(
        name=model_name,
        version=latest_version_staging,
        stage="Production"
    )
    
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    promote_model()