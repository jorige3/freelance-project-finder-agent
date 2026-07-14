import pytest
from unittest.mock import patch, AsyncMock
from app.collectors.remoteok import RemoteOKCollector
from app.collectors.remotive import RemotiveCollector
from app.collectors.weworkremotely import WeWorkRemotelyCollector

@pytest.fixture
def anyio_backend():
    return "asyncio"

class MockResponse:
    def __init__(self, json_data, content=b"", status_code=200):
        self._json = json_data
        self.content = content
        self.status_code = status_code
        
    def json(self):
        return self._json
        
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

@pytest.mark.anyio
async def test_remoteok_collector(anyio_backend):
    mock_data = [
        {"position": "Python Developer", "company": "Company A", "url": "https://example.com/1", "tags": ["python", "api"]},
        {"position": "React Developer", "company": "Company B", "url": "https://example.com/2"}
    ]
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MockResponse(mock_data)
        collector = RemoteOKCollector()
        projects = await collector.collect()
        assert len(projects) == 2
        assert projects[0].title == "Python Developer"
        assert projects[0].platform == "RemoteOK"

@pytest.mark.anyio
async def test_remotive_collector(anyio_backend):
    mock_data = {
        "jobs": [
            {"title": "FastAPI Eng", "url": "https://example.com/3", "tags": ["fastapi"], "salary": "$100k", "description": "Backend"}
        ]
    }
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MockResponse(mock_data)
        collector = RemotiveCollector()
        projects = await collector.collect()
        assert len(projects) == 1
        assert projects[0].title == "FastAPI Eng"
        assert projects[0].platform == "Remotive"

@pytest.mark.anyio
async def test_weworkremotely_collector(anyio_backend):
    mock_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <item>
          <title>Python Developer</title>
          <link>https://weworkremotely.com/jobs/1</link>
          <description>Build Django apps</description>
        </item>
      </channel>
    </rss>
    """
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MockResponse({}, content=mock_xml)
        collector = WeWorkRemotelyCollector()
        projects = await collector.collect()
        assert len(projects) == 1
        assert projects[0].title == "Python Developer"
        assert projects[0].platform == "WeWorkRemotely"
