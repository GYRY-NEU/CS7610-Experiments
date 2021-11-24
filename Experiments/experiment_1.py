#!/home/gokberkyar/secfedlearn/runParallel/venv/bin/python
import os
import fabric
from fabric import Connection
from fabric import SerialGroup as Group
from os import getenv
import time
from commons import coordinatorStartCommand,coordinatorPORT,workerStartCommand

print("Experiment 1 Starts...")



connect_kwargs = {
    'password': getenv('MYKHOURYPASS')
}

group_developer    = Group("vdi-linux-047.ccs.neu.edu",connect_kwargs=connect_kwargs)
group_worker       = Group("vdi-linux-046.ccs.neu.edu",connect_kwargs=connect_kwargs)
group_client       = Group("vdi-linux-045.ccs.neu.edu",connect_kwargs=connect_kwargs)
group_coordinator  = Group("vdi-linux-044.ccs.neu.edu",connect_kwargs=connect_kwargs)

projectDir ="CS7610-Experimentation"

def task_developer(c):
    with c.cd(projectDir):
        command = "pwd"
        result = c.run(command, hide=True)
        msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
        print(msg.format(result))
    pass

def task_worker(c,ip):
    # command = "hostname -i"
    # result = c.run(command, hide=True)
    # worker_IP = result.stdout
    # workerId =worker_IP.split(".")[-1].strip()
    print("ip", ip)
    with c.cd(projectDir):
        command = workerStartCommand.format(ip=ip,port=coordinatorPORT,experimentNum=1,workerId=47)
        print("workerCommand: ",command)
        result = c.run(command,hide=True)
        msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

        print(msg.format(result))

    pass

def task_client(c):
    with c.cd(projectDir):
        command = "pwd"
        result = c.run(command, hide=True)
        msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

    print(msg.format(result))

    pass

def task_coordinator(c):
    command = "hostname -I"
    result = c.run(command, hide=True)
    coordinator_IP = result.stdout.strip().split()[1]


    with c.cd(projectDir):
        command = coordinatorStartCommand.format(port=coordinatorPORT,experimentNum=1)
        print("Coordinator command: ",command)
        result = c.run(command,hide=True)
        msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
        print(msg.format(result))

    return coordinator_IP
    # def createTemporaryFolder():
    #     return "a"

    # workDir = createTemporaryFolder()




        

# workDir ="secfedlearn/runParallel"
# environmentPath = "source venv/bin/activate"
# command = "celery --app tasks worker --detach --loglevel INFO -O fair --prefetch-multiplier 1 --concurrency 3 --logfile celery_`hostname`.txt"
# #command = "hostname"
# def task(c):
#     with c.cd(workDir):
#         with c.prefix(environmentPath):         
#            result= c.run(command)
#            print(result)
            

print("Setup Coordinator...")
for connection in group_coordinator:
    coordinatorIp =task_coordinator(connection)
time.sleep(2)

print("Setup Workers...")
for connection in group_worker:
    task_worker(connection,coordinatorIp)
time.sleep(2)

print("Setup Developer...")
for connection in group_developer:
    task_developer(connection)
time.sleep(2)


print("Clients Developer...")
for connection in group_client:
    task_client(connection)
time.sleep(2)
