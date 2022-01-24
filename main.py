import pandas as pd
from usps import USPSApi, Address
from config import USERID, FILE


def validate_address_data(address: Address):
    """requires USPS address object"""

    usps = USPSApi(USERID, test=True)
    validation = usps.validate_address(address)

    try:
        validation.result['AddressValidateResponse']['Address']['Error']
    except KeyError:
        return "Yes"
    else:
        return "No"


def update_address_csv(valid_address_data, filename):
    """overwrites existing file with updated information"""
    valid_address_data.to_csv(filename, index=False)
    print(f"Done. Please check {filename}")


def check_address_data(filename):
    """reads csv and passes dataframe to validate_address_data func"""
    try:
        address_data = pd.read_csv(filename)
        is_valid = []
        for index, row in address_data.iterrows():
            is_valid.append(validate_address_data(Address(
                name=row.get("Company"),
                address_1=row.get("Street"),
                city=row.get("City"),
                state=row.get("St"),
                zipcode=row.get("ZIPCode")
            )))
        # add column to dataframe
        address_data['Valid Address'] = is_valid
        update_address_csv(address_data, filename)

    except FileNotFoundError:
        print("File not found")


check_address_data(FILE)
