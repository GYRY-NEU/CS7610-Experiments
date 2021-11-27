from Simulation.Process.Commons import workerStartCommand,coordinatorPORT
from multiprocessing import Process
from fabric import Connection
class Worker(Process):
    def __init__(self,projectDir,workerIp,connect_kwargs, hostIp,experimentNum,workerId):
        super(Worker, self).__init__()

        
        self.projectDir = projectDir
        self.connection = Connection(workerIp,connect_kwargs=connect_kwargs)
        self.ip = hostIp
        self.experimentNum = experimentNum
        self.workerId = workerId

    def run(self):
        print("Setup Workers...")
        self.task()
        

    def task(self,):
    # command = "hostname -i"
    # result = c.run(command, hide=True)
    # worker_IP = result.stdout
    # workerId =worker_IP.split(".")[-1].strip()
        print("ip", self.ip)
        with self.connection.cd(self.projectDir):
            command = workerStartCommand.format(ip=self.ip,port=coordinatorPORT,experimentNum=self.experimentNum,workerId=self.workerId)
            print("workerCommand: ",command)
            self.connection.run(command,hide=True,pty=False)
            # msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"

            # print(msg.format(result))

