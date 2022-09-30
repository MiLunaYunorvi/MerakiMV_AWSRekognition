from time import sleep
import requests
import urllib.request
from PIL import Image
from io import BytesIO
import json

############### PARAMETROS PARA LLENAR ##############################
api_key = ''
mv_serial = ''
token_bot = ''
room_id = ''
COLLECT_NAME = 'ROSTROS'  #cambiar el nombre si se uso uno diferente al momento de crear la colección
######################################################################

global url_snap
def snapshot():
    global url_snap
    url = "https://api.meraki.com/api/v1/devices/{}/camera/generateSnapshot".format(mv_serial)
    payload = '''{
        "fullframe": true
    }'''
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Cisco-Meraki-API-Key": api_key
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
    "roomId": room_id,
    "text": mensaje,
    "files": [url_snap]
    })
    headers = {
    'Authorization': 'Bearer {}'.format(token_bot),
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