from multiprocessing import Process

class Developer(Process):
    def __init__(self,projectDir,c):
        super(Developer, self).__init__()

        self.projectDir = projectDir
        self.c = c

    
    def run(self):
        print("Setup Developer...")
        for connection in self.c:


            self.task(connection)

    def task(self,connection):
        with connection.cd(self.projectDir):
            command = "pwd"
            result = connection.run(command, hide=True,)
            msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
            print(msg.format(result))