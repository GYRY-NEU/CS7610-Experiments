import os
from fabric import SerialGroup as Group
from os import getenv
import shutil

import time

from Simulation.Process.Worker import Worker
from Simulation.Process.Client import Client
from Simulation.Process.Developer import Developer
from Simulation.Process.Coordinator import Coordinator
import sys
from Simulation.Process.AddressTable import ipTable

print("Experiment 1 Starts...")

connect_kwargs = {
    'password': getenv('MYKHOURYPASS')
}


# print(ipTable)
group_all          = Group("vdi-linux-047.ccs.neu.edu","vdi-linux-046.ccs.neu.edu","vdi-linux-045.ccs.neu.edu","vdi-linux-043.ccs.neu.edu",connect_kwargs=connect_kwargs)

expNum = 1
projectDir ="Simulation"
tempDeveloperBase = os.path.join(projectDir,"TempDeveloper")
tempClientBase = os.path.join(projectDir,"TempClient")
tempWorkerBase = os.path.join(projectDir,"TempWorker")
tempCoordinatorBase = os.path.join(projectDir,"TempCoordinator")




def task_clean(c):
    username =  getenv('USER')
    command = f"pkill -u {username}"
    result = c.run(command, hide=True)
    msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    print(msg.format(result))

def createDeveloperFile(developerId,developerFolder):
    tempFolder = os.path.join(tempDeveloperBase,f"temp_{developerId}")

    if os.path.exists(tempFolder):
        shutil.rmtree(tempFolder)
    



try:

    coordinator = Coordinator(projectDir,expNum,"vdi-linux-043.ccs.neu.edu",connect_kwargs)
    developer = Developer(projectDir,expNum,"vdi-linux-046.ccs.neu.edu",connect_kwargs,[1])
    worker  = Worker(projectDir,expNum,"vdi-linux-045.ccs.neu.edu",connect_kwargs,ipTable["vdi-linux-043.ccs.neu.edu"])
    worker2  = Worker(projectDir,expNum,"vdi-linux-042.ccs.neu.edu",connect_kwargs,ipTable["vdi-linux-043.ccs.neu.edu"])
    client  = Client(projectDir,expNum,"vdi-linux-047.ccs.neu.edu",connect_kwargs)
    coordinator.start()
    time.sleep(2)
    worker.start()
    time.sleep(2)
    worker2.start()
    developer.start()
    time.sleep(2)
    client.start()
    time.sleep(2)

    print("Ctrl/Cmd + C to terminate ...")
    coordinator.join()
    developer.join()
    worker.join()
    client.join()
    worker2.join()
    print("Clean up...")
    task_clean(group_all)

except KeyboardInterrupt:
        print('Interrupted')
        print("Clean up...")
        worker.terminate()
        worker2.terminate()
        developer.terminate()
        coordinator.terminate()
        client.terminate()
        
        task_clean(group_all)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)








