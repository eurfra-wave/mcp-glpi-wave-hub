"""Tests de configuración y cliente GLPI."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.config import Settings
from src.client import GLPIClient, GLPIAuthError


class TestSettings:
    """Tests de configuración."""

    def test_settings_loads_from_env(self, monkeypatch):
        monkeypatch.setenv("GLPI_URL", "http://test.glpi/apirest.php")
        monkeypatch.setenv("GLPI_APP_TOKEN", "test-app-token")
        monkeypatch.setenv("GLPI_USER_TOKEN", "test-user-token")
        monkeypatch.setenv("MCP_PORT", "9090")
        monkeypatch.setenv("GLPI_INTERNAL_HOST", "10.0.0.20")
        monkeypatch.setenv("HUB_INTERNAL_HOST", "10.0.0.10")
        monkeypatch.setenv("HERMES_AGENT_INTERNAL_HOST", "10.0.0.5")
        monkeypatch.setenv("PROXMOX_NETWORK_SUBNET", "10.0.0.0/24")

        settings = Settings()
        assert settings.glpi_url == "http://test.glpi/apirest.php"
        assert settings.glpi_app_token == "test-app-token"
        assert settings.glpi_user_token == "test-user-token"
        assert settings.mcp_port == 9090

    def test_settings_requires_glpi_url(self, monkeypatch):
        monkeypatch.delenv("GLPI_URL", raising=False)
        monkeypatch.delenv("GLPI_APP_TOKEN", raising=False)
        monkeypatch.delenv("GLPI_INTERNAL_HOST", raising=False)
        monkeypatch.delenv("HUB_INTERNAL_HOST", raising=False)
        monkeypatch.delenv("HERMES_AGENT_INTERNAL_HOST", raising=False)
        monkeypatch.delenv("PROXMOX_NETWORK_SUBNET", raising=False)

        with pytest.raises(Exception):
            Settings()


@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setenv("GLPI_URL", "http://test.glpi/apirest.php")
    monkeypatch.setenv("GLPI_APP_TOKEN", "test-app-token")
    monkeypatch.setenv("GLPI_USER_TOKEN", "test-user-token")
    monkeypatch.setenv("GLPI_INTERNAL_HOST", "10.0.0.20")
    monkeypatch.setenv("HUB_INTERNAL_HOST", "10.0.0.10")
    monkeypatch.setenv("HERMES_AGENT_INTERNAL_HOST", "10.0.0.5")
    monkeypatch.setenv("PROXMOX_NETWORK_SUBNET", "10.0.0.0/24")


@pytest.fixture
def client(mock_settings):
    return GLPIClient()


class TestGLPIClient:
    """Tests del cliente GLPI."""

    @pytest.mark.asyncio
    async def test_init_session_with_user_token(self, client):
        with patch.object(client._client, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"session_token": "test-session-token"}
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value = mock_response

            token = await client.init_session()

            assert token == "test-session-token"
            assert client._session_token == "test-session-token"
            mock_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_init_session_without_auth_raises(self, client):
        client.user_token = ""
        client.username = ""
        client.password = ""

        with pytest.raises(GLPIAuthError):
            await client.init_session()

    @pytest.mark.asyncio
    async def test_ensure_session_lazy_init(self, client):
        client._session_token = None

        with patch.object(client, "init_session", new_callable=AsyncMock) as mock_init:
            mock_init.return_value = "new-token"
            await client.ensure_session()
            mock_init.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_session_reuses_existing(self, client):
        client._session_token = "existing-token"

        with patch.object(client, "init_session", new_callable=AsyncMock) as mock_init:
            await client.ensure_session()
            mock_init.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_items_builds_params(self, client):
        client._session_token = "token"

        with patch.object(client._client, "request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = [{"id": 1}, {"id": 2}]
            mock_response.raise_for_status = MagicMock()
            mock_request.return_value = mock_response

            result = await client.get_items("Ticket", range_="0-9", order="ASC")

            assert len(result) == 2
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]["params"]["range"] == "0-9"
            assert call_args[1]["params"]["order"] == "ASC"

    @pytest.mark.asyncio
    async def test_session_refresh_on_401(self, client):
        client._session_token = "expired-token"

        with patch.object(client._client, "request") as mock_request:
            mock_401 = MagicMock()
            mock_401.raise_for_status.side_effect = Exception("401")
            mock_401.status_code = 401
            mock_401.text = "Unauthorized"

            mock_ok = MagicMock()
            mock_ok.json.return_value = [{"id": 3}]
            mock_ok.raise_for_status = MagicMock()

            import httpx
            error_401 = httpx.HTTPStatusError("401", request=MagicMock(), response=mock_401)
            mock_request.side_effect = [error_401, mock_ok]

            with patch.object(client, "init_session", new_callable=AsyncMock) as mock_init:
                mock_init.return_value = "new-token"
                result = await client.get_items("Ticket")
                assert result == [{"id": 3}]
                mock_init.assert_called_once()
