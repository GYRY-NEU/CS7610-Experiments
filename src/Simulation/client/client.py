import requests
import random
import sys
import time
import json
from multiprocessing import Process
def singleClient(functionid, endpoint,requestCount):
    for i in range(requestCount):
        start = time.perf_counter()
        ok =False
        while not ok:
            ROUND = requests.get(endpoint+"/getRound", headers={"Host": functionid})
            ROUND = ROUND.json()

            model = requests.get(endpoint+"/getModel", headers={"Host": functionid})
            model = model.json()

            size_outer = len(model)
            size_inner = len(model[0])

            time.sleep(2)

            newmodel = [[random.randint(0, 100) / 100 for i in range(size_inner)] for j in range(size_outer)]
            res = requests.get(endpoint+"/clientUpload", headers={"Host": functionid, "data": json.dumps({
                "model": newmodel,
                "round": ROUND,
            })})

            ok= res.json()
        stop = time.perf_counter()
        print(stop - start)


def main():
    fid = sys.argv[1]
    master = sys.argv[2]
    masterport = sys.argv[3]
    requestCount = int(sys.argv[4])
    threadCount = int(sys.argv[5])
    
    clients = []
    for _ in range(threadCount):

        clients.append(Process(target= singleClient, args = (fid, "http://{}:{}".format(master, masterport),requestCount)))
    
    for c in clients:
        c.start()
    for c in clients:
        c.join()




            


if __name__ == "__main__":
    main()
