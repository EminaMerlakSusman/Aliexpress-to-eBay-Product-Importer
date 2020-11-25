from djangonautic.raw_html_test import return_response


def format_api_call(url):
    '''Formats everything for the api call'''
    (title, images_list, price_value, listing_has_variations, listing_has_var_images, productSKUPropertyList, variationPictures, skuPriceList) = return_response(url)

    '''Formatting title'''

    title_fr = ""
    if title[80] == " ":
        title_fr = title[:80]
    else:
        rev = title[:80][::-1]
        i = rev.index(" ")
        i_fr = 79-i
        title_fr = title[:i_fr]


    if not listing_has_variations:
        price = price_value


    '''Variations data'''
    main_product_images = images_list

    if listing_has_variations:
        # getting variation specific picture set
        if listing_has_var_images:
            variationSpecificName = list(variationPictures.keys())[0]
            #print("variation spicture", variation_pictures)
            variationSpecificPictureSet = []
            name_value_URL_dicts = variationPictures[variationSpecificName]
            for name_value_URL_dict in name_value_URL_dicts:
                val = name_value_URL_dict["Actual_Name"]
                pic_url = name_value_URL_dict["PictureURL"]
                name_url_pair = {"VariationSpecificValue": val, "PictureURL": pic_url}
                variationSpecificPictureSet.append(name_url_pair)

        variation_node = []

        # getting the Variation combiantions

        for combo_list in skuPriceList:
            nameValueList = []
            for i in range(len(combo_list) - 1): #last one is price
                var_name = productSKUPropertyList[i]["Name"] #variation combos are in the same order as in skuPropertyList
                var_val = combo_list[i]["Value_Name"]
                name_value_pair = {"Name": var_name, "Value": var_val}
                nameValueList.append(name_value_pair)

            startPrice = combo_list[-1]["price"]

            this_variation = {
                     "VariationSpecifics": {"NameValueList": nameValueList},
                     "Quantity": 1,
                     "StartPrice": startPrice
                 }
            variation_node.append(this_variation)

        # getting variation specific set

        variationSpecificsSet = {"NameValueList": []}
        for name_values_dict in productSKUPropertyList:
            name = name_values_dict["Name"]
            values_list = name_values_dict["Value"]
            vals_list_formatted = []
            for values_dict in values_list:
                val_name = values_dict["Actual_Name"]
                vals_list_formatted.append(val_name)
            variationSpecificsSet["NameValueList"].append({"Name": name, "Value": vals_list_formatted})
    # try:
    #     #print(variation_node)
    #     #print(variationSpecificsSet)
    #     #print(variationSpecificPictureSet)
    # except:
    #     pass
    if not listing_has_var_images:
        variationSpecificName = None
        variationSpecificPictureSet = None
    
    return (title_fr, listing_has_variations, main_product_images, price_value, variation_node, variationSpecificsSet, variationSpecificName, variationSpecificPictureSet)
#which_var_has_images = which_var_has_images