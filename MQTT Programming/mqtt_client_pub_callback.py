import paho.mqtt.client as paho
broker="iot.eclipse.org"
port=1883
def on_publish(client,userdata,result): #create function for callback
	print("data published \n")
	pass

client1= paho.Client() #create client object
client1.on_publish = on_publish #assign function to callback
client1.connect(broker, port)
ret= client1.publish("mqtt/test","Hello") #publish