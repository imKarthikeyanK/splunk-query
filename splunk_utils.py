import urllib
from splunklib.six import moves
from xml.etree import ElementTree

# HOST = ""
# PORT = ""
# USERNAME = ""
# PASSWORD = ""

def query_splunk(host, port, username, password, query, range):
    connection = moves.http_client.HTTPSConnection(host, port)
    body = urllib.urlencode({
        'username': username, 
        'password': password
        })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(body)),
        'Host': host,
        'Accept': "*/*"
    }

    try:
        connection.request("POST", "/services/auth/login", body, headers)
        response = connection.getresponse()
    finally:
        connection.close()

    if response.status != 200:
        raise Exception("%d (%s)" % (response.status, response.reason))

    body = response.read()

    print(body)
    session_key = ElementTree.XML(body).findout("./sessionKey")
    print(session_key)
