from Simulation.Process.Commons import workerStartCommand,coordinatorPORT
from multiprocessing import Process
from fabric import Connection
import os
import shutil

class Worker(Process):
    def __init__(self,projectDir,expNum,workerIp,connect_kwargs, hostIp):
        super(Worker, self).__init__()

        
        self.projectDir = projectDir
        self.connection = Connection(workerIp,connect_kwargs=connect_kwargs)
        self.ip = hostIp
        self.experimentNum = expNum
        self.processId = workerIp[workerIp.find("linux-",2)+6:workerIp.find(".")]
        self.workerPath= os.path.join(self.projectDir,"TempWorker",f"Worker_{self.processId}")


    def run(self):
        print("Setup Workers...")
        self.setup()

        print("Run Worker")
        self.task()
        

    def setup(self,):
        def createStorage():
        
            print("Clean Previous Worker Files")
            if os.path.exists(f"TempWorker/Worker_{self.processId}"):
                shutil.rmtree(f"TempWorker/Worker_{self.processId}")
            
            # os.mkdir("TempWorker")
            os.mkdir(f"TempWorker/Worker_{self.processId}")
        
        createStorage()

    def task(self,):
    # command = "hostname -i"
    # result = c.run(command, hide=True)
    # worker_IP = result.stdout
    # workerId =worker_IP.split(".")[-1].strip()
        print("ip", self.ip)
        with self.connection.cd(self.workerPath):
            command = workerStartCommand.format(ip=self.ip,port=coordinatorPORT,experimentNum=self.experimentNum,workerId=int(self.processId))
            print("workerCommand: ",command)
            self.connection.run(command,hide=True,pty=False)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

            # print(msg.format(result))

