import os
from fabric import SerialGroup as Group
from fabric.exceptions import  GroupException
from os import getenv
import shutil

import time

from Simulation.Process.Worker import Worker
from Simulation.Process.Client import Client
from Simulation.Process.Developer import Developer
from Simulation.Process.Coordinator import Coordinator
import sys
from Simulation.Process.AddressTable import ipTable


connect_kwargs = {
    'password': getenv('MYKHOURYPASS')
}


# print(ipTable)

expNum = int(sys.argv[6])
projectDir ="Simulation"
tempDeveloperBase = os.path.join(projectDir,"TempDeveloper")
tempClientBase = os.path.join(projectDir,"TempClient")
tempWorkerBase = os.path.join(projectDir,"TempWorker")
tempCoordinatorBase = os.path.join(projectDir,"TempCoordinator")
outputDir = os.path.join("Outputs",f'experiment_{expNum}')
print('-'*100)
print(f"Experiment {expNum} Starts...")




def task_clean(c):
    username =  getenv('USER')
    command = f"pkill -u {username}"
    result = c.run(command, hide=True)
    msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    print(msg.format(result))

def folder_clean(tempDeveloperBase,tempClientBase,tempWorkerBase,tempCoordinatorBase,outputDir):
    def clean_single(path):
        path = os.path.basename(path)
        if os.path.exists(path):
            # print(f'exists {path}')
            shutil.rmtree(path)
            
        os.mkdir(path)
    def clean_output(dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)
        os.mkdir(os.path.join(dir,'client'))
        os.mkdir(os.path.join(dir,'worker'))
        os.mkdir(os.path.join(dir,'coordinator'))

        
    
    clean_single(tempDeveloperBase)
    clean_single(tempClientBase)
    clean_single(tempWorkerBase)
    clean_single(tempCoordinatorBase)
    clean_output(outputDir)





def createDeveloperFile(developerId,developerFolder):
    tempFolder = os.path.join(tempDeveloperBase,f"temp_{developerId}")

    if os.path.exists(tempFolder):
        shutil.rmtree(tempFolder)
    



try:
    vdiUrl ="vdi-linux-0{id}.ccs.neu.edu"

    threads = []
    currentID=42
    coordinatorIp = vdiUrl.format(id=41)
    workerCount = int(sys.argv[1])
    developerCount=int(sys.argv[2])
    clientCount=int(sys.argv[3])
    requestPerClient = int(sys.argv[4])
    threadCount = int(sys.argv[5])
    total = 1 + workerCount + developerCount + clientCount + requestPerClient

    print("Clean up ssh before start...")
    try:
        
        host = [vdiUrl.format(id=i) for i in range(41,41+total)]
        group_all= Group(*host,connect_kwargs=connect_kwargs)

        task_clean(group_all)
    except GroupException:
        print('Cleaned ssh Successfully')
        print("Clean up ssh before start...")
    

    print('clean folders')
    folder_clean(tempDeveloperBase,tempClientBase,tempWorkerBase,tempCoordinatorBase,outputDir)
    time.sleep(10)


    #Setup Coordinator

    coordinator = Coordinator(projectDir,expNum,coordinatorIp,connect_kwargs)
    coordinator.start()
    time.sleep(2)





    # Start Workers
    #______________________________________________________________________________________________________________________________
    workers = []
    for workerNum in range(workerCount):
        workerIp = vdiUrl.format(id=currentID)
        currentID +=1
        workers.append(Worker(projectDir,expNum,workerIp,connect_kwargs,ipTable[coordinatorIp]))

    for worker in workers:
        worker.start()
        time.sleep(1)


    # Setup Developers
    #______________________________________________________________________________________________________________________________
    developers = []
    developerFuncID={}
    for developerNum in range(developerCount):
        developerIp = vdiUrl.format(id=currentID)
        currentID +=1
        developers.append(Developer(projectDir,expNum,developerIp,connect_kwargs,developerNum,ipTable[coordinatorIp]))

    for developerID,developer in enumerate(developers):
        funcID =developer.setup()
        developerFuncID[developerID]= funcID
        time.sleep(1)

    for developer in developers:
        developer.start()
        time.sleep(1)
    
    # Developer Join
    #______________________________________________________________________________________________________________________________
    for developer in developers:
        developer.join()
    # Star Clients
    #______________________________________________________________________________________________________________________________
    clients = []
    for clientNum in range(clientCount):
        clientIp = vdiUrl.format(id=currentID)
        currentID +=1
        clients.append(Client(projectDir,expNum,clientIp,connect_kwargs,ipTable[coordinatorIp],developerFuncID[clientNum % developerCount],requestPerClient,threadCount))

    for client in clients:
        client.start()


    # Client Join
    #______________________________________________________________________________________________________________________________
    for client in clients:
        client.join()
    
    print("Clean up...")
    try:
        host = [vdiUrl.format(id=i) for i in range(41,currentID)]
        group_all= Group(*host,connect_kwargs=connect_kwargs)

        task_clean(group_all)
    except GroupException:
        print('Cleaned Successfully')


except KeyboardInterrupt:
        print('Interrupted')
        print("Clean up...")
        # developer.terminate()
        # client.terminate()
        try:
            task_clean(group_all)
        except GroupException:
            print('Cleaned Successfully')
            
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)










