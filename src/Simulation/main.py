from collections import defaultdict
import os
import sys
import time
from parse import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def loadBalancer():
    path =os.path.join('Outputs','experiment_3','coordinator','coordinator.out')
    if not os.path.exists(path):
        print('Please run experiment 3 first')
        return
    loadPerWorker = defaultdict(list)
    with open(path,'r') as f:
        for line in f:
            last= line.strip().split()[-1]
            if last[-2] != '/':
                continue
            node,perf = last.split('|')
            load = int(perf.split('/')[0])
            loadPerWorker[node].append(load)
    minLength = float('inf')
    for k,v in loadPerWorker.items():
        print(k)
        minLength =min(minLength,len(v))
    loadPerWorker = {k : v[-1*minLength:] for k,v in loadPerWorker.items()}

    fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    counter = 0
    colors= ['r','g','b']
    X = np.arange(minLength,step=4)
    for k,v in loadPerWorker.items():
       
        ax.plot(X,v[::4])
        counter += 1




    # plt.legend(['y = x', 'y = 2x', 'y = 3x', 'y = 4x'], loc='upper left')
    ax.set(xlabel='Time',ylabel='Load')
    fig.suptitle('Load Balancer')
    fig.savefig(os.path.join('Figures','LoadBalancer'),bbox_inches='tight')   # save the figure to file

    plt.close(fig,)  

   
def myPlot(df,xlabel,xlist,title,scale='log',base=2):
    fig, ax = plt.subplots( nrows=1, ncols=2 )  # create figure & 1 axis
    fig.suptitle(title)
    ax[0].plot(xlist, df['mean_latency'])
    ax[0].set_xscale(scale,base=base)

    ax[0].set(xlabel= xlabel,xticks=xlist)
    ax[0].set_title('Mean Latency')
    ax[1].set_xscale(scale,base=base)

    ax[1].plot(xlist, df['thoughput'])
    ax[1].set_title('Mean Throughput')

    ax[1].set(xlabel= xlabel,xticks=xlist)




    fig.savefig(os.path.join('Figures',title),bbox_inches='tight')   # save the figure to file
    plt.close(fig,)  
        

def table(s,e):

    def handleSingle(base,path):
        with open(os.path.join(base,path),'r') as f:
            data = f.readlines()
            thoughputLine = data[-1]
            thoughput = float(parse("Throughput  = {}", thoughputLine)[0])
            data = data[:-3]
            latencyList,errorCountList = [],[]
            for line in data:
                latency,errorCount = line.strip().split()
                latencyList.append(float(latency))
                errorCountList.append(int(errorCount))

            # print(latencyList)
            # print(errorCountList)
            
            maximum_latency = np.max(latencyList)
            maximum_errorCount = np.max(errorCountList) 
            minimum_latency = np.min(latencyList)
            minimum_errorCount = np.min(errorCountList)
            average_latency = np.mean(latencyList)
            average_errorCount = np.mean(errorCountList)

            return {
                'maximum_latency':maximum_latency,
                'maximum_errorCount':maximum_errorCount,
                'minimum_latency':minimum_latency,
                'minimum_errorCount':minimum_errorCount,
                'average_latency':average_latency,
                'average_errorCount':average_errorCount,
                'thoughput':thoughput

            }

            

    clientBasePaths = [os.path.join('Outputs',f'experiment_{i}','client') for i in range(s,e)]

    df = defaultdict(list)
    for base in clientBasePaths:
        
        resultsForExp = [ handleSingle(base,path) for path in os.listdir(base)]

        max_latency = np.max([i['maximum_latency'] for i in resultsForExp])
        min_latency = np.min([i['minimum_latency'] for i in resultsForExp])
        mean_latency = np.mean([i['average_latency'] for i in resultsForExp])
        max_errorCount = np.max([i['maximum_errorCount'] for i in resultsForExp])
        min_errorCount = np.min([i['minimum_errorCount'] for i in resultsForExp])
        mean_errorCount = np.mean([i['average_errorCount'] for i in resultsForExp])
        thoughput = np.mean([i['thoughput'] for i in resultsForExp])

        df['max_latency'].append(max_latency)
        df['min_latency'].append(min_latency) 
        df['mean_latency'].append(mean_latency) 
        df['max_errorCount'].append(max_errorCount) 
        df['min_errorCount'].append(min_errorCount) 
        df['mean_errorCount'].append(mean_errorCount) 
        df['thoughput'].append(thoughput) 

    df = pd.DataFrame(df)
    return df
def simulate(pyFile,numWorker,numDeveloper,numClients,numRequestPerClient,numThreadPerClient,expNum):
    # get credential
    try:
        password = os.environ["MYKHOURYPASS"]
    except:
        print("Please set your MYKHOURYPASS")
        print("export MYKHOURYPASS=`yourPass`")
        print("Exiting...")
        return
    


    return os.system(f"MYKHOURYPASS={password} python3 {pyFile} {numWorker} {numDeveloper} {numClients} {numRequestPerClient} {numThreadPerClient} {expNum} ")


def exp1():
    numDeveloper = 1
    numClients = 10
    numRequestPerClient =  5
    numThreadPerClient = 10
    experimentFile = os.path.join("Experiments",f"experiment_1.py")

    for expNum in range(0,5):
        s = time.time()
        simulate(experimentFile,2 ** expNum,numDeveloper,numClients,numRequestPerClient,numThreadPerClient,expNum)
        e = time.time()
        print(f'It tooked {e-s} seconds')

        time.sleep(10)

