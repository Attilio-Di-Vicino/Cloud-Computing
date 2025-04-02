# Create a DynamoDB table:
import boto3

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