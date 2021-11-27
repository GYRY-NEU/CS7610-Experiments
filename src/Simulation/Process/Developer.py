from multiprocessing import Process
from fabric import Connection

# rm -f pythonfunc.zip;
# 7z a -tzip pythonfunc.zip *;
# HOST=$(curl --data-binary @pythonfunc.zip $master:$master_port/function | awk '{ print $3 }');
# curl --resolve $HOST:$master_port:$master http://$HOST:$master_port/init


class Developer(Process):
    def __init__(self,projectDir,ip,connect_kwargs,developerList):
        super(Developer, self).__init__()

        self.projectDir = projectDir
        self.connection = Connection(ip,connect_kwargs=connect_kwargs)

        self.developerList =developerList

    
    def run(self,):
        print("Setup Developer...")
        self.task()

    def task(self,):
        with self.connection.cd(self.projectDir):
            command = "pwd"
            result = self.connection.run(command, hide=True,)
            msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
            print(msg.format(result))