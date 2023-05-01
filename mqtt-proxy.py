import paho.mqtt.client as mqtt
import requests

TOKEN = "643d0b49827f2746222ce912.ecda82a87eab4748ce96a7b0b35f71c2fac21506b711223d"
mqttBroker = "10.24.27.124"
port = 1883

 

def sendHTTP(groupNr,question,action):
    req = requests.post('https://ervik-dev.appfarm.app/api/services/service/'+action, 
                    headers={
                        "accept": "*/*",
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer " + TOKEN
                    }, 
                    json={
                        "groupnr": groupNr,
                        "question": question
                    })
    print("res: "+req.text)

 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

 

    client.subscribe("ttm4115/#")

 

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    error = False
    groupNr = -1
    question = -1
    action = ""
    #print(msg.payload.decode())
    
    try:
        groupNr = int(msg.topic.split("/")[1])
        question = int(msg.payload.decode().split(",")[0])
        action = msg.payload.decode().split(",")[1]
        print("gr: "+str(groupNr)+" q: "+str(question)+" action: " + action)
    except:
        error = True
        
    print("gr: '"+str(groupNr)+"' q: '"+str(question)+"' action: '" +
          action + "' error: '" + str(error) + "'")
    
    if(error == False) and (question >= 0) and (groupNr > 0) and (action != ""):
        print("gr: "+str(groupNr)+" q: "+str(question)+" action: " + action)
        sendHTTP(groupNr,question,action)
    else:
        print("Bad MQTT message!")
        print(msg.payload.decode())

 

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

 

client.connect(mqttBroker, port, 60)

 

client.loop_forever()
