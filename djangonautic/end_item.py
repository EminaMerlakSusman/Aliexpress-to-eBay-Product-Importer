from ebaysdk.trading import Connection
'''Ending sandbox test listings that I don't need anymore'''

if __name__ == '__main__':
    api = Connection(domain='api.sandbox.ebay.com', config_file='ebay.yaml', debug=True)
    request = {
        "ItemID": 110525437375,
        "EndingReason": "NotAvailable"

    }
    call = api.execute('ValidateTestUserRegistration', request)
    response = api.execute('EndItem', request)