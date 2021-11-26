from Commons import coordinatorStartCommand,coordinatorPORT
from multiprocessing import Process

class Coordinator(Process):
    def __init__(self,projectDir,c,experimentNum):
        super(Coordinator, self).__init__()

        self.projectDir=projectDir
        self.c = c
        self.experimentNum = experimentNum

    def run(self,):
        print("Setup Coordinator...")
        for connection in self.c:

            self.task(connection)
        
    def task(self,connection):
       
        command = "hostname -I"
        result = connection.run(command, hide=True)
        coordinator_IP = result.stdout.strip().split()[1]


        with connection.cd(self.projectDir):
            command = coordinatorStartCommand.format(port=coordinatorPORT,experimentNum=1)
            print("Coordinator command: ",command)
            connection.run(command,hide=True,pty=False)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
            # print(msg.format(result))

