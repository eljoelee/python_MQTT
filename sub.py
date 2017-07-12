# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import time

#MongoDB 연결
db_client = MongoClient()
db = db_client.temp

broker = "IPAddress"

def on_connect(client, userdata, rc):
    print("Connect with result code "+str(rc))
    client.subscribe("temp")
    client.subscribe("dust")
    client.subscribe("discom")

def on_message(client, userdata, msg):
    if msg.topic == 'temp':
        #msg.topic : MQTT Key
        #msg.payload : MQTT Value
        print('Topic : '+str(msg.topic)+' payload : ', end="");print(float(msg.payload))

        #현재 시간 가져오기
        now = time.localtime()

        #YYYY-MM-DD HH:MM
        s = "%04d-%02d-%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)

        #DB connection에 보낼 값을 JSON 형태로 작성
        temp_post = {"temp":float(msg.payload),
                    "date":s}

        #DB table 접근
        temp_posts = db.temp_posts

        temp_posts.insert_one(temp_post)
    elif msg.topic == 'dust':
        print('Topic : '+str(msg.topic)+' payload : ', end="");print(int(msg.payload))

        now = time.localtime()

        s = "%04d-%02d-%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)

        dust_post = {"dust": int(msg.payload),
                     "date": s}

        dust_posts = db.dust_posts

        dust_posts.insert_one(dust_post)
    else :
        print('Topic : ' + str(msg.topic) + ' payload : ', end="");print(int(msg.payload))

        now = time.localtime()

        s = "%04d-%02d-%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)

        discom_post = {"discomfort": int(msg.payload),
                     "date": s}

        discom_posts = db.discom_posts

        discom_posts.insert_one(discom_post)

#MQTT Connect & Message Subscribe
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)
client.loop_forever()