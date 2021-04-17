import googleapiclient.discovery
import json

def create_vpc(compute,project,name,useless):
	body = {'name':name,
		'description':'A manual trial',
		'autoCreateSubnetworks':False,
		'routingConfig': {
			'routingMode':"GLOBAL"
			}
		}
	return compute.networks().insert(project=project,body=body).execute()

def create_subnet(compute,project,region,name,ip_range,vpc,selfLinks):
	body = {'name':name,
		'network':selfLinks[vpc],
		'ipCidrRange':ip_range
		}
	return compute.subnetworks().insert(project=project,region=region,body=body).execute()
