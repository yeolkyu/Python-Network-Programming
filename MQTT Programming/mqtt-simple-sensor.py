#! python3.6
#Simple Light or door type Sensor that can receive control Information to change state

import paho.mqtt.client as mqtt
import json
import os
import time
import logging,random,os
from mqtt_functions import *

options=dict()
brokers=["192.168.1.15","test.mosquitto.org",\
         "broker.hivemq.com","iot.eclipse.org"]
options["broker"]=brokers[1]
options["port"]=1883
options["verbose"]=False
options["username"]=""
options["password"]=""
options["cname"]=""
options["sensor_type"]="light"
options["topic_base"]="sensors"
options["interval"]=10 #loop time when sensor publishes in verbose
options["interval_pub"]=25 # in non chatty mode publish
# status at this interval if 0 then ignore
options["keepalive"]=120
options["loglevel"]=logging.ERROR
cname=""
QOS0=0

mqttclient_log=False

username=""
password=""

chatty=False
interval=2 #loop time when sensor publishes
sensor_pub_interval=300 # how often to publish if status is unchanged

def command_input(options):
    topics_in=[]
    qos_in=[]

    valid_options=" -b <broker> -p <port>-t <topic> -q QOS -v <verbose yes/no> -h <help>\
-c <loop Time secs -d logging debug  -n Client ID or Name -i loop Interval\
-s <set states to open and closed> -u Username -P Password"
    print_options_flag=False
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hb:i:dk:p:t:q:l:vsn:r:u:P:")
    except getopt.GetoptError:
      print (sys.argv[0],valid_options)
      sys.exit(2)
    qos=0

    for opt, arg in opts:
        if opt == '-h':
            print (sys.argv[0],valid_options)
            sys.exit()
        elif opt == "-b":
             options["broker"] = str(arg)
        elif opt == "-i":
             options["interval"] = int(arg)
        elif opt == "-k":
             options["keepalive"] = int(arg)
        elif opt=="-r":
            options["topic_base"]=str(arg)
        elif opt =="-p":
            options["port"] = int(arg)
        elif opt =="-t":
            topics_in.append(arg)
        elif opt =="-q":
             qos_in.append(int(arg))
        elif opt =="-n":
             options["cname"]=arg
        elif opt =="-d":
            options["loglevel"]=logging.DEBUG
        elif opt =="-v":
            options["verbose"]=True
        elif opt =="-s":
            print("here")
            options["sensor_type"]="door"
        elif opt == "-P":
             options["password"] = str(arg)
        elif opt == "-u":
             options["username"] = str(arg)        

        

    lqos=len(qos_in)
    for i in range(len(topics_in)):
        if lqos >i: 
            topics_in[i]=(topics_in[i],int(qos_in[i]))
        else:
            topics_in[i]=(topics_in[i],0)
            
        
    if topics_in:
        options["topics"]=topics_in

def run_loop(client,broker,port,topics,keepalive,loop_function=None,\
             interval=1,run_forever=False):
    """runs a loop that will auto reconnect and subscribe to topics
    pass topics as alist of tuples
    """
    client.run_flag=True
    no_sub_flag=False
    sub_count=0
    #print("running loop")
    if topics=="": #not subscribing
        no_sub_flag=True
    while client.run_flag: #loop forever

        if client.bad_connection_flag:
            break         
        if not client.connected_flag:
            if Connect(client,broker,port,keepalive,run_forever) !=-1:
                if not wait_for(client,"CONNACK"):
                   client.run_flag=False #break
            else:
                client.run_flag=False #break
        if not no_sub_flag and not client.subscribe_flag and client.connected_flag:
            if subscribe_topics(client,topics)!=-1 and check_subs(client):
                client.subscribe_flag=True
                sub_count=0
                        
            else:# try 3 times to subsribe then quit
                sub_count+=1;
                if sub_count>3:
                    client.run_flag=False

        client.loop(.01)

        if client.connected_flag and loop_function and client.subscribe_flag: #function to call
                loop_function(client) #call function
        #time.sleep(interval)
    client.disconnect()
    client.connected_flag=False

