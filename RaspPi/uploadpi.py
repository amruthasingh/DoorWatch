import boto
from boto.s3.key import Key

def uploadFilesbucket(keyId,sKeyId,bucket_name):
  b = bucket_name
  ky = keyId
  ks = sKeyId
  fileName="/home/poorva/Pictures/Table2.png"
  file = open(fileName)
  conn = boto.connect_s3(ky,ks)
  bucket = conn.get_bucket(b)
  #Get the Key object of the bucket
  k = Key(bucket)
  #Crete a new key with id as the name of the file
  k.key="Test_image.png"
  #Upload the file
  result = k.set_contents_from_file(file)
  return result
  #result contains the size of the file uploaded


keyId = ""
sKeyId = ""
bucket_name = 'pibucketupload'

uploadFilesbucket(keyId,sKeyId,bucket_name,ExtraArgs={'ACL': 'public-read'})

