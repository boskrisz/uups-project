import pytest

from azure.identity import DefaultAzureCredential


@pytest.fixture
def azure_managed_identity() -> DefaultAzureCredential:
    """
    Initialize authentication depending on the executing environment.
    - When run locally, the developer must have the Azure CLI installed and logged in.
      Furthermore, the developer must have the necessary role assignments,
      to interact with the relevant test services on Azure.
    - When run via a GitHub runner during CI/CD, the runner's authenticates with Azure via OICD.
      For this a Service Principal with GitHub's Federated Credential must be created.
      This can be done in Microsoft Entra ID via an App Registration or in Azure via creating 
      a User Managed Identity, which have Federated Credentials assigned to them.
      Furthermore, the Identity must have the necessary permissions to interact 
      with the test services on Azure.

    The necessary permissions are as follows:
    - Storage Account permissions to read, write and delete blobs within containers.
    - Cosmos DB permissions to read, write and delete documents within containers.

    Using Role Based Access Control (RBAC) in Azure, the following roles can be assigned:
    - Storage Blob Data Contributor
    - Cosmos DB Built-in Data Contributor
    """
    return DefaultAzureCredential()
