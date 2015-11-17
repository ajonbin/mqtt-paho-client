#!/usr/bin/python
import re
import os
import sys
import time
from datetime import datetime, tzinfo, timedelta
import getopt
import json
import paho.mqtt.client as mqtt
from uuid import getnode as get_mac
import socket
import struct


REPORT_INTERVAL=60
MQTT_HOST=""
MQTT_TITLE=""
MQTT_USERNAME=""
MQTT_PASSWORD=""
MQTT_MSG="Msg from mqtt-publisher"
MQTT_QOS=0
MQTT_CLIENT_ID=""

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    print(mid)

def on_log(client, userdata, level, buf):
    print "%d: %s"%(level,buf) 

def on_disconnect(client, userdata, rc):
    print "Disconncted: " + str(rc)  
    
def usage():
    print 'Collect Endpoint Data and Send To MQTT Broker'
    print '\t-h, --help:     print help message.'
    print '\t-i, --interval: publish data interval, in seconds, default is 60s. 0 means only once'
    print '\t-b, --broker:   MQTT broker'
    print '\t-t, --topic:    MQTT topic'
    print '\t-u, --username: Username'
    print '\t-p, --password: Password'
    print '\t-m, --message:  Message to publish'
    print '\t-q, --qos:      QoS'
    print '\t-d, --client-d: Client ID'


def main(argv):
    
    global REPORT_INTERVAL,MQTT_HOST,MQTT_TITLE,MQTT_USERNAME,MQTT_PASSWORD,MQTT_MSG,MQTT_QOS,MQTT_CLIENT_ID
    try:
        opts, args = getopt.getopt(argv[1:], 'hi:b:t:u:p:m:q:d:', ['help','interval=', 'broker=', 'topic=','username=','password=','message=','qos=','client-id='])
    except Exception as err:
        print str(err)
        usage()
        sys.exit(2)
        
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
        elif o in ('-b', '--broker'):
            MQTT_HOST = a
        elif o in ('-i', '--interval'):
            REPORT_INTERVAL = a
        elif o in ('-t', '--topic'):
            MQTT_TITLE = a
        elif o in ('-u', '--username'):
            MQTT_USERNAME = a
        elif o in ('-p', '--password'):
            MQTT_PASSWORD = a
        elif o in ('-m', '--message'):
            MQTT_MSG = a
        elif o in ('-q', '--qos'):
            MQTT_QOS = int(a)
        elif o in ('-d', '--client-id'):
            MQTT_CLIENT_ID = a
        else:
            print 'unhandled option'
            sys.exit(3)
 
    client = mqtt.Client(client_id=MQTT_CLIENT_ID)
    if(MQTT_USERNAME != ""):
      client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    client.on_publish = on_publish
    client.on_log = on_log
    client.on_disconnect = on_disconnect
    #client.max_inflight_messages_set(1)
    client.connect(MQTT_HOST,1883,60)
    index = 0;
    while(True):                           
        client.publish(MQTT_TITLE,MQTT_MSG,qos=MQTT_QOS)
        #dict1 = {'counter':1111, 'x': 7, 'y': '7','z':9}
        #client.publish(MQTT_TITLE,dict1,qos=MQTT_QOS)
        #!!!! Must Call loop(), otherwise PUBACK will not be recived !!!
        client.loop()
        if int(REPORT_INTERVAL) == 0:
            break
        else:
            time.sleep(int(REPORT_INTERVAL))
        index += 1

if __name__ == "__main__":
    main(sys.argv)
