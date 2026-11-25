
import csv
from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# DATASET CONFIGURATION
# --------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

CSV_FILE = (
    PROJECT_FOLDER
    / "dataset"
    / "AGMARKNET_Mandi_Prices.csv"
)

DATA_SOURCE = "AGMARKNET"
SOURCE_URL = "https://agmarknet.gov.in/"


# --------------------------------------------------
# DATE CONVERSION
# --------------------------------------------------

def parse_arrival_date(date_value):

    if not date_value:
        return None

    date_value = date_value.strip()

    date_formats = [
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%b-%Y",
        "%d %b %Y",
        "%m/%d/%Y"
    ]

    for date_format in date_formats:

        try:
            return datetime.strptime(date_value, date_format)

        except ValueError:
            continue

    return None


# --------------------------------------------------
# FETCH MANDI PRICES
# --------------------------------------------------

def get_mandi_prices(state, district, commodity):

    if not CSV_FILE.exists():

        return {
            "error": f"Dataset not found: {CSV_FILE}"
        }

    results = []

    try:

        with open(
            CSV_FILE,
            mode="r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            required_columns = [
                "State",
                "District",
                "Market",
                "Commodity",
                "Arrival_Date",
                "Min_x0020_Price",
                "Max_x0020_Price",
                "Modal_x0020_Price"
            ]

            if not reader.fieldnames or not all(
                column in reader.fieldnames
                for column in required_columns
            ):

                return {
                    "error": "Dataset columns do not match the expected format."
                }

            for row in reader:

                state_value = (row.get("State") or "").strip()
                district_value = (row.get("District") or "").strip()
                commodity_value = (row.get("Commodity") or "").strip()

                state_match = state.lower() in state_value.lower()
                district_match = district.lower() in district_value.lower()
                commodity_match = commodity.lower() in commodity_value.lower()

                if state_match and district_match and commodity_match:

                    results.append(row)

        if not results:

            return {
                "records": [],
                "error": None,
                "source": DATA_SOURCE,
                "source_url": SOURCE_URL,
                "data_as_of": None,
                "data_type": "Historical mandi price dataset"
            }

        # Find the latest available arrival date
        valid_dates = []

        for row in results:

            date_value = row.get("Arrival_Date", "")
            parsed_date = parse_arrival_date(date_value)

            if parsed_date:
                valid_dates.append((parsed_date, date_value))

        if valid_dates:

            latest_date = max(
                valid_dates,
                key=lambda item: item[0]
            )[1]

        else:
            latest_date = "Date unavailable"

        return {
            "records": results,
            "error": None,
            "source": DATA_SOURCE,
            "source_url": SOURCE_URL,
            "data_as_of": latest_date,
            "data_type": "Historical mandi price dataset"
        }

    except (OSError, KeyError, csv.Error) as error:

        return {
            "error": f"Unable to read mandi dataset: {error}"
        }


# --------------------------------------------------
# DISPLAY MANDI PRICE REPORT
# --------------------------------------------------

def display_mandi_prices(result):

    print("\n========== MANDI PRICE REPORT ==========")

    if isinstance(result, dict) and result.get("error"):

        print(result["error"])
        return

    records = result.get("records", [])

    if not records:

        print("No matching mandi records found.")
        print("Try another district or commodity.")
        return

    for index, row in enumerate(records, start=1):

        print(f"\nRecord {index}")

        print("State:", row.get("State", "N/A"))
        print("District:", row.get("District", "N/A"))
        print("Market:", row.get("Market", "N/A"))
        print("Commodity:", row.get("Commodity", "N/A"))
        print("Variety:", row.get("Variety", "N/A"))
        print("Grade:", row.get("Grade", "N/A"))
        print("Arrival Date:", row.get("Arrival_Date", "N/A"))

        print("Minimum Price:", row.get("Min_x0020_Price", "N/A"))
        print("Maximum Price:", row.get("Max_x0020_Price", "N/A"))
        print("Modal Price:", row.get("Modal_x0020_Price", "N/A"))

    print("\n========== SOURCE INFORMATION ==========")

    print("Data Type:", result["data_type"])
    print("Data As Of:", result["data_as_of"])
    print("Source:", result["source"])
    print("Source URL:", result["source_url"])

    print("\nTotal matching records:", len(records))


# --------------------------------------------------
# MAIN TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("===== AGRICULTURAL MANDI PRICE SEARCH =====")

    state = input("Enter State: ").strip()
    district = input("Enter District: ").strip()
    commodity = input("Enter Commodity: ").strip()

    if not state or not district or not commodity:

        print("Please enter all three fields.")

    else:

        data = get_mandi_prices(
            state,
            district,
            commodity
        )

        display_mandi_prices(data)
