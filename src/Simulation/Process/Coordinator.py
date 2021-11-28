from Simulation.Process.Commons import coordinatorStartCommand,coordinatorPORT
from multiprocessing import Process, process
from fabric import Connection
import shutil
import os

class Coordinator(Process):
    def __init__(self,projectDir,expNum,ip,connect_kwargs):
        super(Coordinator, self).__init__()

        self.projectDir=projectDir
        self.coordinatorDir = os.path.join(self.projectDir, "TempCoordinator")
        self.connection = Connection(ip,connect_kwargs=connect_kwargs)
        self.experimentNum = expNum
        self.processId = ip[ip.find("linux-",2)+6:ip.find(".")]

    def run(self,):
        self.setup()
        print("Run Coordinator ...")
        # for connection in self.c:

        #     self.task(connection)
        self.task()
    
    def setup(self,):
        print("Setup Coordinator...")

        def createStorage():
        
            print("Clean Previous Coordinator Files")
            if os.path.exists("TempCoordinator"):
                shutil.rmtree("TempCoordinator")
            
            os.mkdir("TempCoordinator")
        
        createStorage()



    def task(self,):
       
        command = "hostname -I"
        result = self.connection.run(command, hide=True)
        coordinator_IP = result.stdout.strip().split()[1]


        with self.connection.cd(self.coordinatorDir):
            command = coordinatorStartCommand.format(port=coordinatorPORT,experimentNum=1)
            print("Coordinator command: ",command)
            self.connection.run(command,hide=True,pty=False)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
            # print(msg.format(result))

