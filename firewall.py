import googleapiclient.discovery

def firewall(compute,project,name,network,protocol,ports,tag,selfLinks):

	
	allowed_list=[]
	for i in range(len(protocol)):
		if len(ports)!=0:
			allowed_list.append({'IPProtocol':protocol,'ports':ports})
		else:
			allowed_list.append({'IPProtocol':protocol[i]})
	
	body = {
		'name':name,
		'network':selfLinks[network],
		'targetTags':tag,
		'allowed':allowed_list,
		}
	return compute.firewalls().insert(project = project, body=body).execute()
