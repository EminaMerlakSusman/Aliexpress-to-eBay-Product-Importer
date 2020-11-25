
from ebaysdk.trading import Connection
import os
from djangonautic import api_formatting_for_raw_html
from djangonautic import get_categories
from djangonautic.models import Product
from djangonautic.models import Page


'''Makes the api call to add product, also calls other functions to import the product in the url'''

def make_api_call(token):
    # getting inputted product url from database
    url_list = list(Product.objects.all())
    url = url_list[-1].productURL

    (title_fr, listing_has_variations, main_product_images, price_value, variation_node, variationSpecificsSet,
     variationSpecificName, variationSpecificPictureSet) = api_formatting_for_raw_html.format_api_call(url)  # Importing product data from URL
    # getting rid of '&' sign in title to avoid xml errors
    cleaned_title = ''
    for char in title_fr:
        if char != "&":
            if len(cleaned_title) > 0:
                if cleaned_title[-1] != ' ':
                    cleaned_title += char
                elif char != ' ':
                    cleaned_title += char
            else:
                cleaned_title += char
        else:
            cleaned_title += '&amp;'


    cateid = get_categories.get_suggested_categories(query=cleaned_title, config_file=None)[1] # getting suggested categories
    api = Connection(domain='api.sandbox.ebay.com', token = token)

    request = {
        "Item": {
            "Title": cleaned_title,
            "Country": "CN",
            "Location": "CN",
            "Site": "US",
            "ConditionID": "1000",
            "PaymentMethods": "PayPal",
            "PayPalEmailAddress": "sb-ekcsr976485@personal.example.com",
            "PrimaryCategory": {"CategoryID": cateid},
            "ItemSpecifics": {"NameValueList": [{"Name": "Brand", "Value": "Unbranded"}, {"Name": "Type", "Value": "Toilet Brush"}, {"Name": "Material", "Value": "Plastic"}]},
            "Description": "sth",
            "ListingDuration": "GTC",
            "Currency": "USD",
            "ReturnPolicy": {
                "ReturnsAcceptedOption": "ReturnsAccepted",
                "RefundOption": "MoneyBack",
                "ReturnsWithinOption": "Days_30",
                #"Description": "If you are not satisfied, return the keyboard.",
                "ShippingCostPaidByOption": "Seller"
            },
            "ShippingDetails": {
                "ShippingServiceOptions": {
                    "FreeShipping": "True",
                    "ShippingService": "StandardShippingFromOutsideUS"
                }
            },
            "DispatchTimeMax": "3",
            "PictureDetails": {
                "PictureURL":  main_product_images
                },

        }
    }

    # If we have variations, we add them to the call
    if listing_has_variations:
        request["Item"]["Variations"] = {
            "Variation": variation_node,
            "VariationSpecificsSet": variationSpecificsSet
        }

        if variationSpecificPictureSet != []:
            request["Item"]["Variations"]["Pictures"] = {"VariationSpecificName": variationSpecificName, "VariationSpecificPictureSet": variationSpecificPictureSet}
    else:
        request["Item"]["StartPrice"] = price_value

    #call = api.execute('ValidateTestUserRegistration', request)
    response = api.execute('AddFixedPriceItem', request)
    progress = Page(title='Made api call')
    progress.save()
    return 'Work is complete!'
#make_api_call("https://www.aliexpress.com/item/4001155636952.html?spm=a2g0o.productlist.0.0.448e413dN6SAhP&algo_pvid=838dab60-bf9f-4bc9-9a16-8b0dd7656a47&algo_expid=838dab60-bf9f-4bc9-9a16-8b0dd7656a47-9&btsid=0bb0622f16027692419813645ecfb0&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_")
#make_api_call()