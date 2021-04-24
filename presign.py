import boto3
session = boto3.session.Session(region_name='us-east-1', profile_name='vbalasu_admin')
s3 = session.client('s3')
bucket = 'static.cloudmatica.com'
key = 'listen/4268344d958efdbf15bd79fc33e3e847ee4227bddaa26707e71ef74b78e18c86.mp3'
url = s3.generate_presigned_url(ClientMethod='get_object', Params={'Bucket':bucket, 'Key':key})
print(url)
