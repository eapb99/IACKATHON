import datetime

import pandas as pd
import json

df = pd.read_csv('dbProcurement.Contract.csv')
c = 0
with open('dbProcurement.Contract.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
import requests
import queue
import time

q = queue.Queue()
for i in df['ocid']:
    q.put(i)

# Mientras la cola no esté vacía
new_items = []
print(datetime.datetime.now())
while not q.empty():
    i = q.get()
    filtered_objects = [obj for obj in data if obj.get("ocid") == i]
    response = requests.get(f'https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/record?ocid={i}')
    time.sleep(1)
    try:
        datos = response.json()["releases"][0]
        auctions = datos["auctions"]
        amount = datos["tender"]['lots'][0]['value']['amount']
        lista = auctions[0]['stages'][0]
        bid_amount = []
        ruc_list = []
        date_list = []
        d = filtered_objects[0]

        entidad = d['entity_name']
        condicion = "DIRECCION DISTRITAL" in entidad or \
                    "DIRECCIÓN DISTRITAL" in entidad or \
                    "DIRECION DISTRITAL" in entidad or \
                    "COORDINACION ZONAL" in entidad or \
                    "COORDINACIÓN ZONAL" in entidad

        if not condicion:
            pos = data.index(filtered_objects[0])
            for value in lista["bids"]:
                bid_amount.append(value['value']['amount'])
                date_list.append(value['date'])
                ruc_list.append(value['tenderers'][0]['id'])
            d['bids_amounts'] = bid_amount
            d['amount_planning'] = amount
            d['bidders_ruc'] = ruc_list
            d['date_list'] = date_list
            d['num_bids'] = len(bid_amount)
            new_items.append(d)

    except Exception as e:
        q.put(i)

with open("dbProcurementNew4.json", 'w') as json_file:
    json.dump(new_items, json_file, indent=4)

print(datetime.datetime.now())
