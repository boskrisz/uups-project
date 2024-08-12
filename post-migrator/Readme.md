# UUPS - Post Migrator
The "_UUPS - Post Migrator_" application is one of the service components of the UUPS project.

This application is used to migrate the generated assets of the "_Post Producer_" to the cloud, 
where the "_Post Publisher_" application can work with them.
It uploads the manually approved images and their metadata to an Azure Blob Storage and to a Cosmos DB Core (NoSQL) document storage.
Subsequently, these assets are picked up by the "_Post Publisher_" and are posted to the configured social media accounts. 
Therefore, this component serves as a hybrid bridge between the on-premise and the cloud native components.

## Usage
First, review the generated images of the "_Post Producer_" application.
- They are stored under the `uups_project/generated_assets/base_images` folder.
- Simply move the preferred images from the `/base_images` to the `/approved_images` directory.

Second, create the following required Azure Services, where the generated assets will be migrated to:
- Azure Storage Account with a Blob Container, where the images will be uploaded
- Azure Cosmos DB Core with a database and a container, where the images' metadata will be stored

Third, configure the environment variables in the ``post-migrator/config/.env`` file:
- `STORAGE_ACCOUNT_URL`: The URL of the Azure Storage Account
- `STORAGE_CONTAINER_NAME`: The name of the blob container inside the storage account
- `STORAGE_CONTAINER_SAS`: A generated Shared Access Signature for the granular access of the blob container
- `COSMOSDB_ACCOUNT_URL`: The URL of the Azure Cosmos DB account
- `COSMOSDB_ACCOUNT_KEY`: One of the read-write keys of the Cosmos DB account
- `COSMOSDB_DATABASE_NAME`: The name of the database inside the database account
- `COSMOSDB_CONTAINER_NAME`: The name of the container (data table) inside the database

Finally, running the application to migrate the assets can be done via at least the following ways:
- Docker
- Python Virtual Environment

**Docker**

Requirements:
- Docker

Build an image from the application and run it in a container with persistent storage mounted to the local `generated_assets` directory:
```bash
# from root dir: uups_project/
docker build -t [image_name] ./post-migrator
docker run -v $(pwd)/generated_assets:/generated_assets -e [image_name]
```
- `image_name`: The name of the Docker image to be built

**Python Virtual Environment**

Requirements:
- Python 3.x

Create a virtual environment to store the installed dependencies and run the application:
```bash
cd post-producer/

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

python3 -m app
```

## Continuous Integration
Whenever a new commit is pushed to the master branch, or a pull request is opened againts it, a GitHub Action's workflow is triggered to evaluate the changes by running the unit and integration tests. The workflow configuration can be found in the `.github/workflows/master_migrator.yml`.

In order to run this workflow, the following requirements must be met:
- TEST Storage and Cosmos DB Accounts need to be provisioned in Azure, mirroring the ones of the production environment
- In GitHub the following environment variables need to be added:
   - `TEST_COSMOSDB_ACCOUNT_KEY`: One of the read-write keys of the Cosmos DB account
   - `TEST_STORAGE_CONTAINER_SAS`: A generated Shared Access Signature for the granular access of the blob container
- In GitHub the following secrets need to be added:
   - `TEST_STORAGE_ACCOUNT_URL`: The URL of the Azure Storage Account
   - `TEST_STORAGE_CONTAINER_NAME`: The name of the blob container inside the storage account
   - `TEST_COSMOSDB_ACCOUNT_URL`: The URL of the Azure Cosmos DB account
   - `TEST_COSMOSDB_DATABASE_NAME`: The name of the database inside the database account
   - `TEST_COSMOSDB_CONTAINER_NAME`: The name of the container (data table) inside the database

## Development via DevContainers
Documentations about DevContainers:
- [Microsoft - Dev Containers: Getting Started](https://microsoft.github.io/code-with-engineering-playbook/developer-experience/devcontainers/)
- [GitHub - Introduction to dev containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)
- [Visual Studio Code - Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers)

**Requirements:**
- Docker installed and running on your OS
- VS Code and Dev Containers extension
- If you are using Windows, for more optimal execution run the application from WSL

**Development:**
1. Open VS Code (if you are on Windows, open it inside WSL for better performance)
2. Press ``Ctrl + Shift + P`` (or in the top search bar click on ``Show and Run Commands >``) and select the ``Dev Containers: Open Folder in Container`` option.
3. Select the ``post-producer`` folder.
4. For the first time, it will build the Dev Container with all of the dependencies needed for development. In subsequent starts, it will only update the dependencies if any changed.
   - You can also force re-building the Dev Container with selecting the ``Dev Containers: Rebuild Container``.
5. Modify any files, and run the application either via VS Code's ``Run and Debug`` or from its terminal via ``python -m app --image_num [num_images]``

**Testing:**
The integration tests rely on a TEST Azure environment that mirrors the Blob Storage and the Cosmos DB document store of the production environment. Therefore, before running the tests, make sure to provision a test environment and insert their credentials into the `app/config/.env.test` file.

Inside the DevContainer you can run the tests via either:
- VS Code's Test Suite
- or via executing the following command from VS Code's Terminal: `pytest tests/`

**Some considerations:**

- In the case you receive a ``gpg: keyserver receive failed: Server indicated a failure``, then simply disable the VPN.
- If Git would mark all files are modified, while nothing seems to be changed, then run: ``git config --global core.autocrlf true``
- If you receive an ``Error response from daemon: removal of container [...] is already in progress``, then simply try opening the Dev Container again while making sure that it is not running in Docker.
