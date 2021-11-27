from multiprocessing import Process
from fabric import Connection
class Client(Process):
    def __init__(self,projectDir,ip,connect_kwargs):
        super(Client, self).__init__()
        self.projectDir = projectDir
        self.connection = Connection(ip,connect_kwargs=connect_kwargs) 
        pass
    def run(self):
        print("Setup Clients ...")  
        self.task()
        

    def task(self):

        with self.connection.cd(self.projectDir):
            command = "pwd"
            self.connection.run(command, hide=True,pty=False)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

        # print(msg.format(result))

