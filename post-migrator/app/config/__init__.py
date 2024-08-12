import csv
import os
from dotenv import load_dotenv

from app.models.image_meta import ImageMeta


class Config:
    """
    Configuration class for the application.
    """
    def __init__(self):
        # Load the environment variables from the .env file
        self.load_env_variables()
        self.set_env_variables()
        # Set folder and file paths used in the application
        self.set_generated_images_root_dir()
        self.set_generated_image_paths()
        # Create the required directories if they don't exist
        self.create_asset_directories()


    def load_env_variables(self):
        """
        Load the environment variables from the .env file.
        """
        load_dotenv(os.path.join('app', 'config', '.env'))


    def set_env_variables(self):
        """
        Set the environment variables for the application
        """
        # Azure Storage Account credentials
        self.STORAGE_ACCOUNT_URL = os.environ['STORAGE_ACCOUNT_URL']
        self.STORAGE_CONTAINER_NAME = os.environ['STORAGE_CONTAINER_NAME']
        self.STORAGE_CONTAINER_SAS = os.environ['STORAGE_CONTAINER_SAS']
        # Azure Cosmos DB credentials
        self.COSMOSDB_ACCOUNT_URL = os.environ['COSMOSDB_ACCOUNT_URL']
        self.COSMOSDB_ACCOUNT_KEY = os.environ['COSMOSDB_ACCOUNT_KEY']
        self.COSMOSDB_DATABASE_NAME = os.environ['COSMOSDB_DATABASE_NAME']
        self.COSMOSDB_CONTAINER_NAME = os.environ['COSMOSDB_CONTAINER_NAME']


    def set_generated_images_root_dir(self):
        """
        Set the root directory for the generated assets.
        """
        # Generated assets are saved outside the app directory as shared with the post-producer
        self.GENERATED_ASSETS_DIR = os.path.join(os.path.dirname(os.getcwd()), 'generated_assets')


    def set_generated_image_paths(self):
        """
        Set the paths for the generated images and metadata files.
        """
        self.APPROVED_IMAGE_DIR = os.path.join(self.GENERATED_ASSETS_DIR, 'approved_images')
        self.PROCESSED_IMAGE_DIR = os.path.join(self.GENERATED_ASSETS_DIR, 'processed_images')
        self.IMAGE_META_FILE = os.path.join(self.GENERATED_ASSETS_DIR, 'images_meta.csv')


    def create_asset_directories(self):
        """
        Create the directories where the generated images are stored.
        """
        try:
            os.makedirs(self.GENERATED_ASSETS_DIR, exist_ok=True)
            os.makedirs(self.APPROVED_IMAGE_DIR, exist_ok=True)
            os.makedirs(self.PROCESSED_IMAGE_DIR, exist_ok=True)
        except FileExistsError as e:
            # Probably errno 17: File exists
            # This usually happens when you delete the directories on the host machine
            # while the DevContainer is still running.
            # In this case, just restart/rebuild the DevContainer and try again.
            raise FileExistsError("Failed to create directories for \
                storing the generated images.") from e


class TestConfig(Config):
    """
    Configuration class for the test environment.
    """
    def __init__(self):
        super().__init__()
        # Create test files necessary for the automated tests
        self.create_test_files()


    def load_env_variables(self):
        """
        Load the environment variables from the .env.test file.
        """
        load_dotenv(os.path.join('app', 'config', '.env.test'))


    def set_env_variables(self):
        """
        Set the test environment variables for the application
        """
        # Azure Storage Account credentials
        self.STORAGE_ACCOUNT_URL = os.environ['TEST_STORAGE_ACCOUNT_URL']
        self.STORAGE_CONTAINER_NAME = os.environ['TEST_STORAGE_CONTAINER_NAME']
        self.STORAGE_CONTAINER_SAS = os.environ['TEST_STORAGE_CONTAINER_SAS']
        # Azure Cosmos DB credentials
        self.COSMOSDB_ACCOUNT_URL = os.environ['TEST_COSMOSDB_ACCOUNT_URL']
        self.COSMOSDB_ACCOUNT_KEY = os.environ['TEST_COSMOSDB_ACCOUNT_KEY']
        self.COSMOSDB_DATABASE_NAME = os.environ['TEST_COSMOSDB_DATABASE_NAME']
        self.COSMOSDB_CONTAINER_NAME = os.environ['TEST_COSMOSDB_CONTAINER_NAME']


    def set_generated_images_root_dir(self):
        """
        Overwrites setting the root directory for the generated test assets.
        """
        self.GENERATED_ASSETS_DIR = os.path.join(os.getcwd(), 'test_generated_assets')


    def create_test_files(self):
        """
        Create the test files for the automated tests.
        """
        # Create the images meta file if it doesn't exist
        if not os.path.exists(self.IMAGE_META_FILE):
            headers = ImageMeta.get_field_names()

            with open(self.IMAGE_META_FILE, 'w', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(headers)


# Initialize the Config class as a global variable
config = None

def init_config(env='test'):
    global config
    if env == 'test':
        config = TestConfig()
    elif env == 'prod':
        config = Config()
    else:
        raise ValueError("Invalid environment specified. Use 'test' or 'prod'.")

def get_config():
    return config
