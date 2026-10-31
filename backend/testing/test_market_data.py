
import os
import requests
import json
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("DATA_GOV_IN_API_KEY")

RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"

if not API_KEY:
    raise ValueError("API key missing. Check your .env file.")

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}


def fetch_paddy_prices():
    print("\nFetching Paddy prices in Krishna district...\n")

    all_records = []
    offset = 0
    limit = 10

    while True:
        params = {
            "api-key": API_KEY,
            "format": "json",
            "limit": limit,
            "offset": offset,
            "filters[state.keyword]": "Andhra Pradesh",
            "filters[district]": "Krishna",
            "filters[commodity]": "Paddy(Common)"
        }

        try:
            response = requests.get(
                URL,
                params=params,
                headers=HEADERS,
                timeout=(20, 90)
            )

            print("HTTP Status:", response.status_code)
            response.raise_for_status()

            data = response.json()

            records = data.get("records", [])
            total = int(data.get("total", 0))

            all_records.extend(records)

            print(
                f"Fetched {len(records)} records. "
                f"Total available: {total}"
            )

            if not records or len(all_records) >= total:
                break

            offset += limit

        except requests.exceptions.Timeout:
            print("ERROR: API request timed out.")
            return

        except requests.exceptions.RequestException as error:
            print("REQUEST ERROR:", error)

            if error.response is not None:
                print("Response:", error.response.text[:1000])

            return

        except (ValueError, TypeError) as error:
            print("DATA ERROR:", error)
            return

    print("\n========== FINAL RESULTS ==========")
    print("Total records fetched:", len(all_records))

    for record in all_records:
        print("\n----------------------------------")
        print("State:", record.get("state"))
        print("District:", record.get("district"))
        print("Market:", record.get("market"))
        print("Commodity:", record.get("commodity"))
        print("Variety:", record.get("variety"))
        print("Grade:", record.get("grade"))
        print("Arrival Date:", record.get("arrival_date"))
        print("Minimum Price:", record.get("min_price"))
        print("Maximum Price:", record.get("max_price"))
        print("Modal Price:", record.get("modal_price"))


if __name__ == "__main__":
    fetch_paddy_prices()
