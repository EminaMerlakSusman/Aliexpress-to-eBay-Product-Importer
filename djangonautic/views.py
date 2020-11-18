from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
import sys
from djangonautic.forms import HomeForm
import _sqlite3
import os.path
from djangonautic.models import *
from djangonautic.models import Page
import json
import celery
# from djangonautic.savbrb import bla
import redis


def homepage(request):
    progress = None
    var_names = []  # this is later needed while saving SKU combinations
    var_values = {}
    if request.method == "POST" and "btn" in request.POST:
        print("request values")
        form = HomeForm(request.POST)
        if form.is_valid():
            print("Form was valid")
            text = form.cleaned_data['post']
            args = {'form': form, 'text': text}

            from djangonautic.raw_html_test import return_response
            progress = 'making api call'

            (title, images_list, price_value, listing_has_variations, listing_has_var_images, productSKUPropertyList,
             variationPictures, skuPriceList) = return_response(text) # calling function to import product

            thumbnail_image_url = images_list[0]
            print(images_list[0])
            product_data = Product(productURL=text, title=title, thumbnail_image_url=images_list[0],
                                   price=skuPriceList[0][-1]["price"])
            product_data.save()
            database_list = Product.objects.all().latest('id')
            formatted_images_list = ""
            for x in images_list:
                formatted_images_list += x + " "
            formatted_images_list = formatted_images_list
            progress = "saving images..."
            print(progress)

            # adding images to productImages model

            for url in formatted_images_list.split():
                url = ProductImage(product=product_data, imageURL=url)
                url.save()
            images_list_from_db = ProductImage.objects.all().filter(product=Product.objects.all().latest('id'))

            progress = "done..."
            print(progress)

            # Adding variations

            if listing_has_variations:
                for var_dict in productSKUPropertyList:
                    var_name = var_dict["Name"]

                    variation_name_data = Variation(product=product_data,
                                                    variation_name=var_name)  # this is where we save color, size, etc
                    variation_name_data.save()
                    var_names.append(variation_name_data)
                    var_values[var_name] = []
                    values = var_dict["Value"]
                    for val_dict in values:
                        val = val_dict["Actual_Name"]
                        val_data = VariationValue(product = product_data, variation_name=variation_name_data,
                                                  value=val)  # for example "blue, red", and "small, medium"
                        val_data.save()
                        var_values[var_name].append(val_data)
                        # var_names[variation_name_data] += val_data  # needed for SKU combos

            progress = "saving combinations..."  # where the foreign keys would be: color, size
            print(progress)

            # Saving SKU combinations into database
            combo_list_db = []
            if listing_has_variations:
                k = 0
                for combo_list in skuPriceList:
                    price_dict = combo_list[-1]
                    sku = price_dict["sku"]
                    price = price_dict["price"]

                    combo = VariationCombination(product = product_data, sku=sku, price=str(price))
                    combo.save()

                    '''Logging progress'''
                    full = len(skuPriceList)
                    prog = full // (k + 1)
                    print(str(prog) + "% done")
                    k += 1
                    #print(combo_list)
                    for i in range(len(combo_list[:-1])):
                        var_dict = combo_list[i]
                        one_of_vars_text = var_dict["Value_Name"]  # ie "blue"
                        # getting the actual database object of this variation value
                        current_var_type = var_names[i]
                        current_var_value_query = VariationValue.objects.all().filter(
                                                                                      product = product_data,
                                                                                      variation_name=current_var_type,
                                                                                      value=one_of_vars_text
                                                                                      )
                        if len(current_var_value_query) > 1:
                            raise Exception("There was an internal error")
                        else:
                            current_var_value = current_var_value_query[0]  # cause the query returns a list



                        combo.variation_name.add(current_var_type)

                        combo.variation_value.add(current_var_value)

                print("variation pics", listing_has_var_images ,variationPictures)

                # saving variation images to database
                if listing_has_var_images:
                    print("listing had var images", variationPictures)
                    var_name = list(variationPictures.keys())[0]
                    value_list = variationPictures[var_name]

                    # finding matching variation name and product in database
                    matching_product = product_data
                    matching_var_name = Variation.objects.get(product=matching_product, variation_name=var_name)

                    for val_dict in value_list:
                        value_name = val_dict["Actual_Name"]
                        pictureURL = val_dict["PictureURL"]

                        # Finding matching variation value
                        # in database
                        matching_value = VariationValue.objects.get(product = matching_product, value = value_name)

                        # Creating Variation Picture object

                        new_obj = VariationPictures(
                                                    product = matching_product,
                                                    variation_name = matching_var_name,
                                                    value = matching_value,
                                                    imageURL = pictureURL
                                                    )
                        new_obj.save()





            #print("Variation valueas", var_values)

            context = {'object': database_list, 'images': images_list_from_db, 'rating': 4.3, 'product': product_data,
                       'variation_names': var_names, 'variation_values': var_values, 'combinations': combo}
            return redirect('/product_info')

    else:  # this was an initial page load
        print("check false")
        form = HomeForm()
        return render(request, "homepage.html", {'form': form, 'text': 'bla'})


