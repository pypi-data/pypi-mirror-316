from unittest.mock import Mock, patch

import pytest
import requests

from src.iplens.db_cache import DBCache
from src.iplens.ipapi_api import IPInfoAPI
from src.iplens.utils import FIELDNAMES


@pytest.fixture
def mock_db_cache():
    return Mock(spec=DBCache)


@pytest.fixture
def ip_info_api(mock_db_cache):
    with patch("src.iplens.ipapi_api.DBCache", return_value=mock_db_cache):
        return IPInfoAPI()


@pytest.fixture
def sample_ip_data():
    return {
        "ip": "172.71.223.44",
        "rir": "ARIN",
        "company_name": "Cloudflare, Inc.",
        "asn_asn": "13335",
        "location_country": "United States",
    }


def test_fetch_data_cached(ip_info_api, mock_db_cache, sample_ip_data):

    mock_db_cache.get.return_value = sample_ip_data

    result = ip_info_api.fetch_data(["172.71.223.44"])

    assert result[0]["ip"] == sample_ip_data["ip"]
    assert result[0]["rir"] == sample_ip_data["rir"]

    print(f"mock_db_cache.get.call_count: {mock_db_cache.get.call_count}")
    mock_db_cache.get.assert_called_once_with("172.71.223.44")


@patch("src.iplens.ipapi_api.requests.get")
def test_fetch_data_single_ip(mock_get, ip_info_api, mock_db_cache, sample_ip_data):
    mock_db_cache.get.return_value = None
    mock_get.return_value.json.return_value = sample_ip_data
    mock_get.return_value.ok = True

    result = ip_info_api.fetch_data(["172.71.223.44"])

    expected_result = {
        "ip": "172.71.223.44",
        "rir": "ARIN",
        "company_name": "Cloudflare, Inc.",
        "asn_asn": "AS13335",
        "location_country": "United States",
        "company_abuser_score": "",
        "asn_abuser_score": "",
        "is_bogon": "",
        "is_datacenter": "",
        "is_tor": "",
        "is_proxy": "",
        "is_vpn": "",
        "is_abuser": "",
        "company_domain": "",
        "company_network": "",
        "company_whois": "",
        "asn_route": "",
        "asn_descr": "",
        "asn_country": "",
        "asn_active": "",
        "asn_org": "",
        "asn_domain": "",
        "asn_abuse": "",
        "asn_type": "",
        "asn_created": "",
        "asn_updated": "",
        "asn_rir": "",
        "asn_whois": "",
        "location_country_code": "",
        "location_state": "",
        "location_city": "",
        "location_latitude": "",
        "location_longitude": "",
        "location_zip": "",
        "location_timezone": "",
    }

    filtered_result = {key: result[0].get(key, "") for key in expected_result.keys()}

    assert filtered_result == expected_result
    mock_get.assert_called_once_with(f"{ip_info_api.api_url}?q=172.71.223.44")
    mock_db_cache.set.assert_called_once()


@patch("src.iplens.ipapi_api.requests.post")
def test_fetch_data_bulk(mock_post, ip_info_api, mock_db_cache):
    mock_db_cache.get.return_value = None
    mock_post.return_value.json.return_value = {
        "172.71.223.44": {"ip": "172.71.223.44", "rir": "ARIN"},
        "8.8.8.8": {"ip": "8.8.8.8", "rir": "ARIN"},
        "total_elapsed_ms": 100,
    }
    mock_post.return_value.ok = True

    result = ip_info_api.fetch_data(["172.71.223.44", "8.8.8.8"])

    assert len(result) == 2
    assert all(ip_data["rir"] == "ARIN" for ip_data in result)
    mock_post.assert_called_once_with(
        ip_info_api.api_url, json={"ips": ["172.71.223.44", "8.8.8.8"]}
    )
    assert mock_db_cache.set.call_count == 2

    filtered_result = [{k: v for k, v in ip_data.items() if v} for ip_data in result]

    for ip_data in filtered_result:
        assert set(ip_data.keys()) == {"ip", "rir"}
        assert ip_data["ip"] in ["172.71.223.44", "8.8.8.8"]
        assert ip_data["rir"] == "ARIN"


def test_process_response(ip_info_api, sample_ip_data):
    processed_data = ip_info_api.process_response(sample_ip_data)

    assert processed_data["ip"] == "172.71.223.44"
    assert processed_data["rir"] == "ARIN"
    assert processed_data["company_name"] == "Cloudflare, Inc."
    assert processed_data["asn_asn"] == "AS13335"
    assert processed_data["location_country"] == "United States"


@patch("src.iplens.ipapi_api.requests.get")
def test_fetch_single_ip_info_error(mock_get, ip_info_api):
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "404 Client Error: Not Found"
    )

    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError) as exc_info:
        ip_info_api._fetch_single_ip_info("172.71.223.44")

    assert "404 Client Error: Not Found" in str(exc_info.value)
    mock_get.assert_called_once_with(f"{ip_info_api.api_url}?q=172.71.223.44")


@patch("src.iplens.ipapi_api.requests.post")
def test_fetch_ip_info_error(mock_post, ip_info_api):
    mock_post.return_value.ok = False
    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "Internal Server Error"
    mock_post.return_value.raise_for_status.side_effect = requests.HTTPError(
        "500 Server Error: Internal Server Error"
    )

    with pytest.raises(requests.HTTPError):
        ip_info_api._fetch_ip_info(["172.71.223.44", "8.8.8.8"])


