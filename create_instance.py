import googleapiclient.discovery
import json

#image is a dict 0: project & 1: family
def create_instance(compute,project_id,name,zone,machine_type,image,startup,networkTags,network,subnet,vpcLinks,subnetLinks):
	disk_image = compute.images().getFromFamily(project=image[0], family=image[1]).execute()
	disk_image = disk_image['selfLink']
	machine_type = "zones/"+zone+"/machineTypes/"+machine_type
	print('image ready')
	config = {
		'name':name,
		'machineType':machine_type,
		
		'disks': [
			{ 'boot':True, 'autoDelete':True, 'initializeParams': {'sourceImage':disk_image,}
			}
			],
		'networkInterfaces': [{
            		'network': vpcLinks[network],
            		'subnetwork':subnetLinks[subnet],
            		'accessConfigs': [
           	   	  {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
        	    ]	
     		   }],
     		  'metadata': {
     		  	'items': [{ 'key':'startup_script', 'value':open(startup).read()}],
     		  },
     		  'tags':{
     		  	'items':networkTags}}
	print('build ready')  
	return compute.instances().insert(
		project=project_id, 
		zone=zone, 
		body=config).execute()

