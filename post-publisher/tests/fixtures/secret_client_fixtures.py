from typing import Generator

from unittest.mock import patch
import pytest
from azure.keyvault.secrets import SecretClient, KeyVaultSecret

from config import get_config


def get_secret_side_effect(name):
    """
    Define some test values for the Key Vault secrets.
    """
    if name == "instagram-account-id":
        return KeyVaultSecret(properties=None, value="test-account-id")
    elif name == "instagram-access-token":
        return KeyVaultSecret(properties=None, value="test-access-token")
    return KeyVaultSecret(properties=None, value="default-value")


@pytest.fixture
def mock_key_vault_client() -> Generator[SecretClient, None, None]:
    """
    Mock the Instagram Graph API client instance.
    """
    with patch.object(SecretClient, '__init__', return_value=None), \
        patch.object(SecretClient, 'get_secret', side_effect=get_secret_side_effect):
        mock_instance = SecretClient(
            vault_url=get_config().KEYVAULT_URL,
            credential=None
        )
        yield mock_instance
