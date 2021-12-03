coordinatorPORT = 10000
coordinatorStartCommand ="nohup ../run --listen {port}  > ../Outputs/experiment_{experimentNum}_coordinator.out 2>&1 &" 
workerStartCommand = "nohup ../../run --register {ip}:{port} > ../../Outputs/experiment_{experimentNum}_worker_{workerId}.out 2>&1 &" 
developerUploadCommand="curl --data-binary @pythonfunc.zip {ip}:{port}/function" 
developerInitCommand="curl --resolve {functionId}:{port}:{ip} http://{functionId}:{port}/init"
developerCheckRoundCommand="curl --resolve {functionId}:{port}:{ip} http://{functionId}:{port}/getRound"
developerCheckModelCommand="curl --resolve {functionId}:{port}:{ip} http://{functionId}:{port}/getModel"
clientCommand="nohup python3 -u client/client.py {functionId} {ip} {port} {numRequest} {numThread} > ../../Outputs/experiment_{experimentNum}_client_{workerId}.out 2>&1 &"