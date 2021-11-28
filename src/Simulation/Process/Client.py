from multiprocessing import Process, process
from fabric import Connection
import os 
import shutil

class Client(Process):
    def __init__(self,projectDir,expNum,ip,connect_kwargs):
        super(Client, self).__init__()
        self.projectDir = projectDir
        self.clientDir = os.path.join(self.projectDir, "TempClient")
        self.clientFileDir = os.path.join("src","Simulation","client")
        self.experimentNumber = expNum
        self.connection = Connection(ip,connect_kwargs=connect_kwargs)
        self.processId = ip[ip.find("linux-",2)+6:ip.find(".")]

        pass
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
            
            shutil.copytree(src=self.clientFileDir,dst=f"TempClient/TempClient_{self.processId}/pyFiles")

        def zipClientFolder():
            shutil.make_archive(f"TempClient/TempClient_{self.processId}/pythonfunc", 'zip', f"TempClient/TempClient_{self.processId}/pyFiles")


        createStorage()
        copyClientFile()
        zipClientFolder()


    def task(self):

        with self.connection.cd(self.projectDir):
            command = "pwd"
            self.connection.run(command, hide=True,pty=False)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

        # print(msg.format(result))

