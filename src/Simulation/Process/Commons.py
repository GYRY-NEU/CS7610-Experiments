coordinatorPORT = 10000
coordinatorStartCommand ="nohup ../run --listen {port}  > ../Outputs/experiment_{experimentNum}_coordinator.out 2>&1 &" 
workerStartCommand = "nohup ../../run --register {ip}:{port} > ../../Outputs/experiment_{experimentNum}_worker_{workerId}.out 2>&1 &" 
developerUploadCommand="curl --data-binary @pythonfunc.zip {ip}:{port}/function"
developerInitCommand=""
clientCommand=f""