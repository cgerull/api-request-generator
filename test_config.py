import pytest
import client
import config
from urllib.parse import urlparse

@pytest.fixture
def mock_env_server(monkeypatch):
    monkeypatch.setenv("SERVER", "my-server")

#
# Test configuration
def test_logger_name():
    assert client.config['logger_name'] != ''
    
def test_log_level():
    assert client.config['log_level'] != ''

def test_server(mock_env_server):
    a_config = config.load_environment(client.config)
    assert a_config['server'] == "my-server"

#
# Test logging
def test_init_logger():
    logger = client.init_logger()
    assert logger.name == client.config['logger_name']

#
# Test request
def test_send_api_request(httpserver):
    # set up the server to serve /api/echo with the json
    httpserver.expect_request("/").respond_with_json({"foo": "bar"})
    url = urlparse(httpserver.url_for("/"))
    print("url: {}, hostname: {}, port: {}, path: {}".format(url, url.hostname, url.port, url.path))
    # check that the request is served
    assert client.get_connection(server=url.hostname, port=url.port, srv_path=url.path)
    # assert requests.get(httpserver.url_for("/foobar")).json() == {'foo': 'bar'}