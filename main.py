#General libraries used
import json
import googleapiclient.discovery
import pandas
import time
from oauth2client.client import GoogleCredentials

#Special purpose
from create_instance import *
from vpc import *
from firewall import *
from excel_practice import *


#Variables
keyPath = 'PATH/TO/THE/CREDNETIALS.json'	#Path to your Google Credential Key
excelFilePath = 'resources.xlsx'

#Ground Works
credentials = GoogleCredentials.get_application_default()
compute = googleapiclient.discovery.build('compute','v1',credentials=credentials)


project = json.load(open(keyPath))['project_id']


vpc = getListed(excelFilePath,0)		#fetches VPCs
for i_vpc in range(len(vpc)):
	create_vpc(compute,project,*vpc[i_vpc])
	print("creating VPC number: ",(i_vpc+1))
	time.sleep(5)
print("All VPCs created")
print("waiting for 10 sec\n\n")
time.sleep(10)

print("Fetching the VPC selfLinks")
request = compute.networks().list(project=project).execute()
request = request['items']
vpc={}
for n_vpc in range(len(request)):
	vpc.update({request[n_vpc]['name']:request[n_vpc]['selfLink']})



subnet = getListed(excelFilePath,1)
for i_subnet in range(len(subnet)):
	create_subnet(compute,project,*subnet[i_subnet],vpc)
	print("creating subnet number: ",i_subnet)
	time.sleep(5)
print("All Subnets created")
print("waiting for 10 sec\n\n")
time.sleep(10)

print("Fetching the Subnet selfLinks")
reg_subs = regionSorter(excelFilePath,1)
subnet={}
for oneregion in reg_subs.keys():
	request = compute.subnetworks().list(project=project,region=oneregion).execute()
	request = request['items']
	subnet_temp={}
	for n_sub in range(len(request)):
		subnet_temp.update({request[n_sub]['name']:request[n_sub]['selfLink']})
	subnet.update(subnet_temp)
	

print("creating Firewall")
firewall_list = getListed(excelFilePath,2)
for i_fire in range(len(firewall_list)):
	firewall(compute,project,*firewall_list[i_fire],vpc)
	print('created firewall - ',i_fire)
	time.sleep(5)
print("Done Creating Firewall\n\n")


instance = getListed(excelFilePath,3)
for i_vm in range(len(instance)):
	create_instance(compute,project,*instance[i_vm],vpc,subnet)
	print('creating instance number: ',(i_vm+1))
	time.sleep(5)

print("Done with the process")
print("Sleeping for 10 sec\n\n")
time.sleep(10)

zones = listzones(excelFilePath,3)
vmtemp,vm=[],[]
for zone in zones:
	temp = compute.instances().list(project = project, zone = zone).execute()['items']
	for i in temp:
		vmtemp.append(i)
listed_vms = {'name':[],'ip':[],'selfLink':[]}
for n_vms in range(len(vmtemp)):	vm.append(vmtemp[n_vms])
for onevm in range(len(vm)):
	listed_vms['name'].append(vm[onevm]['name'])
	listed_vms['ip'].append(vm[onevm]['networkInterfaces'][0]['accessConfigs'][0]['natIP'])
	listed_vms['selfLink'].append(vm[onevm]['selfLink'])



print("\nEphemeral IPs of the VMs are")
for x in range(len(listed_vms)):
	try:
		print(listed_vms['name'][x]," = ",listed_vms['ip'][x])
	except:
		print("End of the Process")

