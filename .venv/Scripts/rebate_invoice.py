class RebateInvoice:
    """
    Represents a rebate invoice with various transaction details.
    """

    def __init__(self, campaign_sponsor, campaign_code, tracking_number, submission_date, purchase_date,
                 invoice_number, retailer_name, retailer_address, retailer_city, retailer_state_code, retailer_zip,
                 rebate_amount, rebate_status, consumer_name, consumer_address, consumer_city, consumer_state_code,
                 consumer_zip, email, consumer_phone, ip_address):
        self.campaign_sponsor = campaign_sponsor
        self.campaign_code = campaign_code
        self.tracking_number = tracking_number
        self.submission_date = submission_date
        self.purchase_date = purchase_date
        self.invoice_number = invoice_number
        self.retailer_name = retailer_name
        self.retailer_address = retailer_address
        self.retailer_city = retailer_city
        self.retailer_state_code = retailer_state_code
        self.retailer_zip = retailer_zip
        self.rebate_amount = rebate_amount
        self.rebate_status = rebate_status
        self.consumer_name = consumer_name
        self.consumer_address = consumer_address
        self.consumer_city = consumer_city
        self.consumer_state_code = consumer_state_code
        self.consumer_zip = consumer_zip
        self.email = email
        self.consumer_phone = consumer_phone
        self.ip_address = ip_address

    def to_dict(self):
        """
        Converts the RebateInvoice object to a dictionary format.
        """
        return {
            "campaign_sponsor": self.campaign_sponsor,
            "campaign_code": self.campaign_code,
            "tracking_number": self.tracking_number,
            "submission_date": self.submission_date,
            "purchase_date": self.purchase_date,
            "invoice_number": self.invoice_number,
            "retailer_name": self.retailer_name,
            "retailer_address": self.retailer_address,
            "retailer_city": self.retailer_city,
            "retailer_state_code": self.retailer_state_code,
            "retailer_zip": self.retailer_zip,
            "rebate_amount": self.rebate_amount,
            "rebate_status": self.rebate_status,
            "consumer_name": self.consumer_name,
            "consumer_address": self.consumer_address,
            "consumer_city": self.consumer_city,
            "consumer_state_code": self.consumer_state_code,
            "consumer_zip": self.consumer_zip,
            "email": self.email,
            "consumer_phone": self.consumer_phone,
            "ip_address": self.ip_address
        }
