from Commons import workerStartCommand,coordinatorPORT
from multiprocessing import Process

class Worker(Process):
    def __init__(self,projectDir,c,ip,experimentNum,workerId,):
        super(Worker, self).__init__()

        
        self.projectDir = projectDir
        self.c = c
        self.ip = ip
        self.experimentNum = experimentNum
        self.workerId = workerId

    def run(self):
        print("Setup Workers...")
        for connection in self.c:
            self.task(connection)

        pass
    def task(self,connection):
    # command = "hostname -i"
    # result = c.run(command, hide=True)
    # worker_IP = result.stdout
    # workerId =worker_IP.split(".")[-1].strip()
        print("ip", self.ip)
        with connection.cd(self.projectDir):
            command = workerStartCommand.format(ip=self.ip,port=coordinatorPORT,experimentNum=self.experimentNum,workerId=self.workerId)
            print("workerCommand: ",command)
            connection.run(command,hide=True)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

            # print(msg.format(result))

