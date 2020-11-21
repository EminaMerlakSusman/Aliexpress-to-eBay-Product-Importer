from ebaysdk.trading import Connection
import requests
import xml.etree.ElementTree as ET



def get_session_ID():
    '''Establishing API conncetion'''

    api = Connection(domain='api.sandbox.ebay.com', appid="EminaMer-testing-SBX-0ca7fae46-248b79d0", devid = "09ea5789-88e8-49dd-9491-8d50ebdc9fd4",
                     certid = "SBX-ca7fae460895-89b9-45d6-8fce-7d21")

    '''Making GetSessionID call to get session ID of the user who logged in'''

    request = {
        'RuName': "Emina_Merlak_Su-EminaMer-testin-gjjhk"

    }

    sess_id_response = api.execute('GetSessionID', request)

    # parsing response
    root = ET.fromstring(sess_id_response.text)

    session_ID = root[4].text

    return session_ID

def get_token(session_ID):
    '''Exchanging user's SessionID for a token'''

    data = {
        'SessionID': "SysFAA**ec001c891750ac793df557bcfffff2b3"

    }

    #
    # token_response = api.execute('FetchToken', data)
    #
    # # parsing response
    # root = ET.fromstring(token_response.text)
    #
    # token = root[4].text
    # print(token)


    api = Connection(domain='api.sandbox.ebay.com', token="AgAAAA**AQAAAA**aAAAAA**tli5Xw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4aiCpSDoA6dj6x9nY+seQ**SysFAA**AAMAAA**fuG6FhFWC2ckDcNXyOAsdXH3SbqDIDXtqt8rgRvfHV09Eqzu0P6Fi1HB1rzY622nqUXVFYQBJJK3nxga5h9FZXGjAotN1k0NK7b6D2aNpKGB9R28lQZF0wLQG1YEAuR3esl/QusZin7P1mTlf48NDC++nrkr0RHfEGwD2bR0l9USBAvGus1A6h86u1JvDu7QzSpZsuMJyRUdX6KnY7fU7lEi4zHmZIr1YYfBEhdI88e0PTKOwyHyBPSxaLc5oRIzmc9tkn60TquKAd44uEK2AKNu/+vAOEP6pJjdfsi8So7aTORECG8CGSSQ6HcT1iW2yyXZVSt1V6CMTUYIS9+dx+VaHrTh6a2ctwGDOoM6WnrqOPylm6aRC043XwyDCTsPPri229QVTxX9lEIpEnO5xHjXg2rnCYFM+RoSiqZXCUj7CcRGVpd/enhYYGUzZ1QBXPHX3AWHiJvJlemYOAnllcyovwCaZD1m9sTWn8UL/VnvyLUHiuuxTZuhuHEKKRKvFVLWGsA261nI0jQ4pU9xxKOPvHGAmdGPt717urn2ILli/+XLsnr5riU6hYUXIxdcNcUXvdn3Ic2ALCobwjbuiYpMlxObJTOjK/4OBwhD2wFjfkl8WtiKqEIYNjrALIxenQa9RE4a8DlGRJU7AltkDFrQn58NkZtTPck0xSLPHFW7ZNoYGnjUW51stzYK0Alod4SAG7dXwvEjq1k+KBeTG0Q+Td/VNqHjRN4KwjF7FHtU+1UgLSgHFQr6jaU4mM4S", debug=True)

    # request = {
    #     "Item": {
    #         "Title":"testingngfnw ",
    #         "Country": "CN",
    #         "Location": "CN",
    #         "Site": "US",
    #         "StartPrice": 5.99,
    #         "ConditionID": "1000",
    #         "PaymentMethods": "PayPal",
    #         "PayPalEmailAddress": "sb-ekcsr976485@personal.example.com",
    #         "PrimaryCategory": {"CategoryID": '1234'},
    #         "ItemSpecifics": {
    #             "NameValueList": [{"Name": "Brand", "Value": "Unbranded"}, {"Name": "Type", "Value": "Toilet Brush"},
    #                               {"Name": "Material", "Value": "Plastic"}]},
    #         "Description": "sth",
    #         "ListingDuration": "Days_7",
    #         "Currency": "USD",
    #         "ReturnPolicy": {
    #             "ReturnsAcceptedOption": "ReturnsAccepted",
    #             "RefundOption": "MoneyBack",
    #             "ReturnsWithinOption": "Days_30",
    #             # "Description": "If you are not satisfied, return the keyboard.",
    #             "ShippingCostPaidByOption": "Seller"
    #         },
    #         "ShippingDetails": {
    #             "ShippingServiceOptions": {
    #                 "FreeShipping": "True",
    #                 "ShippingService": "StandardShippingFromOutsideUS"
    #             }
    #         },
    #         "DispatchTimeMax": "3",
    #         "PictureDetails": {
    #             "PictureURL": 'https://ae01.alicdn.com/kf/Hcb1eebaa296a473486f79669211f0001m/2019-Movie-Joker-Silk-Poster-Joker-Origin-Movie-Prints-Comics-Wall-Art-Decor-Canvas-Pictures-Film.jpg'
    #         },
    #
    #     }
    # }
    #
    # resp = api.execute('AddItem', request)

#resp = requests.get("https://signin.ebay.com/ws/eBayISAPI.dll?oAuthRequestAccessToken&client_id=EminaMer-testing-PRD-2e6527e18-557772c0&redirect_uri=Emina_Merlak_Su-EminaMer-testin-vnissn&client_secret=PRD-e6527e1828b8-ed34-423d-956f-2792&code=v%5E1.1%2523i%5E1%2523p%5E3%2523I%5E3%2523f%5E0%2523r%5E1%2523t%5EUl41XzExOjEyNTQzNUQ5NzcyNzAwRjlEQjQwRTQ2QUREQzE1Qzg2XzBfMSNFXjI2MA%253D%253D")
#print(resp.text)