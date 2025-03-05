import requests
import config
from concurrent.futures import ThreadPoolExecutor

# Caching dictionaries to prevent redundant API calls
ip_cache = {}
business_cache = {}


def get_ip_location(ip_address):
    """Fetches geolocation details for a given IP address using ipinfo.com."""
    if ip_address in ip_cache:
        return ip_cache[ip_address]  # Return cached result

    try:
        response = requests.get(config.IPINFO_URL.format(ip=ip_address), timeout=config.API_TIMEOUT)
        data = response.json()

        result = {
            "ip_state": data.get("region", "Unknown"),
            "ip_country": data.get("country", "Unknown")
        }
        ip_cache[ip_address] = result  # Cache result
        return result
    except requests.RequestException:
        return {"ip_state": "Error", "ip_country": "Error"}

def fetch_ip_batch(ip_list):
    """Fetches multiple IP locations in parallel with dynamic threading."""
    max_workers = min(10, len(ip_list) or 1)  # Limit thread count
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(get_ip_location, ip_list))
    return results