def test_clear_expired_cache(ip_info_api, mock_db_cache):
    ip_info_api.clear_expired_cache()
    mock_db_cache.clear_expired.assert_called_once()


def test_process_response_with_none_values(ip_info_api):
    # Test data with None values in nested fields
    sample_data_with_none = {
        "ip": "172.71.223.44",
        "asn": None,  # This caused the original error
        "location": None,
        "company": None,
    }

    processed_data = ip_info_api.process_response(sample_data_with_none)

    # Verify that all fields are present with empty strings
    assert processed_data["ip"] == "172.71.223.44"
    assert processed_data["asn_asn"] == ""
    assert processed_data["rir"] == ""
    assert processed_data["location_country"] == ""
    assert processed_data["company_name"] == ""
    assert all(processed_data[field] == "" for field in processed_data if field != "ip")


def test_process_response_with_invalid_nested_structure(ip_info_api):
    # Test data with invalid nested structure
    sample_data_invalid = {
        "ip": "172.71.223.44",
        "asn": "AS12345",  # Not a dict as expected
        "location": "US",  # Not a dict as expected
        "company": True,  # Not a dict as expected
    }

    processed_data = ip_info_api.process_response(sample_data_invalid)

    # Verify that the processing handles invalid nested structures
    assert processed_data["ip"] == "172.71.223.44"
    assert processed_data["asn_asn"] == ""
    assert processed_data["location_country"] == ""
    assert processed_data["company_name"] == ""


def test_process_response_completely_none(ip_info_api):
    # Test with None response
    processed_data = ip_info_api.process_response(None)

    # Verify that all fields are present with empty strings
    assert all(isinstance(v, str) for v in processed_data.values())
    assert all(v == "" for v in processed_data.values())
    assert set(processed_data.keys()) == set(FIELDNAMES)


@patch("src.iplens.ipapi_api.requests.post")
@patch("time.sleep")  # Mock sleep to speed up tests
def test_fetch_data_rate_limit_handling(
    mock_sleep, mock_post, ip_info_api, mock_db_cache
):
    """Test that the API properly handles rate limits with large batches."""
    # Generate 1200 IPs to trigger rate limit pause
    test_ips = [f"192.168.1.{i}" for i in range(1, 1201)]

    # Mock cache to return None for all IPs
    mock_db_cache.get.return_value = None

    # Mock successful API response
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        ip: {"ip": ip, "rir": "TEST"} for ip in test_ips[:100]
    }
    mock_post.return_value.json.return_value["total_elapsed_ms"] = 100

    # Process IPs
    ip_info_api.fetch_data(test_ips)

    # Verify that sleep was called after processing 1000 IPs
    mock_sleep.assert_any_call(60)  # Check for the 60-second pause

    # Verify that API calls were made in chunks of 100
    assert mock_post.call_count == len(test_ips) // 100 + (
        1 if len(test_ips) % 100 else 0
    )


@patch("src.iplens.ipapi_api.requests.post")
def test_fetch_data_cache_priority(mock_post, ip_info_api, mock_db_cache):
    """Test that cached IPs are returned immediately without API calls."""
    test_ips = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
    cached_data = {"ip": "192.168.1.1", "rir": "CACHED"}

    # Mock cache to return data for first IP only
    def mock_cache_get(ip):
        return cached_data if ip == "192.168.1.1" else None

    mock_db_cache.get.side_effect = mock_cache_get

    # Mock API response for uncached IPs
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        "192.168.1.2": {"ip": "192.168.1.2", "rir": "API"},
        "192.168.1.3": {"ip": "192.168.1.3", "rir": "API"},
        "total_elapsed_ms": 100,
    }

    results = ip_info_api.fetch_data(test_ips)

    # Verify cache was checked for all IPs
    assert mock_db_cache.get.call_count == len(test_ips)

    # Verify API was only called for uncached IPs
    mock_post.assert_called_once()
    assert len(mock_post.call_args[1]["json"]["ips"]) == 2

    # Verify results contain both cached and API data
    assert len(results) == 3
    assert any(r.get("rir") == "CACHED" for r in results)
    assert sum(1 for r in results if r.get("rir") == "API") == 2


@patch("src.iplens.ipapi_api.requests.post")
def test_fetch_data_chunk_size(mock_post, ip_info_api, mock_db_cache):
    """Test that API requests are made in correct chunk sizes."""
    # Generate 250 IPs to test chunking
    test_ips = [f"192.168.1.{i}" for i in range(1, 251)]

    # Mock cache to return None for all IPs
    mock_db_cache.get.return_value = None

    # Mock successful API response
    mock_post.return_value.ok = True

    def mock_response(ips):
        return {ip: {"ip": ip, "rir": "TEST"} for ip in ips["ips"]}

    mock_post.return_value.json.side_effect = lambda: {
        **mock_response(mock_post.call_args[1]["json"]),
        "total_elapsed_ms": 100,
    }

    ip_info_api.fetch_data(test_ips)

    # Verify that each API call contained no more than 100 IPs
    for call in mock_post.call_args_list:
        assert len(call[1]["json"]["ips"]) <= 100

    # Verify total number of API calls
    expected_calls = len(test_ips) // 100 + (1 if len(test_ips) % 100 else 0)
    assert mock_post.call_count == expected_calls
