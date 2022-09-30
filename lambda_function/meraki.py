from time import sleep
import requests
import urllib.request
from PIL import Image
from io import BytesIO
import json

global url_snap

def snapshot():
    global url_snap
    url = "https://api.meraki.com/api/v1/devices/Q2GV-2V9V-NMDF/camera/generateSnapshot"
    payload = '''{
        "timestamp": "2022-09-29T10:39:31Z",
        "fullframe": false
    }'''
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": "771d04c7ce12516c5146a80cc17826d53bebc706"
    }
    response = requests.request('POST', url, headers=headers, data = payload)
    print(response.json())
    url_snap = (response.json())['url']
    print((response.json())['url'])
    return url_snap

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
    print("Enviando a Webex: ", mensaje)
    global url_snap
    url_webex = "https://webexapis.com/v1/messages"
    payload = json.dumps({
    "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vOWQ4NmVlNzAtMWE3ZS0xMWVjLTliNzAtNTM1NjYyZTVkYzIz",
    "text": mensaje,
    "files": [url_snap]
    })
    headers = {
    'Authorization': 'Bearer YTg4OTVmYjktNWFkZS00YzA4LWFkNWItMjE5YTJkZDM1MjNmY2ZjOTFlZGItYmE1_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url_webex, headers=headers, data=payload)
    print("Mensaje enviado a Webex? : ",response)

def formato_webex(mensaje):
    cadena = 'Se ha(n) encontrado a las siguiente(s) persona(s)\n'
    for i in mensaje:
        cadena = cadena + i[0] + ' al ' + str(round(i[1],1)) + '\n'
    print(cadena)
    return cadena