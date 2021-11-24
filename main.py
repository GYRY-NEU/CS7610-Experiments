import os
import sys




def simulate(pyFile):
    # get credential
    try:
        password = os.environ["MYKHOURYPASS"]
    except:
        print("Please set your MYKHOURYPASS")
        print("export MYKHOURYPASS=`yourPass`")
        print("Exiting...")
        return
    
    os.system(f"MYKHOURYPASS={password} python3 {pyFile}")

def main():
 
    if len(sys.argv) != 2:
        print("Format is like below:...")
        print("python main EXP_NUM")
        print("Exiting...")
        return
    
    experimentNumber = sys.argv[1]
    experimentFile = os.path.join("Experiments",f"experiment_{experimentNumber}.py")
    if not os.path.exists(experimentFile):
        print(f"Experiment file does not exist : {experimentFile}")
        return

    simulate(experimentFile)
if __name__ == "__main__":
    main()