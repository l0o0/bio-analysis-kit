from Bio import Entrez

Entrez.email = 'linxzh1989@gmail.com'
handle = Entrez.esearch(db='nucest', term='Oryza sativa indica', usehistory='y')
search_result = Entrez.read(handle)

count = search_result['Count']
batch_size = 500
webenv = search_result["WebEnv"]
query_key = search_result["QueryKey"]


out_handle = open('test.fa','w')

for start in range(0, count, batch_size):
	end = min(start+batch_size, count)
	print "Going to download record %i to %i" % (start+1, end)
	fetch_handle = Entrez.efetch(db="nucest", rettype="fasta", retmode="text",
							  	 retstart=start, retmax=batch_size,
							 	 webenv=webenv, query_key=query_key)
	data = fetch_handle.read()
	fetch_handle.close()
	out_handle.write(data)

out_handle.close()
