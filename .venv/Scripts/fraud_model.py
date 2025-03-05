import json
import os
from datetime import datetime, timedelta
from api_services import get_ip_location

USER_HISTORY_FILE = "data/user_history.json"

class UserHistory:
    """
    Tracks past rebate submissions to detect repeated claims.
    """

    def __init__(self):
        self.user_data = self.load_user_history()

    def load_user_history(self):
        """Loads user submission history from a JSON file."""
        if not os.path.exists(USER_HISTORY_FILE):
            return {}

        try:
            with open(USER_HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_user_history(self):
        """Saves the updated user history to a JSON file."""
        with open(USER_HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(self.user_data, file, indent=4)

    def has_recent_submission(self, name, submission_date):
        """Checks if the user has submitted in the last year."""
        if name not in self.user_data:
            return False

        one_year_ago = submission_date - timedelta(days=365)
        for record in self.user_data[name]:
            prev_date = datetime.strptime(record["submission_date"], "%Y-%m-%d %H:%M:%S")
            if prev_date >= one_year_ago:
                return True

        return False

    def add_submission(self, name, submission_date, tracking_number):
        """Records a new submission to the user history."""
        if name not in self.user_data:
            self.user_data[name] = []

        self.user_data[name].append({
            "submission_date": submission_date.strftime("%Y-%m-%d %H:%M:%S"),
            "tracking_number": tracking_number
        })
        self.save_user_history()


def process_fraud_check(json_file):
    if not os.path.exists(json_file):
        print("❌ Error: Input JSON file not found.")
        return

    # Load existing JSON data (invoices with full details)
    with open(json_file, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON format in input file.")
            return

    user_history = UserHistory()  # Initialize user history tracking
    print(f"🔍 Processing {len(data)} transactions...")

    for row in data:
        consumer_name = row.get("consumer_name", "").strip().lower()
        tracking_number = row.get("tracking_number", "")
        submission_date_str = row.get("submission_date", "")

        try:
            submission_date = datetime.strptime(submission_date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            row["fraud_reasons"] = ["Invalid submission date format"]
            continue

        # Fraud detection logic
        row["fraud_score"] = 0
        row["fraud_flag"] = False
        row["fraud_reasons"] = []

        if user_history.has_recent_submission(consumer_name, submission_date):
            row["fraud_score"] += 2
            row["fraud_reasons"].append("Repeat submission within one year")

        row["fraud_flag"] = row["fraud_score"] >= 3

        # Save submission to user history
        user_history.add_submission(consumer_name, submission_date, tracking_number)

        # Enrich with IP location data
        ip = row.get("ip_address", "")
        ip_info = get_ip_location(ip)
        row.update(ip_info)

    # Save the processed fraud results (WITH dealer info)
    output_file = os.path.join("data", "processed_fraud_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Fraud check completed. Results saved to {output_file}")
