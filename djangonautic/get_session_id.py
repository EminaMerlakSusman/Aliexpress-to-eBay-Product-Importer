from urllib.request import urlopen

from ebaysdk.trading import Connection
import requests
import xml.etree.ElementTree as ET
import urllib

api = Connection(config_file=config_file)


def get_session_id():
    '''Establishing API conncetion
     Making GetSessionID call to get session ID of the user who logged in'''
    request = {
        'RuName': ruName,

    }

    sess_id_response = api.execute('GetSessionID', request)

    # parsing response
    root = ET.fromstring(sess_id_response.text)

    session_ID = root[4].text

    return session_ID


def get_token(session_ID):
    '''Exchanging user's SessionID for a token'''



    data = {
        'SessionID': session_ID

    }

    #
    token_response = api.execute('FetchToken', data)

    # parsing response
    root = ET.fromstring(token_response.text)
    #
    token = root[4].text

    return token
