from multiprocessing import Process
from fabric import Connection
import os 
import shutil
from Simulation.Process.Commons import clientCommand,coordinatorPORT

class Client(Process):
    def __init__(self,projectDir,expNum,ip,connect_kwargs,hostIP,functionId):
        super(Client, self).__init__()
        self.projectDir = projectDir
        self.clientFileDir = os.path.join("src","Simulation","client")
        self.experimentNumber = expNum
        self.connection = Connection(ip,connect_kwargs=connect_kwargs)
        self.processId = ip[ip.find("linux-",2)+6:ip.find(".")]
        self.clientDir = os.path.join(self.projectDir, f"TempClient/TempClient_{self.processId}")

        self.hostIP = hostIP
        self.functionId = functionId
        self.environmentPath = "source ~/env/bin/activate"
        
    def run(self):

        print("Setup Client ...")  
        self.setup()

        print("Run Client...")
        self.task()
        
    def setup(self):
        def createStorage():
        
            print("Clean Previous Client File")
            if os.path.exists(f"TempClient/TempClient_{self.processId}"):
                shutil.rmtree(f"TempClient/TempClient_{self.processId}")
            
            os.mkdir(f"TempClient/TempClient_{self.processId}")
        
        
        def copyClientFile():
            
            shutil.copytree(src=self.clientFileDir,dst=f"TempClient/TempClient_{self.processId}/client")

       

        createStorage()
        copyClientFile()


    def task(self):
        with self.connection.cd(self.clientDir):
            with self.connection.prefix(self.environmentPath): 
            
                
                command = clientCommand.format(ip=self.hostIP,port=coordinatorPORT,functionId =self.functionId,experimentNum=self.experimentNumber,workerId=self.processId)
                print(command)
                result = self.connection.run(command, hide=True,pty=False)
                msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

                print(msg.format(result))

