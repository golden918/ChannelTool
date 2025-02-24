import pandas as pd
import json
import os
from datetime import datetime, timedelta

USER_HISTORY_FILE = "data/user_history.json"


def load_user_history():
    """Load user history from JSON or create an empty file if missing."""
    if not os.path.exists(USER_HISTORY_FILE):
        return {}

    with open(USER_HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_user_history(history):
    """Save updated user history to JSON."""
    with open(USER_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)


def fraud_engine(transaction, user_history):
    fraud_score = 0
    reasons = []

    full_name = transaction.get("consumer_name", "").strip().lower()
    submission_date = transaction.get("submission_date", "")

    # Convert submission_date to datetime
    try:
        submission_date = datetime.strptime(submission_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        reasons.append("Invalid submission date format")
        return fraud_score, False, reasons

    one_year_ago = submission_date - timedelta(days=365)

    # Check if the user has submitted within the past year
    if full_name in user_history:
        previous_submissions = user_history[full_name]
        for record in previous_submissions:
            prev_date = datetime.strptime(record["submission_date"], "%Y-%m-%d %H:%M:%S")
            if prev_date >= one_year_ago:
                fraud_score += 2
                reasons.append("Repeat submission within one year")
                break  # No need to check further

    # Update user history with the latest submission
    if full_name not in user_history:
        user_history[full_name] = []
    user_history[full_name].append({
        "submission_date": submission_date.strftime("%Y-%m-%d %H:%M:%S"),
        "tracking_number": transaction.get("tracking_number", "Unknown")
    })

    fraud_flag = fraud_score >= 3
    return fraud_score, fraud_flag, reasons


def process_fraud_check(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    user_history = load_user_history()
    results = []

    for row in data:
        score, flag, reasons = fraud_engine(row, user_history)
        results.append({
            "Transaction ID": row.get("tracking_number", "Unknown"),
            "Fraud Score": score,
            "Flagged": flag,
            "Reasons": ", ".join(reasons)
        })

    save_user_history(user_history)

    results_df = pd.DataFrame(results)
    output_file = "processed_fraud_results.csv"
    results_df.to_csv(output_file, index=False)
    print(f"✅ Fraud check completed. Results saved to {output_file}")

