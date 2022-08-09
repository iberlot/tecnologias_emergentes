from ast import main
import paho.mqtt.client as mqtt
import time
import httpx
import asyncio
import json
import mysql.connector
from queue import Queue

queueData = Queue()

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
	# print("message received " ,str(message.payload.decode("utf-8")))
	#archivo-salida.py

	json_object = json.loads(str(message.payload.decode("utf-8")))

	conexion1=mysql.connector.connect(host="tecnologias_emergentes_db_1", port="3306", user="usuario", passwd="1234", database="te_pilar_grp_1")
	cursor1=conexion1.cursor()
	sql="INSERT INTO temp (temp, humidity, location_id) VALUES (%s,%s,%s)"
	datos=(json_object["temp"], json_object["humidity"], json_object["location_id"])
	cursor1.execute(sql, datos)
	conexion1.commit()
	conexion1.close()  

 
	f = open ('log.txt','a')
	f.write(sql)
	f.write("\n")
	f.close()
	
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
	# client.publish("clima","OFF")
	time.sleep(4) # wait
	client.loop_stop()
    
	# print("never scheduled!")

async def main():

	while True:
		await test()
		# await add(str(client.on_message))

asyncio.run(main())
