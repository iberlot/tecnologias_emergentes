from ast import main
import paho.mqtt.client as mqtt
import time
import httpx
import asyncio
from queue import Queue

queueData = Queue()

# def on_message(client, userdata, message):
# 	datos = str(message.payload.decode("utf-8"))
# 	datosConv = datos.split('#')
# 	data = {"temperatura": float(datosConv[0]), "humedad": float(datosConv[1]), "ubicacion": str(datosConv[2])}
# 	queueData.put(data)
# 	print("Mensaje recibido: ", datos)

# def on_connect(client, userdata, flags, rc):
# 	print("Conectado, codigo: " + str(rc))
# 	client.subscribe("Registros")

async def add(data):
	async with httpx.AsyncClient() as client:
# 		res = await client.post("http://localhost/temp/{temp}/{humidity}/{location_id}")
 		print(data.json())

# while True:
# 		# await add(queueData.get())
# 	print(queueData.get())



def on_log(client, userdata, level, buf):
    print("log: ",buf)



############
def on_message(client, userdata, message):
	print("message received " ,str(message.payload.decode("utf-8")))
	
	
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)
########################################

async def test():
	broker_address="192.168.10.50"
	client = mqtt.Client("P1")
	client.on_log=on_log
	client.on_message=on_message
	client.connect(broker_address)
	client.loop_start()
	client.subscribe("clima")
	client.publish("clima","OxFxF")
	time.sleep(4) # wait
	client.loop_stop()
    
	# print("never scheduled!")

async def main():

	while True:
		await test()
		# await add(str(client.on_message))

asyncio.run(main())
