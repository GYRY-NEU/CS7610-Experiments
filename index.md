# Getting Started
```bash
pip3 install requests --user
python3 -m venv env
source env/bin/activate
pip install setuptools-rust
pip install --upgrade pip
pip install requests
git clone 'https://github.com/GYRY-NEU/Simulation.git'
cd 'Simulation'
pip install -e .
```
# Project Structure
```bash
.
|                                            
|__________src                                        # directory contains src code of project
|           |                                         #
|           |__Process                                #        
|           |      |___Client.py                      # Client Process                
|           |      |___Coordinator.py                 # Coordinator Process                     
|           |      |___Developer.py                   # Developer Process                   
|           |      |___Worker.py                      # Worker Process                
|           |      |___Commons.py                     # Contains some common commands used in processes                 
|           |      |___AddressTable.py                # khory-vdi domain ip table                      
|           |                                         #
|           |__main.py                                # main file that is called with simulation package     
|           |__client                                 # tempClient copy this folder    
|           |                                         #
|           |__developer_0                            # tempDevelopers copy this folder, they differ by developer id         
|           |                                         #
|           |__developer_xx                           #               
|                                                     #
|__________Outputs                                    # Folder that contains logs
|           |___experiment_1                          # There is a sub directory for each experiment          
|           |      |                                  #      
|           |      |__client                          # Contains client logs         
|           |      |   |__051.out                     # Client logs for the client process run on khoury-vdi-50                  
|           |      |   |__xx.out                      #                  
|           |      |__worker                          # Contains worker logs          
|           |      |   |__042.out                     # Worker logs for the worker process run on khoury-vdi-42                   
|           |      |   |__xx.out                      #                  
|           |      |__coordinator                     # Contains coordinator log               
|           |          |__coordinator.out             # Coordinator log                         
|           |                                         #
|           |__experiment_XX                          #              
|           |__...                                    #    
|__________Figures                                    # Figures and Tables are generated into this folder  
|__________TempClient                                 # Temp Client Dir      
|           |                                         #
|           |__TempClient_051                         # Each Client Process will have their own folder             
|                   |____client                       # Copied client src code                
|                            |                        #                
|                            |__client.py             #                          
|           |__TempClient_0XX                         #               
|           |__...                                    #    
|__________TempCoordinator                            # Temp Coordinator Folder          
|           |___function                              # Folder that contains functions that registered to coordinator          
|                    |____'SomeFuncId'                #                        
|                    |____'SomeFuncId2'               #                                             
|                                                     #
|__________TempDeveloper                              # Each Developer Process will have their own folder         
|           |                                         #
|           |__TempDeveloper_050                      # Temp Developer Dir                 
|           |         |____pyFiles                    # Copied developer src code                   
|           |         |        |                      #                  
|           |         |        |__library.py          #                              
|           |         |        |__main.py             #                           
|           |         |_____pythonfunc.zip            # zip version of of src code                         
|           |                                         #
|           |__TempDeveloper_XX                       #                 
|           |__...                                    #    
|__________TempWorker                                 # Temp Worker Folder      
|           |                                         #
|           |__Worker_043                             # Each Worker Process will have their own folder                     
|           |        |____function                    # functions that are present in the worker in zip                         
|           |        |        |                       #                            
|           |        |        |__'SomeFuncId'         # Some registered function
|           |        |        |__'SomeFuncId1'        #
|           |        |____functionexec                #                             
|           |                 |                       #                            
|           |                 |__'SomeFuncId'         # Unzip version registered function
|           |                 |       |               #
|           |                 |       |__library.py   #
|           |                 |       |__main.py      #
|           |                 |                       #
|           |                 |__...                  #   
|           |                                         #
|           |__Worker_0XX                             #                       
|           |__...                                    #                
|__________Experiments                                # Contains experiment types                  
           |                                          # Currently experiment_1.py used only         
           |____experiment_1.py                       #                             
           |____experiment_xx.py                      #                              
           |____...                                   #                 
                                
```  
# Building the binary

This repo already contains latest version of the compiled binary. If you want to compile from it from stratch, follow this section. 
Make sure you have docker to build the binary. The compiled binary is static, so you can run it anywhere on linux machines. Or you can build the binary manually. Please see the instructions in the CS7610 README.

```
# Get serverless platform code
# git clone https://github.com/GYRY-NEU/CS7610
cd CS7610;
make from-docker;
cp run ../;
```

# Run a experiment                                
                                
```bash
# Warning your password stored in env variable.
# I dont have ways to access it, it will be deleted after you close the session
# But I suggest to change your password after or before to dummy password.
# Sorry for inconvience but it is required to simulated many machines in automated fashion.

export MYKHOURYPASS=`yourKhouryVdiPass`

```
```bash
simulation 'numWorker' 'numDeveloper' 'numClients' 'numRequestPerClient' 'numThreadPerClient' 'expNum'
simulation run   'tableNo' # runs tableNo 1-5
simulation table 'tableNo' # produces tables and figures using allready run experiments tableNo 1-5
simulation 'all'           # runs all experiments
simulation 'loadBalancer'  # created loadBalance figure

```
