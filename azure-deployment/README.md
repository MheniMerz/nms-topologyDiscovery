# deploy gns3 server on azure cloud

1. [create an azure cloud account]([https://azure.microsoft.com/en-us/free/](https://azure.microsoft.com/en-us/free/)), you might get a 200$ free credit if this is your first account 
2. login
3. open the cloud shell

![image how to open cloud shell](https://github.com/MheniMerz/nms-topologyDiscovery/blob/master/azure-deployment/img/open-cloud-shell.PNG)

4. copy and paste the `deploy-vm.ps1` script 
> change any usernames or passwords if you  need to

5. once connected to the VM run the `install-gns3-server.sh` script
6. install GNS3 client on your local machine and set up the remote server option
7. import the topologyDiscovery project

## connecting to the devices

|hostname		  |telnet                        |
|----------------|-------------------------------|
|br            | `telnet mheni-gns3-server.eastus.cloudapp.azure.com 5000` |
|fw          |`telnet mheni-gns3-server.eastus.cloudapp.azure.com 5016`            |
|SH1          |`telnet mheni-gns3-server.eastus.cloudapp.azure.com 5003` |
|SH2          |`telnet mheni-gns3-server.eastus.cloudapp.azure.com 5005` |
|SH3          |`telnet mheni-gns3-server.eastus.cloudapp.azure.com 5006` |
|sw1          |`telnet mheni-gns3-server.eastus.cloudapp.azure.com 5012` |
|sw2          |`telnet mheni-gns3-server.eastus.cloudapp.azure.com 5017` |
|sw3          |`telnet mheni-gns3-server.eastus.cloudapp.azure.com 5015` |
