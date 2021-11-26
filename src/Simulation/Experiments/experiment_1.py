#!/home/gokberkyar/secfedlearn/runParallel/venv/bin/python
import os
import fabric
from fabric import Connection
from fabric import SerialGroup as Group
from os import getenv
import time

from Simulation.Worker import Worker
from Simulation.Client import Client
from Simulation.Developer import Developer
from Simulation.Coordinator import Coordinator
from multiprocessing import Process
import sys
from Simulation.AddressTable import ipTable

print("Experiment 1 Starts...")

connect_kwargs = {
    'password': getenv('MYKHOURYPASS')
}


# print(ipTable)
group_all          = Group("vdi-linux-047.ccs.neu.edu","vdi-linux-046.ccs.neu.edu","vdi-linux-045.ccs.neu.edu","vdi-linux-043.ccs.neu.edu",connect_kwargs=connect_kwargs)
group_developer    = Group("vdi-linux-047.ccs.neu.edu",connect_kwargs=connect_kwargs)
group_worker       = Group("vdi-linux-046.ccs.neu.edu",connect_kwargs=connect_kwargs)
group_client       = Group("vdi-linux-045.ccs.neu.edu",connect_kwargs=connect_kwargs)
group_coordinator  = Group("vdi-linux-043.ccs.neu.edu",connect_kwargs=connect_kwargs)

projectDir ="CS7610_Experimentation"




def task_clean(c):
    username =  getenv('USER')
    command = f"pkill -u {username}"
    result = c.run(command, hide=True)
    msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    print(msg.format(result))



try:

    coordinator = Coordinator(projectDir,group_coordinator,1)
    developer = Developer(projectDir,group_developer)
    worker  = Worker(projectDir,group_worker,ipTable["vdi-linux-043.ccs.neu.edu"],1,46)
    client  = Client(projectDir,group_client)
    coordinator.start()
    time.sleep(2)
    worker.start()
    developer.start()
    time.sleep(2)
    client.start()
    time.sleep(2)

    print("Ctrl/Cmd + C to terminate ...")
    coordinator.join()
    developer.join()
    worker.join()
    client.join()
    print("Clean up...")
    task_clean(group_all)

except KeyboardInterrupt:
        print('Interrupted')
        print("Clean up...")
        worker.terminate()
        developer.terminate()
        coordinator.terminate()
        client.terminate()
        
        task_clean(group_all)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)








