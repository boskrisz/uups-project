import os
import csv

from dotenv import load_dotenv

from app.models.image_meta import ImageMeta


class Config:
    """
    Configuration class for the application.
    """
    def __init__(self):
        # Load the environment variables from the .env file
        self.set_env_variables()
        # Set folder and file paths
        self.set_asset_paths()
        self.set_export_root()
        self.set_export_paths()
        # Create the directories and files for storing the generated images
        self.create_asset_directories()
        self.create_image_meta_file()


    def set_env_variables(self):
        """
        Set the environment variables for the application.
        """
        load_dotenv(os.path.join('app', 'config', '.env'))
        self.OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        self.OPENAI_MODEL = os.environ['OPENAI_MODEL']


    def set_asset_paths(self):
        """
        Set the paths for the directories and files used for the image generation.
        """
        self.PROJECT_ASSETS_DIR = os.path.join(os.getcwd(), 'app', 'assets')
        self.BACKGROUND_DIR = os.path.join(self.PROJECT_ASSETS_DIR, 'backgrounds')
        self.FONT_DIR = os.path.join(self.PROJECT_ASSETS_DIR, 'fonts')
        self.BACKGROUND_YELLOW = os.path.join(self.BACKGROUND_DIR, 'background_yellow.png')
        self.BACKGROUND_PINK = os.path.join(self.BACKGROUND_DIR, 'background_pink.png')
        self.BACKGROUND_PURPLE = os.path.join(self.BACKGROUND_DIR, 'background_purple.png')
        self.QUOTE_FONT_BARRIO = os.path.join(self.FONT_DIR, 'Barrio-Regular.ttf')
        self.QUOTE_FONT_MODAK = os.path.join(self.FONT_DIR, 'Modak-Regular.ttf')
        self.QUOTE_FONT_RUBIK = os.path.join(self.FONT_DIR, 'RubikDirt-Regular.ttf')


    def set_export_root(self):
        """
        Set the root directory for the generated assets.
        """
        # Generated assets are saved outside the app directory to be shared with the post-migrator
        self.GENERATED_ASSETS_DIR = os.path.join(os.path.dirname(os.getcwd()), 'generated_assets')


    def set_export_paths(self):
        """
        Set the paths for the directories and files used for the generated images 
        and their metadata.
        """
        self.BASE_IMAGE_DIR = os.path.join(self.GENERATED_ASSETS_DIR, 'base_images')
        self.APPROVED_IMAGE_DIR = os.path.join(self.GENERATED_ASSETS_DIR, 'approved_images')
        self.REJECTED_IMAGE_DIR = os.path.join(self.GENERATED_ASSETS_DIR, 'rejected_images')
        self.PROCESSED_IMAGE_DIR = os.path.join(self.GENERATED_ASSETS_DIR, 'processed_images')
        self.IMAGE_META_FILE = os.path.join(self.GENERATED_ASSETS_DIR, 'images_meta.csv')


    def create_asset_directories(self):
        """
        Create the directories for storing and managing the generated images.
        """
        try:
            os.makedirs(self.GENERATED_ASSETS_DIR, exist_ok=True)
            os.makedirs(self.BASE_IMAGE_DIR, exist_ok=True)
            os.makedirs(self.APPROVED_IMAGE_DIR, exist_ok=True)
            os.makedirs(self.REJECTED_IMAGE_DIR, exist_ok=True)
            os.makedirs(self.PROCESSED_IMAGE_DIR, exist_ok=True)
        except FileExistsError as e:
            # Probably errno 17: File exists
            # This usually happens when you delete the directories on the host machine
            # while the DevContainer is still running.
            # In this case, just restart/rebuild the DevContainer and try again.
            raise FileExistsError("Failed to create directories for \
                storing the generated images.") from e


    def create_image_meta_file(self):
        """
        Create the CSV file for storing the metadata of the generated images.
        """
        # Create the meta file if it doesn't exist
        if not os.path.exists(self.IMAGE_META_FILE):
            headers = ImageMeta.get_field_names()

            with open(self.IMAGE_META_FILE, 'w', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(headers)


class TestConfig(Config):
    """
    Configuration class for the application during automated testing.
    """
    def set_export_root(self):
        # Override the generated assets directory to avoid data corruption
        self.GENERATED_ASSETS_DIR = os.path.join(os.getcwd(), 'test_generated_assets')


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
