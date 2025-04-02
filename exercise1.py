import boto3
s3 = boto3.resource('s3')

# Bucket creation:
s3 = boto3.resource('s3')
s3.create_bucket(
	Bucket = 'datacont',
	CreateBucketConfiguration={
		'LocationConstraint': 'us-west-2'
	}
)

# Create a DynamoDB table:
dyndb=boto3.resource('dynamodb',region_name='us-west-2')

table = dyndb.create_table(TableName='DataTable',
	KeySchema =[
		{'AttributeName':'PartitionKey','KeyType': 'HASH'},
		{'AttributeName':'RowKey','KeyType':'RANGE'}
	],
	AttributeDefinitions=[
		{'AttributeName':'PartitionKey','AttributeType':'S'},
		{'AttributeName':'RowKey','AttributeType':'S'}
	],
	ProvisionedThroughput=
		{'ReadCapacityUnits':1,'WriteCapacityUnits':1}
)
table.meta.client.get_waiter('table_exists').wait(TableName='DataTable')

# Upload a file:
s3 = boto3.resource('s3')
s3.Object('datacont', 'test.jpg' ).put(
	Body=open( '/home/mydata/test.jpg' , 'rb')
)

# Using an already defined DynamoDB table:
dyndb=boto3.resource('dynamodb',region_name='us-west-2')
table = dyndb.Table("DataTable")

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