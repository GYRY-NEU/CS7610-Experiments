from Simulation.Process.Commons import coordinatorStartCommand,coordinatorPORT
from multiprocessing import Process
from fabric import Connection
class Coordinator(Process):
    def __init__(self,projectDir,ip,connect_kwargs,experimentNum):
        super(Coordinator, self).__init__()

        self.projectDir=projectDir
        self.connection = Connection(ip,connect_kwargs=connect_kwargs)
        self.experimentNum = experimentNum

    def run(self,):
        print("Setup Coordinator...")
        # for connection in self.c:

        #     self.task(connection)
        self.task()
        
    def task(self,):
       
        command = "hostname -I"
        result = self.connection.run(command, hide=True)
        coordinator_IP = result.stdout.strip().split()[1]


        with self.connection.cd(self.projectDir):
            command = coordinatorStartCommand.format(port=coordinatorPORT,experimentNum=1)
            print("Coordinator command: ",command)
            self.connection.run(command,hide=True,pty=False)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
            # print(msg.format(result))

