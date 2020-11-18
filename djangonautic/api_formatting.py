from selenium_multiple_variatios_test import title, variations, shipping_dict, images_list, combinations_final

'''Formatting pulled items to put into the additem call'''
main_pictures = images_list
#title = "FRAMVIO 30x40 cm Photo Frame Metal Matte Plexiglass Black White Posters Print Picture Wall Art Frames Canvas Painting Home Decor"
title_fr = ""
if title[80] == " ":
    title_fr = title[:80]
else:
    print(title)
    rev = title[:80][::-1]
    print(rev)
    i = rev.index(" ")
    print(i)
    i_fr = 79-i
    title_fr = title[:i_fr]
    print("Final title:", title_fr)

''' Formatting combiantions'''
#combinations_final = [[('bla', 'White Frame'), ('bla', '30x40cm'), 'US $13.87'], [('bla', 'Black Frame'), ('fefw', '30x40cm'), 'US $13.87']]
combinations = []

#print("combina", combinations_final)
for li in combinations_final:
    single_comb = []
    # li element is formatted like this:
    # [(WebElement of option1, option1), (WebElement of option2, option2), price in "US $0.00" format]
    # we are changing it to something readable
    for i in range(len(li)-1):
        elt = li[i]
        single_comb.append(elt[1])
    if type(li[-1]) != tuple:
        final_elt = float(li[-1][4:])
        if final_elt < 0.99:
            final_elt = 0.99
        single_comb.append(final_elt) # last one is price in "US $13.87", we change it to float
        combinations.append(single_comb)
print(combinations)

variation_1 = []

'''Getting variationSpecificPictureSet'''

# variationSpecificPictureSet only exists if we had variation images
# in the Aliexpress product that we copied.
# If this is the case, we saved a URL link
# of the image of the variation to every
# variation value

var_dict = {}
for key, value_list in variations.items():
    var_dict[key] = [x[1:] for x in value_list]
print("var disct", var_dict)

var_pics_exist = False

variationSpecificPictureSet = []
for var_name, value_list in var_dict.items():
    #checking if this variation had images
    elt = value_list[0]
    if len(elt) == 2:
        var_pics_exist = True
        variationSpecificName = var_name[0].upper() + var_name[1:var_name.index(":")]
        for val_tuple in value_list:
            var_value = val_tuple[0]
            var_URL_small = val_tuple[1]
            var_URL = var_URL_small.replace(".jpg_50x50", "")
            value_URL_pair = {
                "VariationSpecificValue": var_value,
                "PictureURL": var_URL
            }
            variationSpecificPictureSet.append(value_URL_pair)


#variations = {'color:': [('bla', 'White Frame'), ('bla', 'Black Frame')], 'size: 30x40cm': [('bla', '30x40cm')]}

'''Getting Variation containers'''
names = list(variations.keys())
print("names:", names)
for var in combinations:
    #getting quantity
    if len(var) == 3:
        quantity = 1
    else:
        quantity = 0

    #getting name-value lists
    nameValueList = []
    for i in range(len(var)-1):
        name = names[i]
        formatted_name = name[0].upper() + name[1:name.index(":")]
        value = var[i]
        nameValuePair = {"Name": formatted_name, "Value": value}
        nameValueList.append(nameValuePair)

    #getting price
    if len(var) == 3:
        startPrice = var[-1]
    else:
        startPrice = 0.00

    this_variation = {
             "VariationSpecifics": {"NameValueList": nameValueList},
             "Quantity": quantity,
             "StartPrice": startPrice
         }
    variation_1.append(this_variation)



formatted_vars = {}
for name, value_list in variations.items():
    vals = []
    for tup in value_list:
        vals.append(tup[1])

    short_name = name[0].upper() + name[1:name.index(":")]
    formatted_vars[short_name] = vals


variationSpecificsSet = {"NameValueList": []}

for name, value_list in formatted_vars.items():
    variationSpecificsSet["NameValueList"].append({"Name": name, "Value": value_list})



print("variationSpecificcsSet:", variationSpecificsSet)
print("variatioj", variation_1)