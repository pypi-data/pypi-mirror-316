import pytest
from unittest.mock import Mock, patch
import json
from src.salesforce.server import SalesforceClient, server
import mcp.types as types

@pytest.fixture
def sf_client():
    with patch('src.salesforce.server.Salesforce') as mock_sf:
        client = SalesforceClient()
        # Mock successful connection
        mock_sf.return_value.mdapi.CustomObject.read.return_value = {"name": "Account"}
        yield client

@pytest.fixture
def mock_salesforce():
    with patch('src.salesforce.server.Salesforce') as mock_sf:
        yield mock_sf

def test_salesforce_client_connect_success(sf_client):
    assert sf_client.connect() == True

def test_salesforce_client_connect_failure(sf_client):
    with patch('src.salesforce.server.Salesforce', side_effect=Exception("Connection failed")):
        assert sf_client.connect() == False

def test_run_soql_query_success(sf_client):
    mock_records = [
        {"Id": "001", "Name": "Test Account"},
        {"Id": "002", "Name": "Test Account 2"}
    ]
    sf_client.sf = Mock()
    sf_client.sf.query_all.return_value = {"records": mock_records}
    
    results = sf_client.run_soql_query("SELECT Id, Name FROM Account")
    assert results == mock_records
    sf_client.sf.query_all.assert_called_once_with("SELECT Id, Name FROM Account")

def test_run_soql_query_no_connection(sf_client):
    sf_client.sf = None
    results = sf_client.run_soql_query("SELECT Id FROM Account")
    assert results == []

def test_run_sosl_search_success(sf_client):
    mock_records = [
        {"Id": "001", "Name": "Test Account"}
    ]
    sf_client.sf = Mock()
    sf_client.sf.search.return_value = {"searchRecords": mock_records}
    
    results = sf_client.run_sosl_search("FIND {Test}")
    assert results == mock_records
    sf_client.sf.search.assert_called_once_with("FIND {Test}")

@pytest.mark.asyncio
async def test_list_tools():
    tools = await server.list_tools()
    assert len(tools) == 2
    assert any(tool.name == "run_soql_query" for tool in tools)
    assert any(tool.name == "run_sosl_search" for tool in tools)

@pytest.mark.asyncio
async def test_call_tool_soql_query():
    with patch('src.salesforce.server.sf_client') as mock_client:
        mock_records = [{"Id": "001", "Name": "Test"}]
        mock_client.run_soql_query.return_value = mock_records
        
        result = await server.call_tool()("run_soql_query", {"query": "SELECT Id FROM Account"})
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert json.loads(result[0].text.split('\n', 1)[1]) == mock_records

@pytest.mark.asyncio
async def test_call_tool_invalid_name():
    with pytest.raises(ValueError, match="Unknown tool: invalid_tool"):
        await server.call_tool()("invalid_tool", {})

@pytest.mark.asyncio
async def test_call_tool_missing_arguments():
    with pytest.raises(ValueError, match="Missing 'query' argument"):
        await server.call_tool()("run_soql_query", {}) 