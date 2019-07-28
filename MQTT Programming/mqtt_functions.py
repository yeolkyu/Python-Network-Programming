###demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
## last updated 17-12-2017
###Free to use for any purpose
##contains common MQTT functions

import paho.mqtt.client as mqtt
import time
import logging
import sys,getopt



#Callbacks
def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_connect(client, userdata, flags, rc):
    logging.debug("Connected flags"+str(flags)+"result code "\
    +str(rc)+"client1_id")
    if rc==0:
        client.connected_flag=True
    else:
        client.bad_connection_flag=True

def on_disconnect(client, userdata, rc):
    logging.debug("disconnecting reason  " + str(rc))
    client.connected_flag=False
    client.disconnect_flag=True
    client.subscribe_flag=False
    
def on_subscribe(client,userdata,mid,granted_qos):
    m="in on subscribe callback result "+str(mid)
    logging.debug(m)
    for t in client.topic_ack:
        if t[1]==mid:
            t[2]=1 #acknowledged
            m="subscription acknowledged  "+str(t[0])
            logging.debug(m)
def on_publish(client, userdata, mid):
    logging.debug("pub ack "+ str(mid))
    client.puback_flag=True
##main loop



##########

def command_input(options={}):
    topics_in=[]
    qos_in=[]

    valid_options=" -b <broker> -p <port>-t <topic> -q QOS -v <verbose> -h <help>\
-c <loop Time secs -d logging debug  -n Client ID or Name\
-i loop Interval -u Username -P Password\
"
    print_options_flag=False
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hb:i:dk:p:t:q:l:vn:u:P:")
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
        elif opt =="-p":
            options["port"] = int(arg)
        elif opt =="-t":
            topics_in.append(arg)
        elif opt =="-q":
             qos_in.append(int(arg))
        elif opt =="-n":
             options["cname"]=arg
        elif opt =="-d":
            options["loglevel"]="DEBUG"
        elif opt == "-P":
             options["password"] = str(arg)
        elif opt == "-u":
             options["username"] = str(arg)        
        elif opt =="-v":
            options["verbose"]=True
      

    lqos=len(qos_in)
    for i in range(len(topics_in)):
        if lqos >i: 
            topics_in[i]=(topics_in[i],int(qos_in[i]))
        else:
            topics_in[i]=(topics_in[i],0)         
        
    if topics_in:
        options["topics"]=topics_in #array with qos

####
#######

def client_loop(client,broker,port=1883,topics="",keepalive=60,subscribe_flag=False,run_forever=False):
    #handles connects and reconnects and subscribes need to be called
    #inside a loop
    no_sub_flag=False
    if topics=="":
        no_sub_flag=True #don't try to subscribe
    client.loop(0.01) #manually call loop
    if not client.connected_flag:
        if Connect(client,broker,port,keepalive,run_forever=True) !=-1:
            if not wait_for(client,"CONNACK"):
               return False
        else:
            return False
    if client.bad_connection_flag:
        run_flag=False
        return False

         ###handle subscribing after failure
    if not no_sub_flag and not client.subscribe_flag and client.connected_flag:
        if subscribe_topics(client,topics)!=-1 and check_subs(client):
           client.subscribe_flag=True
        else:
            return False
    return True

#################


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

        client.loop(0.01)

        if client.connected_flag and loop_function and client.subscribe_flag: #function to call
                loop_function(client) #call function
        #time.sleep(interval)
    client.disconnect()
    client.connected_flag=False



##########


def subscribe_topics(client,topics,qos=0):
   print("topic ",topics,"  ",qos)
   
   if type(topics) is not list: #topics should be list of tuples
      if type(topics) is not tuple: #topics isn't tuple?
         topic_list=[(topics,qos)]
      else:
         topic_list=[topics]
   else:
      topic_list=topics
   try:
      r=client.subscribe(topic_list)
      if r[0]==0:
          logging.info("subscribed to topic"+str(topic_list)+" return code" +str(r))
          client.topic_ack.append([topic_list,r[1],0]) #keep track of subscription

      else:
          logging.info("error on subscribing "+str(r))
          print("error on subscribing "+str(r))
          return -1

   except Exception as e:
      logging.info("error on subscribe"+str(e))
      return -1
   return r
         
def check_subs(client):
    wcount=0
    while wcount<10:
        for t in client.topic_ack:
            wcount+=1
            if t[2]==0:
                logging.info("subscription to "+str(t[0]) +" not acknowledged")
                break
            print("All subs acknowledged")
            return True
        time.sleep(1)
        if not client.running_loop:
            client.loop(.01)  #check for messages manually

    return False



def Connect(client,broker,port,keepalive,run_forever=False):
    """Attempts connection set delay to >1 to keep trying
    but at longer intervals  """
    connflag=False
    delay=5
    #print("connecting ",client)
    badcount=0 # counter for bad connection attempts
    while not connflag:
        logging.info("connecting to broker "+str(broker))
        print("connecting to broker "+str(broker)+":"+str(port))
        print("Attempts ",badcount)
        time.sleep(delay)
        try:
            res=client.connect(broker,port,keepalive)      #connect to broker
            if res==0:
                connflag=True
                return 0
            else:
                logging.debug("connection failed ",res)
                badcount +=1
                if badcount>=3 and not run_forever: 
                    return -1
                    raise SystemExit #give up
                elif run_forever and badcount<3:
                    delay=5
                else:
                    delay=30

        except:
            client.badconnection_flag=True
            logging.debug("connection failed")
            badcount +=1
            if badcount>=3 and not run_forever: 
                return -1
                raise SystemExit #give up
            elif run_forever and badcount<3:
                delay=5*badcount
            elif delay<300:
                delay=30*badcount

                
    return 0
    #####end connecting

def wait_for(client,msgType,period=1,wait_time=10,running_loop=False):
    #running loop is true when using loop_start or loop_forever
    client.running_loop=running_loop #
    wcount=0  
    while True:
        logging.info("waiting"+ msgType)
        if msgType=="CONNACK":
            if client.on_connect:
                if client.connected_flag:
                    return True
                if client.bad_connection_flag: #
                    return False
                
        if msgType=="SUBACK":
            if client.on_subscribe:
                if client.suback_flag:
                    return True
        if msgType=="MESSAGE":
            if client.on_message:
                if client.message_received_flag:
                    return True
        if msgType=="PUBACK":
            if client.on_publish:        
                if client.puback_flag:
                    return True
     
        if not client.running_loop:
            client.loop(.01)  #check for messages manually
        time.sleep(period)
        #print("loop flag ",client.running_loop)
        wcount+=1
        if wcount>wait_time:
            print("return from wait loop taken too long")
            return False
    return True
