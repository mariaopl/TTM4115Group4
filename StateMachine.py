from stmpy import Machine, Driver
from appJar import gui
import paho.mqtt.client as mqtt
from threading import Thread



class Help:

    def __init__(self, client: mqtt.Client):
        self.mqtt = client
        self.group = None
        self.tasks = [0,1,2,3,4,5,6,7,8,9,10]
        self.app = gui("Ask for help", "400x400")
        self.app.setFont(18)
        self.app.addLabel("group_label", "Enter your group number:")
        self.app.addEntry("group_entry")
        self.app.addButton("Submit", self.on_group_submit)

        def terminate():
            self.stm.terminate()
            return True

        self.queue = []
        self.group = None
        self.app.setStopFunction(terminate)



    def on_group_submit(self):
        self.group = self.app.getEntry("group_entry")
        self.app.removeLabel("group_label")
        self.app.removeEntry("group_entry")
        self.app.removeButton("Submit")

        self.app.addLabel("title", f"What task do you need help with? (Group {self.group})")

        for i in range(1, 11):
            self.app.addButton('Task ' + str(i), self.press_button)
        self.app.addButton("Task", self.press_button)
    
    def press_button(self, msg):
        self.stm.send('Task')
        print(msg)
        self.app.removeAllWidgets()
        self.app.addLabel("title", "You are now in queue for " + str(msg).lower())
        self.app.addButton("Group helped", self.on_help_group)
        self.stm.send('Need help')

    def on_help_group(self):
        print("Helping group " + self.group)
        self.stm.send('Gets help')
        for i in range(1, 11):
            self.app.addButton('Task ' + str(i), self.press_button)
        self.app.hideButton("Group helped")
    
    def on_group_helped(self):
        print("Group helped")

    def enter_queue(self):
        print("Entered queue")
        self.queue.append(self.group)
    
    def exit_queue(self):
        print("Exited queue")
        self.queue.remove(self.group)


class MQTT_Client:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(host)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
    
    def on_message(self, client, userdata, msg):
        print("on_message(): topic: {}".format(msg.topic))
        try:
            self.client.publish("group4", msg.payload)
        except e:
            print(e)

    
    def start(self, broker, port):

        print("Connecting to {}:{}".format(broker, port))
        self.client.connect(broker, port)

        self.client.subscribe("ttm4115")

        try:
            # line below should not have the () after the function!
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()

    


host = "mqtt20.iik.ntnu.no"

help = Help(host)


initial = {'source': 'initial',
        'target': 'no_help'}

    
no_help_transition = {'trigger': 'Task',
        'source': 'no_help',
        'target': 'need_help'}

need_help_transition = {'trigger': 'Need help',
        'source': 'need_help',
        'target': 'gets_help'}

gets_help_transition = {'trigger': 'Gets help',
        'source': 'gets_help',
        'target': 'no_help'}

no_help = {'name': 'no_help'}
need_help = {'name': 'need_help', 'entry': 'enter_queue'}
gets_help = {'name': 'gets_help', 'entry': 'exit_queue'}

states = [no_help, need_help, gets_help]
transitions = [initial, no_help_transition, need_help_transition, gets_help_transition]

stm_help = Machine(name='help', transitions=transitions, obj=help, states=states)
help.stm = stm_help

driver = Driver()
driver.add_machine(stm_help)
driver.start()

client = MQTT_Client()
help.mqtt = client
client.stm_driver = driver
client.start(host, 1883)

help.app.go()
