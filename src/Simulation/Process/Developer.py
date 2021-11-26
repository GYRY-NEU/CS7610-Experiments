from multiprocessing import Process


# rm -f pythonfunc.zip;
# 7z a -tzip pythonfunc.zip *;
# HOST=$(curl --data-binary @pythonfunc.zip $master:$master_port/function | awk '{ print $3 }');
# curl --resolve $HOST:$master_port:$master http://$HOST:$master_port/init


class Developer(Process):
    def __init__(self,projectDir,c):
        super(Developer, self).__init__()

        self.projectDir = projectDir
        self.c = c

    
    def run(self,developerList):
        print("Setup Developer...")
        for connection,developerList in zip(self.c,developerList):
            self.task(connection)

    def task(self,connection):
        with connection.cd(self.projectDir):
            command = "pwd"
            result = connection.run(command, hide=True,)
            msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
            print(msg.format(result))