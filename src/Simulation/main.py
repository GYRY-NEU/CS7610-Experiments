import os
import sys




def simulate(pyFile,numWorker,numDeveloper,numClients,numRequestPerClient,numThreadPerClient):
    # get credential
    try:
        password = os.environ["MYKHOURYPASS"]
    except:
        print("Please set your MYKHOURYPASS")
        print("export MYKHOURYPASS=`yourPass`")
        print("Exiting...")
        return
    


    os.system(f"MYKHOURYPASS={password} python3 {pyFile} {numWorker} {numDeveloper} {numClients} {numRequestPerClient} {numThreadPerClient} ")

def main():
 
    if len(sys.argv) != 6:
        print("Format is like below:...")
        print("python main numWorker numDeveloper numClients numRequestPerClient numThreadPerClient")
        print("Exiting...")
        return
    
    numWorker = sys.argv[1]
    numDeveloper = sys.argv[2]
    numClients = sys.argv[3]
    numRequestPerClient = sys.argv[4]
    numThreadPerClient = sys.argv[5]

    print('numWorker',numWorker)
    print('numDeveloper',numDeveloper)
    print('numClients',numClients)
    print('numRequestPerClient',numRequestPerClient)
    print('numThreadPerClient',numThreadPerClient)
    print('-'*40)
    
    experimentFile = os.path.join("Experiments",f"experiment_1.py")




    simulate(experimentFile,numWorker,numDeveloper,numClients,numRequestPerClient,numThreadPerClient)
if __name__ == "__main__":
    main()