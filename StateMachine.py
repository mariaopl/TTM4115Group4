from stmpy import Machine, Driver
from appJar import gui
import paho.mqtt.client as mqtt
from threading import Thread



class Help:

    def __init__(self, client: mqtt.Client):
        self.mqtt = client
        self.group = None
        self.task = None
        self.app = gui("Ask for help", "400x400")
        self.app.setBg("gainsboro")
        self.app.setFont(18)
        self.app.addLabel("group_label", "Enter your group number:")
        self.app.addEntry("group_entry")
        self.app.addButton("Submit", self.on_submit)

        def terminate():
            self.stm.terminate()
            return True

        self.queue = []
        self.app.setStopFunction(terminate)



    def on_submit(self):
        self.app.setBg("gainsboro")
        self.group = self.app.getEntry("group_entry")
        self.app.removeLabel("group_label")
        self.app.removeButton("Submit")
        self.app.addLabel("title", f"What task do you need help with? (Group {self.group})")
        for i in range(1, 11):
            self.app.addButton('Task ' + str(i), self.on_task_button)
        self.app.addButton("Other", self.on_task_button)
    
    def on_task_button(self, msg):
        self.stm.send('Task')
        print(msg)
        self.app.removeAllWidgets()
        self.app.addLabel("title", "You are now in queue for " + str(msg).lower())
        self.app.addButton("Help group", self.on_help_group)
        self.app.addButton("Abort help", self.on_abort_help)
        if (str(msg).lower() == "other"):
            self.task = 0
        else:
            self.task = str(msg).lower().replace("task ", "")
        self.mqtt_client.publish("ttm4115/" + str(self.group), str(self.task) + ",question")
      
        
    

    def on_help_group(self):
        self.app.setBg("gainsboro")
        self.stm.send('Need help')
        self.mqtt_client.publish("ttm4115/" + str(self.group), str(self.task) + ",getsHelp")
        self.app.removeAllWidgets()
        self.app.addButton("Group helped", self.on_group_helped)

    def on_group_helped(self):
        self.app.setBg("gainsboro")
        self.stm.send('Gets help')
        self.mqtt_client.publish("ttm4115/" + str(self.group), str(self.task) + ",groupHelped")
        self.app.removeAllWidgets()
        self.app.addLabel("title", f"What task do you need help with? (Group {self.group})")
        for i in range(1, 11):
            self.app.addButton('Task ' + str(i), self.on_task_button)
        self.app.addButton("Other", self.on_task_button)
    
    def on_abort_help(self):
        self.app.setBg("gainsboro")
        self.stm.send('Abort help')
        self.mqtt_client.publish("ttm4115/" + str(self.group), str(self.task) +  ",abort")
        self.app.removeAllWidgets()
        self.app.addLabel("title", f"What task do you need help with? (Group {self.group})")
        for i in range(1, 11):
            self.app.addButton('Task ' + str(i), self.on_task_button)
        self.app.addButton("Other", self.on_task_button)


    def enter_queue(self):
        if (self.group not in self.queue):
            self.queue.append(self.group)
    
    def exit_queue(self):
        if (self.group in self.queue):
            self.queue.remove(self.group)


class MQTT_Client:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(host)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
    
    def on_message(self, client, userdata, msg):
        print("on_message(): topic: {}".format(msg.topic))


    def start(self, broker, port):
        print("Connecting to {}:{}".format(broker, port))
        self.client.connect(broker, port)
        self.client.subscribe("ttm4115")

        try:
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()

    


host = "172.31.214.230"

help = Help(host)


initial = {'source': 'initial',
        'target': 'no_help'}

    
t1 = {'trigger': 'Task',
        'source': 'no_help',
        'target': 'need_help'}

t2 = {'trigger': 'Need help',
        'source': 'need_help',
        'target': 'gets_help'}

t3 = {'trigger': 'Gets help',
        'source': 'gets_help',
        'target': 'no_help'}

t4 = {'trigger': 'Abort help',
        'source': 'need_help',
        'target': 'no_help',
        'effect': 'exit_queue'}

no_help = {'name': 'no_help'}
need_help = {'name': 'need_help', 'entry': 'enter_queue'}
gets_help = {'name': 'gets_help', 'entry': 'exit_queue'}

states = [no_help, need_help, gets_help]
transitions = [initial, t1, t2, t3, t4]

stm_help = Machine(name='help', transitions=transitions, obj=help, states=states)
help.stm = stm_help

driver = Driver()
driver.add_machine(stm_help)
driver.start()

help_client = MQTT_Client()
help.mqtt_client = help_client.client
help_client.stm_driver = driver
help_client.start(host, 1883)

help.app.go()
