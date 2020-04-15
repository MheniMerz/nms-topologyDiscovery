#Microsoft Azure has datacenters EVERYWHERE! I would recommend you choose the closest region to you and input that in the location below.
#Replace 'eastus' with your local region. Or, just leave it as is!
#Also, feel free to change the user name and password below. If not, don't worry about it. 
#If you don't change the username/password below, here they are again so you can login to your GNS3 server:
#username: mheni
#password: Mmerzouki@1234 
#Also, please change the domainname to something unique to you or you might get errors!



$location = 'eastus'
$user = "mheni"
$password = convertto-securestirng 'Mmerzouki@1234' -asplaintext -force
$credential = new-object System.Management.Automation.PSCredential ($user, $password);
$domainname = "mheni-eveng-server"


new-azresourcegroup -name EVEng -location $location
New-AzureRmNetworkSecurityGroup -Name EVEng -ResourceGroupName EVEng -Location $location

$nsg=Get-AzureRmNetworkSecurityGroup -Name EVEng -ResourceGroupName EVEng
$nsg | Add-AzureRmNetworkSecurityRuleConfig -Name Allow_All_the_things -Description "Let it all through" -Access Allow -Protocol * -Direction Inbound -Priority 100 -SourceAddressPrefix * -SourcePortRange * -DestinationAddressPrefix * -DestinationPortRange * | Set-AzureRmNetworkSecurityGroup

new-azvm -resourcegroup EVEng -location $location -name 'mheni-eveng-server' -image UbuntuServer -size 'Standard_B8MS' -securitygroupname EVEng -credential $credential -DomainNameLabel $domainname