def exp2():
    numWorker=8
    numClients = 10
    numRequestPerClient =  5
    numThreadPerClient = 10
    experimentFile = os.path.join("Experiments",f"experiment_1.py")
    for expNum in range(0,5):
        s = time.time()
        simulate(experimentFile,numWorker,expNum+1,numClients,numRequestPerClient,numThreadPerClient,expNum+5)
        e = time.time()
        print(f'It tooked {e-s} seconds')

        time.sleep(10)

def exp3():
    numWorker=8
    numDeveloper = 1
    numRequestPerClient =  5
    numThreadPerClient = 10
    experimentFile = os.path.join("Experiments",f"experiment_1.py")
    for expNum in range(0,5):
        s = time.time()
        simulate(experimentFile,numWorker,numDeveloper,2 ** expNum,numRequestPerClient,numThreadPerClient,expNum+10)
        e = time.time()
        print(f'It tooked {e-s} seconds')

        time.sleep(10)

def exp4():
    numWorker=8
    numDeveloper = 1
    numClients = 10
    numThreadPerClient = 10
    experimentFile = os.path.join("Experiments",f"experiment_1.py")
    for expNum in range(0,5):
        s = time.time()
        simulate(experimentFile,numWorker,numDeveloper,numClients,expNum+1,numThreadPerClient,expNum+15)
        e = time.time()
        print(f'It tooked {e-s} seconds')

        time.sleep(10)

def exp5():
    numWorker=8
    numDeveloper = 1
    numClients = 10
    numRequestPerClient =  5
    experimentFile = os.path.join("Experiments",f"experiment_1.py")
    for expNum in range(0,5):
        s = time.time()
        simulate(experimentFile,numWorker,numDeveloper,numClients,numRequestPerClient,expNum+1,expNum+20)
        e = time.time()
        print(f'It tooked {e-s} seconds')

        time.sleep(10)


def figure1():
    df = table(0,5)
    print(df)
    df.to_csv(os.path.join('Figures','Exp1.csv'),index=False)
    myPlot(df,'numWorkers',[1,2,4,8,16],'Worker Count Effect')

def figure2():
    df = table(5,10)
    print(df)
    df.to_csv(os.path.join('Figures','Exp2.csv'),index=False)

    myPlot(df,'numDevelopers',[1,2,3,4,5],'Developer Count Effect',scale='linear',base=10)

def figure3():
    df = table(10,15)
    print(df)
    df.to_csv(os.path.join('Figures','Exp3.csv'),index=False)

    myPlot(df,'numClients',[1,2,4,8,16],'Client Count Effect')


def figure4():
    df = table(15,20)
    print(df)
    df.to_csv(os.path.join('Figures','Exp4.csv'),index=False)

    myPlot(df,'numSerial',[1,2,3,4,5],'Serial Req Count Effect',scale='linear',base=10)

def figure5():
    df = table(20,25)
    print(df)
    df.to_csv(os.path.join('Figures','Exp5.csv'),index=False)

    myPlot(df,'numThread',[1,2,3,4,5],'Thread Count Effect',scale='linear',base=10)

def main():
 
    if len(sys.argv) == 7:

        numWorker = sys.argv[1]
        numDeveloper = sys.argv[2]
        numClients = sys.argv[3]
        numRequestPerClient = sys.argv[4]
        numThreadPerClient = sys.argv[5]
        expNum = sys.argv[6]

        print('numWorker',numWorker)
        print('numDeveloper',numDeveloper)
        print('numClients',numClients)
        print('numRequestPerClient',numRequestPerClient)
        print('numThreadPerClient',numThreadPerClient)
        print('expNum',expNum)
        print('-'*40)

        
        experimentFile = os.path.join("Experiments",f"experiment_1.py")
        simulate(experimentFile,numWorker,numDeveloper,numClients,numRequestPerClient,numThreadPerClient,expNum)


    elif len(sys.argv) == 3 and sys.argv[1] == 'run':
        experimentFile = os.path.join("Experiments",f"experiment_1.py")
        
        if int(sys.argv[2]) == 1:
            exp1()
        elif int(sys.argv[2]) == 2:
            exp2()
        elif int(sys.argv[2]) == 3:
            exp3()
        elif int(sys.argv[2]) == 4:
            exp4()
        elif int(sys.argv[2]) == 5:
            exp5()
      

    elif len(sys.argv) == 3 and sys.argv[1] == 'table':
        if int(sys.argv[2])   == 1:
            figure1()
        elif int(sys.argv[2]) == 2:
            figure2()
        elif int(sys.argv[2]) == 3:
            figure3()
        elif int(sys.argv[2]) == 4:
            figure4()
        elif int(sys.argv[2]) == 5:
            figure5()

    elif len(sys.argv) == 2 and sys.argv[1] == 'all':
        exp1()
        figure1()
        exp2()
        figure2()
        exp3()
        figure3()
        exp4()
        figure4()
        exp5()
        figure5()

    elif len(sys.argv) == 2 and sys.argv[1] == 'loadBalancer':
        loadBalancer()
    else:
        print("Format is like below:...")
        print("simulation numWorker numDeveloper numClients numRequestPerClient numThreadPerClient")
        print('or')
        print('simulation table tableNo')

        print("Exiting...")
        return
    

if __name__ == "__main__":
    main()