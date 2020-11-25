import re
import requests
import json

import re


def return_response(url):
    #url = "https://www.aliexpress.com/item/4000926109140.html?spm=a2g0s.9042311.0.0.6af74c4dYdrOMu"
    '''Return url'''
    response = requests.get(url).text
    print(response)

    '''Getting title and description'''

    start = response.find("pageModule") + len("pageModule") + 2
    end = response[start:].index("preSaleModule") - 2
    #print(response[start:][:end])
    #print(end - start)
    page_module_dict = json.loads(response[start:][:end])
    #print(page_module_dict)
    title = page_module_dict['title']
    cutoff = title.find("|")
    title = title[:cutoff]
    #print(title)
    #print(response[start:][:end])


    '''Getting category'''

    st = response.find("breadCrumbPathList") + len("breadCrumbPathList") + 2
    end = response[st:].find("}]") + 2
    cate_dicts = eval(response[st:][:end])

    category = cate_dicts[-1]["name"]
    #print(category)


    '''Getting discount and price, if there are no variations'''

    st = response.find("priceModule") + len("priceModule") + 2
    end = response[st:].find("quantityModule") - 2
    price_dict = json.loads(response[st:][:end])
    #print(price_dict)

    # checking whether the page displays a single price
    # or a price range (if there are variations which have different costs)

    variations_exist = False
    max_price = price_dict["maxAmount"]["value"]
    min_price = price_dict["minAmount"]["value"]
    price_value = None
    if max_price == min_price:
        price_value = max_price
        if price_value < 0.99: #minimum allowed price on ebay is 0.99
            price_value = 0.99


    '''Getting images'''

    start = response.find("imagePathList") + len("imagePathList") + 2
    end = response[start:].find("]") + 1
    images_list = eval(response[start:][:end])

    #print(images_list)
    ''''
    **********VARIATION RELATED STUFF, DO THIS ONLY IF THE LISTING HAS VARIATIONS************
    '''


    #print(skuPriceList)

    '''Getting variation lists, and also Variation Specific Picture Set'''
    listing_has_variations = True
    listing_has_var_images = False

    start = response.find("productSKUPropertyList")
    #print(start)
    if start == -1:
        listing_has_variations = False

    productSKUPropertyList = []
    variationPictures = {}
    skuPriceList = []
    #which_var_has_images = []

    if listing_has_variations:
        start = start + len("productSKUPropertyList") + 2
        end = response.rfind("skuPriceList") - 2
        variations_list = response[start:end]
        json_of_var_list = json.loads(variations_list)
        #print(json_of_var_list)
        ind = variations_list.index("isShowTypeColor")

        listing_has_var_images = True
        # getting name-value pairs of variations
        productSKUPropertyList = []
        variationPictures = {}

        for prop_dict in json_of_var_list:
            # this part gets name and values for each variation
            var_name = prop_dict['skuPropertyName']

            #print(" var name:", var_name)
            var_vals_unformatted = prop_dict['skuPropertyValues']
            var_vals_formatted = []
            for val_dict in var_vals_unformatted:
                #print(val_dict)

                value_name = val_dict['propertyValueDisplayName']

                #print("val dict:", val_dict)
                value_id = val_dict['propertyValueId']
                var_vals_formatted.append({"Value_Name": value_name, "Value_Id": str(value_id), "Actual_Name": value_name})
                # this part checks if the variation has images,
                # in that case we are appending them to variation
                # image set
                try:
                    image_path = val_dict['skuPropertyImagePath']
                    listing_has_var_images = True
                    #print(image_path)
                    try:
                        variationPictures[var_name].append({"Value_Name": value_name, "Value_Id": str(value_id), "Actual_Name": value_name, "PictureURL": image_path})
                    except:
                        variationPictures[var_name] = [{"Value_Name": value_name, "Value_Id": str(value_id), "Actual_Name": value_name, "PictureURL": image_path}]
                except:
                    #print("No variation images were found.")
                    listing_has_var_images = False
            productSKUPropertyList.append({"Name": var_name, "Value": var_vals_formatted})
                #print(variationPictures)


        '''Getting prices for each variation combination'''

        start = response.find("skuPriceList") + len("skuPriceList") + 2 # this is a list of dictionaries with price of each combination
        end = response[start:].find("warrantyDetailJson") - 2
        #p#rint(response[start:end])
        needed_dict = json.loads(response[start:][:end])

        skuPriceList = []
        #print("len", len(matches_positions))
        for combination_dict in needed_dict:
            #st = i-2
            #print(needed_dict[st:])
            #end = needed_dict[st:].find('}}') + 2
            #to_dict = json.loads(needed_dict[st:][:end])
            #print(to_dict)
            raw_values = combination_dict['skuPropIds'].split(",") #ids of every item in combination
            formatted_values = []
            for j in range(len(raw_values)):
                this_property_id = raw_values[j]
                check_string = this_property_id
                name = productSKUPropertyList[j]["Name"]

                value_list = productSKUPropertyList[j]["Value"]
                #finding value in value list with this id
                #print(value_list)
                for value_dict in value_list:
                    cur_id = value_dict["Value_Id"]


                    cur_val = value_dict["Actual_Name"]
                    if cur_id == this_property_id:
                        value = cur_val
                        id = cur_id

                #if name in which_var_has_images:
                    #in this case we set the variation id a
                    #check_string = id
                formatted_values.append({"Value_Name": value, "Value_Id": id})
            price = combination_dict['skuVal']['skuAmount']['value']
            skuId = combination_dict['skuId']
                #print("skuid found,", raw_values, formatted_values, combination_dict)
                #print(name, value_list)
            if price < 0.99: #minimum allowed price on ebay
                price = 0.99

            currency = combination_dict['skuVal']['skuAmount']['currency']
            formatted_values.append({"price": price, "currency":currency, "sku": skuId})
            skuPriceList.append(formatted_values)

        '''Checking if the variation has duplicate values
        and setting them to id if it does.
        '''

        for var_dict in productSKUPropertyList:
            values_list = var_dict["Value"]
            names = [d["Value_Name"] for d in values_list]
            names_set = set(names)
            if len(names) != len(names_set):
                # names contain duplicate values
                for name_id_pair in values_list:
                    id = name_id_pair["Value_Id"]
                    name_id_pair["Actual_Name"] = str(id)


        '''We also need to change skuPriceList.
        we already changed productSKUPropertyList,
        so we just find the variation's ID and change it
        to the corresponding name in skuPropertyList.
        '''

        for combination_list in skuPriceList:
            for k in range(len(combination_list[:-1])):  # last one is price, so we cut it off
                val_dict = combination_list[k]
                #print(val_dict)
                val_id = val_dict["Value_Id"]
                #print(val_id)
                val_name = val_dict["Value_Name"]
                corresponding_vals = [name_pair["Value_Id"] for name_pair in productSKUPropertyList[k]["Value"]]
                #print(corresponding_vals)
                this_val_index = corresponding_vals.index(val_id)
                real_name = productSKUPropertyList[k]["Value"][this_val_index]["Actual_Name"]
                val_dict["Value_Name"] = real_name

        #print("New sku price list", skuPriceList)


        '''Changing variation specific image set in case of duplicates
        (at this point we aleady changed productSKUPropertyList).
        '''
        listing_has_var_images = variationPictures != {}
        if listing_has_var_images:
            name = list(variationPictures.keys())[0]
            corresponding_names = [name_dict['Name'] for name_dict in productSKUPropertyList]
            corresponding_name_index = corresponding_names.index(name)
            corresponding_dict = productSKUPropertyList[corresponding_name_index]
            list_of_value_dicts = corresponding_dict["Value"]
            list_of_corresponding_ids = [x["Value_Id"] for x in list_of_value_dicts]
            print(list_of_corresponding_ids)
            #print(variationPictures)
            for val_dict in variationPictures[name]:
                #print(val_dict)
                value_id = val_dict["Value_Id"]
                print(value_id)
                ind = list_of_corresponding_ids.index(value_id)
                print(ind)
                value_real_name = list_of_value_dicts[ind]["Actual_Name"]
                print(value_real_name)
                val_dict["Actual_Name"] = value_real_name


        '''Sometimes listings have options for where you can ship the product from.
        We will only ship from China, so we are deleting the other options from 
        the variation list and sku combinations list.'''

        # deleting from variations list
        ship_var_index = None
        i = 0
        china_id = None
        for prop_dict in productSKUPropertyList:
            var_name = prop_dict["Name"]
            #print("ships from" in var_name.lower())
            if "ships from" in var_name.lower():
                #print("found")
                value_list = prop_dict["Value"]
                #print(value_list)
                ship_var_index = i
                new_value_list = []
                for value_dict in value_list:
                    value_name = value_dict["Value_Name"]
                    if "china" in value_name.lower():
                        new_value_list.append(value_dict)
                        china_id = value_dict["Value_Id"]
                prop_dict["Value"] = new_value_list
                ship_var_index = i
            i += 1

        # deleting from sku combinations list
        new_sku_price_list = []
        if ship_var_index != None: # if we have a ships from option
            for sku_list in skuPriceList:
                shipping_option_dict = sku_list[ship_var_index]
                if shipping_option_dict["Value_Id"] == china_id:
                    sku_list.remove(shipping_option_dict)
                    new_sku_price_list.append(sku_list)

            skuPriceList = new_sku_price_list
            productSKUPropertyList.pop(ship_var_index)
        try:

            print("ProductSKUpro", productSKUPropertyList)

            print("VariationPictures", variationPictures)

            print("Skuproce", skuPriceList)

        except:
            pass

    return (title, images_list, price_value, listing_has_variations, listing_has_var_images, productSKUPropertyList, variationPictures, skuPriceList)

#return_response()
#return_response("https://www.aliexpress.com/item/4001041839357.html?spm=a2g0s.9042311.0.0.6af74c4dYdrOMu")
response = return_response("https://www.aliexpress.com/item/32994596152.html?spm=a2g0o.productlist.0.0.f4d75b0adI9yvI&algo_pvid=8492daee-efd4-4294-aafc-ac99754406d5&algo_expid=8492daee-efd4-4294-aafc-ac99754406d5-1&btsid=0bb0623f16063141935796037ec3ae&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_")
