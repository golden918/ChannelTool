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


def verify_business_address(address):
    """Checks if the business address is valid using Google Places API."""
    if address in business_cache:
        return business_cache[address]  # Return cached result

    params = {
        "input": address,
        "inputtype": "textquery",
        "key": config.GOOGLE_PLACES_API_KEY
    }

    try:
        response = requests.get(config.GOOGLE_PLACES_URL, params=params, timeout=config.API_TIMEOUT)
        data = response.json()

        result = 1 if data.get("status") == "OK" and data.get("candidates") else 0  # 1 = Business Exists, 0 = Not Found
        business_cache[address] = result  # Cache result
        return result
    except requests.RequestException:
        return -1  # API Error


def fetch_ip_batch(ip_list):
    """Fetches multiple IP locations in parallel."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_ip_location, ip_list))
    return results


def fetch_business_batch(address_list):
    """Checks multiple business addresses in parallel."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(verify_business_address, address_list))
    return results


# Example Tests
if __name__ == "__main__":
    sample_ips = ["71.13.24.234", "8.8.8.8", "192.168.1.1"]
    sample_addresses = [
        "215 Madison Avenue, Fort Atkinson, Wisconsin",
        "1600 Amphitheatre Parkway, Mountain View, CA"
    ]

    print("Fetching IP locations in batch...")
    ip_results = fetch_ip_batch(sample_ips)
    print(ip_results)

    print("Verifying business addresses in batch...")
    business_results = fetch_business_batch(sample_addresses)
    print(business_results)
