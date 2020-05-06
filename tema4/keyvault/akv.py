from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.common.credentials import ServicePrincipalCredentials

# OS ENVIRONMENT VARS
import os
os.environ["AZURE_CLIENT_ID"] = 'cec1d0e8-3a44-4b6d-a591-02e9c96eabbd'
os.environ["AZURE_CLIENT_SECRET"] = 'PX/2A0H/8r/jA4X@.PnLmrzCG:o9hdh/'
os.environ["AZURE_TENANT_ID"] = '4c804d9f-8c15-41be-9504-540e6a69a87f'
#


credentials = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://petify-vault.vault.azure.net/", credential=credentials)


# Storage key
def get_storage_secret():
    return secret_client.get_secret('storage-secret').value


# DB key
def get_db_secret():
    masterKey = secret_client.get_secret('db-mk-secret').value
    resourceTokens = secret_client.get_secret('db-rt-secret').value
    return {"masterKey": masterKey, "resourceTokens": resourceTokens}


if __name__ == '__main__':
    print(get_storage_secret())
    print(get_db_secret())
