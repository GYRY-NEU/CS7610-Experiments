from multiprocessing import Process, process
from Simulation.Process.Commons import developerUploadCommand,coordinatorPORT,developerInitCommand,developerCheckRoundCommand,developerCheckModelCommand
import time
from fabric import Connection

# rm -f pythonfunc.zip;
# 7z a -tzip pythonfunc.zip *;
# HOST=$(curl --data-binary @pythonfunc.zip $master:$master_port/function | awk '{ print $3 }');
# curl --resolve $HOST:$master_port:$master http://$HOST:$master_port/init
import os 
import shutil

class Developer(Process):
    def __init__(self,projectDir,expNum,ip,connect_kwargs,developerType,hostIP):
        super(Developer, self).__init__()

        self.projectDir = projectDir
        self.ip = ip 
        self.connect_kwargs = connect_kwargs
        self.connection = Connection(ip,connect_kwargs=connect_kwargs)
        self.experimentNumber = expNum
        self.developerType =developerType
        self.processId = ip[ip.find("linux-",2)+6:ip.find(".")]
        self.developerFileDir = os.path.join("src","Simulation",f"developer_{self.developerType}")
        self.developerDir = os.path.join(projectDir,"TempDeveloper",f"TempDeveloper_{self.processId}")
        self.hostIP = hostIP
        


    def run(self,):

        


        print("Run Developer")
        self.task()
        time.sleep(2)

        print('Run Check')
        self.check()

    def reconnect(self):
        self.connection = Connection(self.ip,connect_kwargs=self.connect_kwargs)

    def setup(self):
        print("Setup Developer...")
        def createStorage():
        
            print("Clean Previous Developer File")
            if os.path.exists(f"TempDeveloper/TempDeveloper_{self.processId}"):
                shutil.rmtree(f"TempDeveloper/TempDeveloper_{self.processId}")
            
            os.mkdir(f"TempDeveloper/TempDeveloper_{self.processId}")
        
        
        def copyClientFile():
            
            shutil.copytree(src=self.developerFileDir,dst=f"TempDeveloper/TempDeveloper_{self.processId}/pyFiles")

        def zipClientFolder():
            shutil.make_archive(f"TempDeveloper/TempDeveloper_{self.processId}/pythonfunc", 'zip', f"TempDeveloper/TempDeveloper_{self.processId}/pyFiles")


        createStorage()
        copyClientFile()
        zipClientFolder()


        print(self.developerDir)
        self.reconnect()
        with self.connection.cd(self.developerDir):
            print('Entered')
            command = developerUploadCommand.format(ip=self.hostIP,port=coordinatorPORT,experimentNum=self.experimentNumber,workerId = self.processId)
            # command = 'pwd'
            # print(command)
            result = self.connection.run(command, hide=True)
            msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
            print(msg.format(result))
            self.functionId = result.stdout[result.stdout.find("=> ")+3:].strip()
            
            print(self.functionId)

            return self.functionId

    def task(self,):
            self.reconnect()
            with self.connection.cd(self.developerDir):
                command = developerInitCommand.format(ip=self.hostIP,port=coordinatorPORT,functionId = self.functionId,experimentNum=self.experimentNumber,workerId = self.processId)
                # command = 'pwd'

                print(command)
                result = self.connection.run(command, hide=True)
                msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
                print(msg.format(result))
                # self.functionId = result.stdout[result.stdout.find("=> ")+3:].strip()
                
                # print(self.functionId)

    def check(self,):
        def checkRound():

            self.reconnect()

            with self.connection.cd(self.developerDir):
                command = developerCheckRoundCommand.format(ip=self.hostIP,port=coordinatorPORT,functionId = self.functionId,experimentNum=self.experimentNumber,workerId = self.processId)
                # command = 'pwd'
                # print(command)
                result = self.connection.run(command, hide=True)
                msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
                print(msg.format(result))
                # self.functionId = result.stdout[result.stdout.find("=> ")+3:].strip()
        def checkModel():
            self.reconnect()

            with self.connection.cd(self.developerDir):
                command = developerCheckModelCommand.format(ip=self.hostIP,port=coordinatorPORT,functionId = self.functionId,experimentNum=self.experimentNumber,workerId = self.processId)
                print(command)
                result = self.connection.run(command,hide=True )
                msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
                print(msg.format(result))
                # self.functionId = result.stdout[result.stdout.find("=> ")+3:].strip()
                # print(self.functionId)
        checkRound()
        checkModel()
