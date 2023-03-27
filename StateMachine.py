from stmpy import Machine, Driver
from appJar import gui

class Help:

    def __init__(self):
        self.app = gui("Ask for help", "400x400")
        self.app.setFont(18)
        self.app.addLabel("title", "What task do you need help with")
        def press_button_task(button):
            for i in range(1, 10):
                self.stm.send('Need help with task ' + str(i))

        def press_button_other(button):
            self.stm.send('other')
        for i in range(1, 10):
            self.app.addButton('Need help with task ' + str(i), press_button_task)
        self.app.addButton("other", press_button_other)
        
        def terminate():
            self.stm.terminate()
            return True
        self.app.setStopFunction(terminate)

        
    def on_button_pressed(self):
        print("Button pressed")
    
    def on_help_group(self):
        print("Helping group")
    
    def on_group_helped(self):
        print("Group helped")
    


help = Help()

t0 = {'source': 'initial',
        'target': 'no_help'}

t1 = {'trigger': 'button_pressed',
        'source': 'no_help',
        'target': 'need_help'}

t2 = {'trigger': 'help_group',
        'source': 'need_help',
        'target': 'gets_help'}

t3 = {'trigger': 'group_helped',
        'source': 'gets_help',
        'target': 'no_help'}

no_help = {'name': 'no_help', 'entry': 'on_group_helped; on_init'}
need_help = {'name': 'need_help', 'entry': 'on_button_pressed'}
gets_help = {'name': 'gets_help', 'entry': 'on_help_group'}

states = [no_help, need_help, gets_help]
transitions = [t0, t1, t2, t3]

stm_help = Machine(name='help', transitions=transitions, obj=help, states=states)
help.stm = stm_help

driver = Driver()
driver.add_machine(stm_help)
driver.start()

help.app.go()
