from multiprocessing import Process
class Client(Process):
    def __init__(self,projectDir,c):
        super(Client, self).__init__()
        self.projectDir = projectDir
        self.c = c 
        pass
    def run(self):
        print("Setup Clients ...")  
        for connection in self.c:

            self.task(connection)
        

    def task(self,connection):

        with connection.cd(self.projectDir):
            command = "pwd"
            connection.run(command, hide=True,pty=False)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

        # print(msg.format(result))

