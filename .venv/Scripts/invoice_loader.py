import os
import csv
import json
import logging
from rebate_invoice import RebateInvoice

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class InvoiceLoader:
    def __init__(self, directory="tests", filename="RebateTest.csv", output_directory="data",
                 output_file="test_invoices.json"):
        self.directory = directory
        self.filename = filename
        self.output_directory = output_directory
        self.output_file = os.path.join(output_directory, output_file)
        self.filepath = os.path.join(self.directory, self.filename)

        os.makedirs(self.output_directory, exist_ok=True)

    def detect_delimiter(self):
        """Detects the delimiter of the CSV file (supports comma, tab, and semicolon)."""
        try:
            with open(self.filepath, mode='r', encoding='utf-8-sig') as file:
                sample = file.read(500)
                if "\t" in sample:
                    return "\t"
                elif ";" in sample:
                    return ";"
                else:
                    return ","
        except FileNotFoundError:
            logging.error(f"File not found: {self.filepath}")
            return None

    def load_invoices(self):
        """Loads rebate invoices from CSV and converts them into RebateInvoice objects."""
        invoices = []
        delimiter = self.detect_delimiter()

        if delimiter is None:
            return []

        logging.info(f"Detected delimiter: '{delimiter}'")

        try:
            with open(self.filepath, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file, delimiter=delimiter)

                reader.fieldnames = [header.strip().lower() for header in reader.fieldnames]
                logging.info(f"CSV Headers Detected: {reader.fieldnames}")

                for row in reader:
                    row = {key.strip().lower(): value for key, value in row.items()}

                    try:
                        invoice = RebateInvoice(
                            campaign_sponsor=row.get("campaign sponsor", ""),
                            campaign_code=int(row.get("campaign code", 0)),
                            tracking_number=int(row.get("tracking number", 0)),
                            submission_date=row.get("originating submission date", ""),
                            purchase_date=row.get("purchase date", ""),
                            invoice_number=row.get("invoice number", ""),
                            retailer_name=row.get("retailer name", ""),
                            retailer_address=row.get("retailer address", ""),
                            retailer_city=row.get("retailer city", ""),
                            retailer_state_code=row.get("retailer state code", ""),
                            retailer_zip=row.get("retailer zip", ""),
                            rebate_amount=float(row.get("amount ($)", 0.0)),
                            rebate_status=row.get("rebate status", ""),
                            consumer_name=row.get("consumer name", ""),
                            consumer_address=row.get("consumer address", ""),
                            consumer_city=row.get("consumer city", ""),
                            consumer_state_code=row.get("consumer state code", ""),
                            consumer_zip=row.get("consumer zip", ""),
                            email=row.get("email address", ""),
                            consumer_phone=row.get("consumer phone number", ""),
                            ip_address=row.get("ip address", "")
                        )
                        invoices.append(invoice)
                    except KeyError as e:
                        logging.error(f"Missing column '{str(e)}' in CSV.")
                    except ValueError as e:
                        logging.error(f"Invalid data type in CSV -> {str(e)}")

        except FileNotFoundError:
            logging.error(f"Error: {self.filepath} not found.")
        except Exception as e:
            logging.error(f"Error reading file: {e}")

        logging.info(f"Successfully loaded {len(invoices)} invoices.")
        return invoices

    def save_to_json(self, invoices):
        """Saves invoices to JSON format for further fraud detection processing."""
        try:
            json_data = [invoice.to_dict() for invoice in invoices]

            with open(self.output_file, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4)

            logging.info(f"Saved {len(invoices)} invoices to {self.output_file}")
        except Exception as e:
            logging.error(f"Error saving JSON file: {e}")
