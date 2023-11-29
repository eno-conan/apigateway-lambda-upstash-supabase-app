import base64

import boto3
from botocore.exceptions import ClientError


def read_value(name: str) -> str:
    """Get secret value From SecretManager."""
    secret_name = name
    region_name = "ap-northeast-1"

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name,
        )
        if "SecretString" in get_secret_value_response:
            secret_data = get_secret_value_response["SecretString"]
            return secret_data
        else:
            decoded_binary_secret = base64.b64decode(
                get_secret_value_response["SecretBinary"]
            )  # noqa: F841
    except ClientError as e:
        raise e