def product_info(request):
    if request.method == "GET" and not request.is_ajax():
        '''Get product info from database'''
        print("request was not ajax")
        product = Product.objects.all().latest("id")
        images_list_from_db = ProductImage.objects.all().filter(product=product)
        var_names = Variation.objects.filter(product=product)
        var_values = {}
        for var_type in var_names:
            var_name = var_type.variation_name
            var_values[var_name] = []
            val_list = VariationValue.objects.filter(variation_name = var_type)
            for val_obj in val_list:
                var_values[var_name].append(val_obj)  # for example "blue, red", and "small, medium"

        context = {'object': product, 'images': images_list_from_db, 'rating': 4.3, 'product': product,
                   'variation_names': var_names, 'variation_values': var_values}

        return render(request, "product_info.html", context=context)

    elif request.is_ajax() and request.GET['action'] == 'options_chosen' and request.method == "GET":

        check = True
        print(request.is_ajax())

        '''When a user chooses a product variant on the page, this makes an ajax call
        to retrieve the price of this combination'''

        print("request was ajax")

        combinations = request.GET["alltext"]
        combinations_list = combinations.split(";")
        print("conbinafiosbn", combinations_list)
        product = Product.objects.all().latest("id")

        var_names = list(Variation.objects.filter(product=product))
        print("var_names", var_names)
        corresponding_values = []
        for i in range(len(combinations_list)):
            # finding this variant in database

            var_name = var_names[i]
            print("var_name", var_name)
            var_values = VariationValue.objects.filter(variation_name=var_name)
            print("var values", var_values)
            for val_obj in var_values:
                print("val obj", val_obj)
                val = val_obj.value
                print(str(combinations_list[i]).strip())
                if str(val) == str(combinations_list[i]).strip():
                    corresponding_values.append(val_obj)

        found_price = None
        for i in range(len(corresponding_values)):
            val = corresponding_values[i]
            if i == 0:
                combo_query = VariationCombination.objects.filter(variation_value=val)
            else:
                combo_query = combo_query.filter(variation_value=val)

        price = combo_query[0].price

        '''Fetches the URL of a variation image (if it exists) to display once the
                variation value is clicked'''

        corresponding_var_pics = VariationPictures.objects.filter(product=product)
        var_name = corresponding_var_pics.latest("id").variation_name # they all have the same variation name
        ind = var_names.index(var_name)
        print("var_names index car_name", ind)
        value_list = []
        print("corresponding values", corresponding_values)
        val_obj = corresponding_values[ind]
        var_value_list = VariationPictures.objects.filter(product=product, variation_name = var_names[ind], value = val_obj)
        print(var_value_list)
        value_list = var_value_list

        print("value list", value_list)
        imageURL = value_list[0].imageURL

        data = {
                'price': price,
                'image_url': imageURL
        }
        return JsonResponse(data)

    elif request.is_ajax() and request.GET['action'] == 'test_call' and request.method == "GET":

        '''Fetches the URL of a variation image (if it exists) to display once the
        variation value is clicked'''

        return HttpResponse("Success!")




def get_progress(request, task_id):
    result = celery.result.AsyncResult(task_id)
    response_data = {
        'state': result.state,
        'details': result.info,
    }
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def about(request):
    # return HttpResponse("about")
    return render(request, "about.html")