##callback all others defined in mqtt-functions.py

def on_message(client,userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    logging.debug("Message Received "+m_decode)
    process_message(client,m_decode,topic)

def process_message(client,msg,topic):
    if topic==topic_control: #got control message
        print("control message ",msg)
        update_status(client,msg)
    
def on_connect(client, userdata, flags, rc):
    logging.debug("Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id")
    if rc==0:
        client.connected_flag=True
        client.publish(connected_topic,1,retain=True)
    else:
        client.bad_connection_flag=True  
 
def update_status(client,status):
    status=status.upper()
    print("updating status",status)
    if status==states[0] or status==states[1]: #Valid status
        client.sensor_status=status #update
        print("updating status",client.sensor_status)

def publish_status(client):
    global start_flag
    pubflag=False
    if start_flag:
        start_flag=False
        pubflag=True
    if time.time()-client.last_pub_time >=options["interval_pub"]:
        pubflag=True
    if time.time()-client.last_pub_time >=options["interval"] and chatty:
        pubflag=True
    logging.debug("old "+str(client.sensor_status_old))
    logging.debug("new "+ str(client.sensor_status))    
    if client.sensor_status_old!=client.sensor_status or pubflag:
        client.publish(sensor_status_topic,client.sensor_status,0,True)
        print("publish on",sensor_status_topic,\
              " message  ",client.sensor_status)
        client.last_pub_time=time.time()
        client.sensor_status_old=client.sensor_status

def Initialise_client_object():
    mqtt.Client.last_pub_time=time.time()
    mqtt.Client.topic_ack=[]
    mqtt.Client.run_flag=True
    mqtt.Client.subscribe_flag=False
    mqtt.Client.sensor_status=states[1]
    mqtt.Client.sensor_status_old=None
    mqtt.Client.bad_connection_flag=False
    mqtt.Client.connected_flag=False
    mqtt.Client.disconnect_flag=False
    mqtt.Client.disconnect_time=0.0
    mqtt.Client.disconnect_flagset=False
    mqtt.Client.pub_msg_count=0
    
def Initialise_clients(cname):
    #flags set
    client= mqtt.Client(cname)
    if mqttclient_log: #enable mqqt client logging
        client.on_log=on_log
    client.on_connect= on_connect        #attach function to callback
    client.on_message=on_message        #attach function to callback
    client.on_disconnect=on_disconnect
    client.on_subscribe=on_subscribe
    client.on_publish=on_publish
    return client    

if __name__ == "__main__" and len(sys.argv)>=2:
    command_input(options)
chatty=options["verbose"]
logging.basicConfig(level=options["loglevel"]) #error logging
#use DEBUG,INFO,WARNING,ERROR
if not options["cname"]:
    r=random.randrange(1,10000)
    r=3542
    cname="sensor-"+str(r)
else:
    cname=str(options["cname"])
connected_topic=options["topic_base"]+"/connected/"+cname
sensor_status_topic=options["topic_base"]+"/"+cname
topic_control=sensor_status_topic+"/control"
options["topics"]=[(topic_control,0)]

if not options["verbose"]:
    print("only sending changes")

if options["sensor_type"]=="light":
    states=["ON","OFF"] #possible sensor states
else:
    states=["OPEN","CLOSED"] #possible sensor states    
Initialise_client_object() # add extra flags

logging.info("creating client"+cname)
client=Initialise_clients(cname)#create and initialise client object
if options["username"] !="":
    client.username_pw_set(options["username"],options["password"])
client.will_set(connected_topic,0, qos=0, retain=True) #set will

print("starting")
start_flag=True #used to always publish when starting
try:
    run_loop(client,options["broker"],options["port"],options["topics"],\
             options["keepalive"],publish_status)
    client.publish(connected_topic,0,retain=True)
    client.disconnect()
    
except KeyboardInterrupt:
    print("interrrupted by keyboard")