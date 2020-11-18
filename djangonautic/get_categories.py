from djangonautic import raw_html_test
import xml.etree.ElementTree as ET
from ebaysdk.trading import Connection

def get_suggested_categories(query, config_file):
    '''Getting suggestet categories'''
    title = query
    #title = raw_html_test.return_response(url)[0]
    api = Connection(domain='api.ebay.com', appid="EminaMer-testing-PRD-2e6527e18-557772c0", devid = "09ea5789-88e8-49dd-9491-8d50ebdc9fd4",
                     certid = "PRD-e6527e1828b8-ed34-423d-956f-2792", token = "AgAAAA**AQAAAA**aAAAAA**IlWIXw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AClYClAJOHoQWdj6x9nY+seQ**6X4GAA**AAMAAA**o6WOvjJT/9a6cQuSffJ9t9+6RqpitvABF28T5qWZEryYEADlqbm1jwcYT8nWAfj/6I17cL1gd0Glz6rdTVjdq9LbLn+Oj44z511aY6nP6Sndj8i4OC9LghdVQDCNAgm0HoMwKVblLBEFAslNvRxJhaY+id9EGiOF7EMBRb6UZCchRaJmlWrqN0/8ygEOvsqU1dBROwbag3OFKpnDa9rfgQcUJiSzOft/+dkBZI52JlmCzsNP02aNg802KK5IzYplpWVQKgyKQT6wF60SIlPyGJQn4FaerK4XzrfFQRA3CEkq9gmkDDvBpPUQRLll+6VULWYnvvYtx6lBvrnEYtl3ISOUIkFTxzfI5vPXvVPNBfrofqL0BcKekm03mh9oPVkVdkg+GX/ZEYLOo9GCUTyx3wBWaZqoVQUYX2IUYB+cwHOea2f7qAuP9/cUFM58+xb57+Qve1fujnnoXTFX4MAroo1WwZp1Y5RMTmgfReF8lowElFgSajYXVkA7FbCzImyZKsSdKFel4WdAgTgbK0LA71p+X4mmLyheIlDOFesqB+ZqOD64rC992XPcoqDRjiuUjRcdAs8/BG9PYRksvcOFQNyuM1njowOcd0QmZJdlB4xDFnzzyGrSZJt2qdHlkvhWLnNzop1KThiAhEeozEzcgV9DgiSGmCs9+ZcoY/lZ8bsESlSb28+Rgedi3TQ7pHPnD5jqVkr4OJQ+9ZkqY52f2zMpYDFKte8m2FwL+M+fNHr9UzeqUq3SCXWLOzjICBPq", config_file=config_file, debug=True)
    #print(title)
    #getting rid of any special characters in title to avoid errors with the query
    # cleaned_title = ''
    # for char in title:
    #     if char.isalnum() or char == ' ':
    #         cleaned_title += char

    #print(cleaned_title)

    request = {
        "Query": title,
    }
    #call = api.execute('ValidateTestUserRegistration', request)
    response = api.execute('GetSuggestedCategories', request)
    #print(response.text)
    root = ET.fromstring(response.text)
    suggested_cat_array = root[4]
    suggested_cat_list = []
    children = suggested_cat_array[0][0]
    name = children[1].text
    cateid = children[0].text
    #print(response.text.find())
    print(str(name))
    print(id)
    #print(sug_category)
    diff = 2 + int((len(children) - 2)/2)
    parents = []
    for k in range(diff, len(children)):
       elt = children[k]
       parent = str(elt.text).encode('iso-8859-1').decode('utf8')
       parents.append(parent)
        #name = category.find('CategoryName').text
        #print(name)
    category_path = "/".join(list(reversed(parents))) + "/" + name
    return (category_path, cateid)

# get_suggested_categories(query = "https://www.aliexpress.com/item/4001155636952.html?spm=a2g0o.productlist.0.0.448e413dN6SAhP&algo_pvid=838dab60-bf9f-4bc9-9a16-8b0dd7656a47&algo_expid=838dab60-bf9f-4bc9-9a16-8b0dd7656a47-9&btsid=0bb0622f16027692419813645ecfb0&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
# , config_file=None)