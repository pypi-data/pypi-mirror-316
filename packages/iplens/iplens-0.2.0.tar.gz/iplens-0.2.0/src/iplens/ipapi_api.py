import logging
import time
from typing import Any, Dict, List

import requests
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)

from iplens.base_operations import IPInfoOperation
from iplens.config_loader import load_config
from iplens.db_cache import DBCache
from iplens.logger import logger
from iplens.utils import FIELDNAMES


class IPInfoAPI(IPInfoOperation):
    def __init__(self):
        """
        Initialize the IPInfoAPI class with API URL and backoff factor loaded from the configuration file.
        The class also initializes the cache for storing IP information.
        """
        config = load_config()
        api_url = config.get("API", "url")
        backoff_factor = int(config.get("API", "backoff_factor"))
        super().__init__(api_url, backoff_factor)
        self.cache = DBCache()

    def fetch_data(
        self, ips: List[str], chunk_size: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Fetch data for a list of IP addresses. Cached IPs are processed immediately,
        while non-cached IPs are processed in batches with rate limit handling.

        Args:
            ips (List[str]): List of IP addresses to fetch data for.
            chunk_size (int): Maximum number of IPs to fetch in each bulk request.
        """
        response_data_list = []
        ips_to_fetch = []
        fetched_from_cache = 0
        fetched_from_api = 0
        failed_requests = 0

        logger.info(f"Starting to process {len(ips)} IP address(es)...")

        # First pass - check cache
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            cache_task = progress.add_task("Checking cache...", total=len(ips))

            for ip in ips:
                cached_data = self.cache.get(ip)
                if cached_data:
                    response_data_list.append(cached_data)
                    fetched_from_cache += 1
                else:
                    ips_to_fetch.append(ip)
                progress.update(cache_task, advance=1)

        if not ips_to_fetch:
            return response_data_list

        # Process non-cached IPs in batches
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            api_task = progress.add_task(
                f"Fetching {len(ips_to_fetch)} uncached IPs from API...",
                total=len(ips_to_fetch),
            )

            # Process in chunks of 100 for API limitations
            api_chunk_size = 100
            for i in range(0, len(ips_to_fetch), api_chunk_size):
                ip_chunk = ips_to_fetch[i : i + api_chunk_size]

                # If we've processed 1000 or more IPs, pause for a minute
                if i > 0 and i % 1000 == 0:
                    progress.update(
                        api_task,
                        description="API rate limit reached - Pausing for 60 seconds...",
                    )
                    time.sleep(60)
                    progress.update(
                        api_task,
                        description=f"Fetching {len(ips_to_fetch)} uncached IPs from API...",
                    )

                try:
                    if len(ip_chunk) < 2:
                        for ip in ip_chunk:
                            response_data = self._fetch_single_ip_info(ip)
                            processed_data = self.process_response(response_data)
                            response_data_list.append(processed_data)
                            self.cache.set(ip, processed_data)
                            fetched_from_api += 1
                            progress.update(api_task, advance=1)
                    else:
                        response_data = self._fetch_ip_info(ip_chunk)
                        for ip, ip_data in response_data.items():
                            if ip != "total_elapsed_ms":
                                processed_data = self.process_response(ip_data)
                                response_data_list.append(processed_data)
                                self.cache.set(ip, processed_data)
                                fetched_from_api += 1
                                progress.update(api_task, advance=1)

                    time.sleep(self.backoff_factor)
                except requests.HTTPError as e:
                    logger.error(f"Error during bulk request: {e}")
                    logger.error(f"Response content: {e.response.text}")
                    failed_requests += len(ip_chunk)
                    progress.update(api_task, advance=len(ip_chunk))

        if logger.isEnabledFor(logging.WARNING):
            logger.warning(
                f"Summary: {fetched_from_cache} IP(s) from cache, "
                f"{fetched_from_api} IP(s) from API, "
                f"{failed_requests} failed requests."
            )

        return response_data_list

    def _fetch_ip_info(self, ips: List[str]) -> Dict:
        """
        Fetch information for a list of IP addresses in bulk.

        Args:
            ips (List[str]): List of IP addresses to fetch data for.

        Returns:
            Dict: A dictionary with IP addresses as keys and their corresponding data as values.
        """
        logger.info(f"Making bulk request for {len(ips)} IP(s)")
        ips_dict = {"ips": ips}
        response = requests.post(self.api_url, json=ips_dict)
        if not response.ok:
            logger.error(f"Bulk request failed with status code {response.status_code}")
            logger.error(f"Response content: {response.text}")
            response.raise_for_status()
        logger.info("Bulk request successful")
        return response.json()

    def _fetch_single_ip_info(self, ip: str) -> Dict:
        """
        Fetch information for a single IP address.

        Args:
            ip (str): The IP address to fetch data for.

        Returns:
            Dict: A dictionary containing the data for the IP address.
        """
        logger.info(f"Making single request for IP: {ip}")
        response = requests.get(f"{self.api_url}?q={ip}")
        if not response.ok:
            logger.error(
                f"Single request failed for IP {ip} with status code {response.status_code}"
            )
            logger.error(f"Response content: {response.text}")
            response.raise_for_status()
        logger.info(f"Single request successful for IP: {ip}")
        return response.json()

    def process_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the response data from the API, extracting and formatting the relevant fields.

        Args:
            response (Dict[str, Any]): The API response for a single IP address.

        Returns:
            Dict[str, Any]: A dictionary with the processed IP information.
        """
        if not response or not isinstance(response, dict):
            logger.warning(f"Invalid response received: {response}")
            return {field: "" for field in FIELDNAMES}

        data = {}
        for field in FIELDNAMES:
            try:
                parts = field.split("_")
                if len(parts) == 1:
                    value = response.get(field)
                else:
                    category, subfield = parts[0], "_".join(parts[1:])
                    category_data = response.get(category, {})
                    if not isinstance(category_data, dict):
                        value = response.get(field)
                    else:
                        value = category_data.get(subfield)
                        if value is None:
                            value = response.get(field)

                if value is not None:
                    if field == "asn_asn" and value and not str(value).startswith("AS"):
                        value = f"AS{value}"

                    if value is False:
                        value = "False"
                    elif value is True:
                        value = "True"
                    data[field] = str(value)
                else:
                    data[field] = ""
            except Exception as e:
                logger.error(f"Error processing field {field}: {str(e)}")
                data[field] = ""

        # Special handling for RIR field
        try:
            if (
                "rir" in FIELDNAMES
                and "asn" in response
                and isinstance(response["asn"], dict)
            ):
                data["rir"] = response["asn"].get("rir", "")
        except Exception as e:
            logger.error(f"Error processing RIR field: {str(e)}")
            data["rir"] = ""

        logger.debug(f"Processed response data: {data}")
        return data

    def clear_expired_cache(self):
        """
        Clear expired cache entries from the local cache.
        """
        logger.info("Clearing expired cache entries")
        self.cache.clear_expired()
