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
MQTT_CLIENT_ID=""
MQTT_CLEAN_SESSION=True
MQTT_QOS=0

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_connect(client, userdata, flags, rc):
    global MQTT_QOS
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TITLE,qos=MQTT_QOS)
def on_disconnect(client, userdata, rc):
    print "Disconncted: " + str(rc) 

def on_subscribe(client, userdata, mid, granted_qos):
    print "On Subscribed: qos = %d" % granted_qos

def on_log(client, userdata, level, buf):
    print "%s: %s"%(level,buf)

def usage():
    print 'Collect Endpoint Data and Send To MQTT Broker'
    print '\t-h, --help:          print help message.'
    print '\t-b, --broker:        MQTT broker'
    print '\t-t, --topic:         MQTT topic'
    print '\t-u, --username:      Username'
    print '\t-p, --password:      Password'
    print '\t-d, --client-id:     Client ID'
    print '\t-c, --clean-session: Clean Session (Default is True)'
    print '\t-q, --qos:           QoS'


def main(argv):
    
    global MQTT_HOST,MQTT_TITLE,MQTT_USERNAME,MQTT_PASSWORD,MQTT_CLIENT_ID,MQTT_CLEAN_SESSION,MQTT_QOS
    try:
        opts, args = getopt.getopt(argv[1:], 'hb:t:u:p:d:c:q:', ['help', 'broker=', 'topic=','username=','password=','client-id=','clean-session=','qos='])
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
        elif o in ('-t', '--topic'):
            MQTT_TITLE = a
        elif o in ('-u', '--username'):
            MQTT_USERNAME = a
        elif o in ('-p', '--password'):
            MQTT_PASSWORD = a
        elif o in ('-d', '--client-id'):
            MQTT_CLIENT_ID = a
        elif o in ('-c', '--clean-session'):
            if(a == "False") or (a == "false"):
                MQTT_CLEAN_SESSION = False
        elif o in ('-q', '--qos'):
            MQTT_QOS = int(a)
        else:
            print 'unhandled option'
            sys.exit(3)
    print 'client-id = ' + MQTT_CLIENT_ID
    client = mqtt.Client(client_id=MQTT_CLIENT_ID,clean_session=MQTT_CLEAN_SESSION)
    if(MQTT_USERNAME != ""):
      client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_log = on_log
    client.connect(MQTT_HOST,1883,60)

    client.loop_forever()

if __name__ == "__main__":
    main(sys.argv)
