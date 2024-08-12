import os

from dotenv import load_dotenv


class Config:
    """
    Config class that stores all the environment variables

    The environment variables are stored in the local.settings.json file.
    """
    def __init__(self):
        # Azure Storage Account credentials
        self.STORAGE_ACCOUNT_URL = os.environ['STORAGE_ACCOUNT_URL']
        self.STORAGE_CONTAINER_NAME = os.environ['STORAGE_CONTAINER_NAME']
        # Azure Cosmos DB credentials
        self.COSMOSDB_ACCOUNT_URL = os.environ['COSMOSDB_ACCOUNT_URL']
        self.COSMOSDB_DATABASE_NAME = os.environ['COSMOSDB_DATABASE_NAME']
        self.COSMOSDB_CONTAINER_NAME = os.environ['COSMOSDB_CONTAINER_NAME']
        # Azure Key Vault credentials
        self.KEYVAULT_URL = os.environ['KEYVAULT_URL']


class TestConfig:
    """
    Test Config class that stores dummy config variables for testing

    The environment variables are stored in the local.settings.json file.
    """
    def __init__(self):
        load_dotenv(os.path.join('config', '.env.test'))
        # Azure Storage Account credentials
        self.STORAGE_ACCOUNT_URL = os.environ['TEST_STORAGE_ACCOUNT_URL']
        self.STORAGE_CONTAINER_NAME = os.environ['TEST_STORAGE_CONTAINER_NAME']
        # Azure Cosmos DB credentials
        self.COSMOSDB_ACCOUNT_URL = os.environ['TEST_COSMOSDB_ACCOUNT_URL']
        self.COSMOSDB_DATABASE_NAME = os.environ['TEST_COSMOSDB_DATABASE_NAME']
        self.COSMOSDB_CONTAINER_NAME = os.environ['TEST_COSMOSDB_CONTAINER_NAME']
        # Azure Key Vault credentials
        self.KEYVAULT_URL = 'test_keyvault_url'


# Initialize the Config class as a global variable
config = None

def init_config(env: str = 'test'):
    global config
    if env == 'test':
        config = TestConfig()
    elif env == 'prod':
        config = Config()
    else:
        raise ValueError("Invalid environment specified. Use 'test' or 'prod'.")

    return config

def get_config():
    return config
