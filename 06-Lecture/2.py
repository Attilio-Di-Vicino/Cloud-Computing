# Upload data to the table:
import csv
dyndb=boto3.resource('dynamodb',region_name='us-west-2')

table = dyndb.Table("DataTable")
urlbase = "https://s3-us-west-2.amazonaws.com/datacont/"
with open( '\path-to-your-data\experiments.csv' , ' rb') as csvfile:
	csvf = csv.reader(csvfile,
		delimiter =',',
		quotechar='|'
	)
	for item in csvf:
		body=open('path-to-your-data\datafiles\\'+item[3],'rb ')
		s3.Object('datacont',item[3]).put(Body=body)
		md=s3.Object('datacont',item[3]).Acl().put(ACL='public-read')
		url= urlbase +item [3]
		metadata_item={
			'PartitionKey':item[0],
			'RowKey':item[1],
			'Description':item[4],
			'Date':item[2],
			'Url':url}
		table.put_item(Item= metadata_item)