from time import sleep
import requests
import urllib.request
from PIL import Image
from io import BytesIO
import json

api_key = ''
mv_serial = ''

def snapshot():
    url = "https://api.meraki.com/api/v1/devices/{}/camera/generateSnapshot".format(mv_serial)
    payload = '''{
        "fullframe": false
    }'''
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api_key
    }
    response = requests.request('POST', url, headers=headers, data = payload)
    url = (response.json())['url']
    print((response.json())['url'])
    return url

def open_image(url):
    sleep(0.5)
    #urllib.request.urlretrieve(url,'imagen.png')
    response = requests.get(url)
    bytes = response.content
    return bytes                          
    #img = Image.open(BytesIO(response.content))
    #img.show()
    #return(img)


def webex(mensaje):
    url_webex = "https://webexapis.com/v1/messages"
    mensaje_f = formato_webex(mensaje)
    payload = json.dumps({
    "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vOWQ4NmVlNzAtMWE3ZS0xMWVjLTliNzAtNTM1NjYyZTVkYzIz",
    "text": mensaje_f
    #"files": ["{}".format(url)]
    })
    headers = {
    'Authorization': 'Bearer YTg4OTVmYjktNWFkZS00YzA4LWFkNWItMjE5YTJkZDM1MjNmY2ZjOTFlZGItYmE1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f',
    'Content-Type': 'application/json'
    }
    requests.request("POST", url_webex, headers=headers, data=payload)

def formato_webex(mensaje):
    cadena = 'Se ha(n) encontrado a las siguiente(s) persona(s)\n'
    for i in mensaje:
        cadena = cadena + i[0] + ' al ' + str(round(i[1],1)) + '\n'
    print(cadena)
    return cadena