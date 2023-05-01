# TTM4115Group4

Access professor and teaching assistant interfaces:

Professor:
URL:  https://ervik-dev.appfarm.app/prof
Username: ttm.4115.stud+professor@gmail.com
Password: 12345678

Teaching Assistant:
URL:  https://ervik-dev.appfarm.app/ta
Username: ttm.4115.stud+ta1@gmail.com
Password: 12345678


Install mosquitto in linux environment and run an MQTT broker:
Step 1:
sudo apt update

Step 2:
sudo apt install -y mosquitto

Step 3:
git clone https://github.com/mariaopl/TTM4115Group4.git

Step 4:
Move to directory: mqtt-server

Step 5:
get local ip address

Step 6:
Change the bind_address to local ip address in the file mosquitto-conf

Step 7:
mosquitto -c mosquitto-conf &

Step 8:
Change ip addresses in mqtt-proxy.py and StateMachines.py



Set up mqtt proxy and student interface:

Run mqtt proxy by running the file mqtt-proxy.py

Run student interface by running the file StateMachine.py
