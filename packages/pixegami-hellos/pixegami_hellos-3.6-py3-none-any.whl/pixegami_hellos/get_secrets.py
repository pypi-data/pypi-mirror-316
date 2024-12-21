# import boto3
# import json
# from botocore.exceptions import ClientError

# def get_secret(secret_name, region_name="us-east-1"):
#     """
#     Retrieve secrets from AWS Secrets Manager.

#     Args:
#         secret_name (str): Name of the secret to retrieve.
#         region_name (str): AWS region where the secret is stored.

#     Returns:
#         dict: The secret key-value pairs as a dictionary.

#     Raises:
#         ClientError: If AWS Secrets Manager fails to retrieve the secret.
#     """
#     session = boto3.session.Session()
#     client = session.client(service_name='secretsmanager', region_name=region_name)

#     try:
#         get_secret_value_response = client.get_secret_value(SecretId=secret_name)
#     except ClientError as e:
#         raise e

#     secret = get_secret_value_response.get('SecretString')
#     if secret:
#         return json.loads(secret)
#     else:
#         raise ValueError("SecretString is missing in the secret value response.")


# CREDS = get_secret("camdb_updates")
# AWS_CREDS = get_secret("SecondaryPayer")
# AZR_CREDS = get_secret("utilities_azure")
# python3 setup.py bdist_wheel  
# python3 -m pixegami_hellos/app.py                                                                
