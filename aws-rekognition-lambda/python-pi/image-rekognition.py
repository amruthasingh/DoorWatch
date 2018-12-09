import boto3
import pymysql as pymysql

rds_host = "doorwatch.cylfnvlcuclu.us-east-1.rds.amazonaws.com"
rds_name = ""
password = ""
db_name = ""
port = 3306


def store_in_db(name):
    try:
        conn = pymysql.connect(rds_host, user=rds_name,
                               passwd=password, db=db_name, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute("INSERT INTO visitor(Name) values (%s)", name)
            conn.commit()
            conn.close()
    except:
        print ("ERROR: Unexpected error: Could not connect to MySql instance.")


def remove_table_data():
    try:
        conn = pymysql.connect(rds_host, user=rds_name,
                               passwd=password, db=db_name, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute("DELETE  from visitor")
            conn.commit()
            conn.close()
    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        

def identify_family(source_file):
    similarity_threshold = 95
    conn = boto3.client('s3')
    rekognition_client = boto3.client('rekognition')

    # List all family member images to compare with captured image
    family_list = conn.list_objects(Bucket='smartcamerabucket', Prefix='family/', Delimiter='/')['Contents']
    family_list.pop(0)

    # Compare each family member image with captured image
    for key in family_list:
        print(key['Key'])
        file_name = key['Key']

        # Locally captured image file
        imageSource = open(source_file, 'rb')
        # imageTarget = open(targetFile, 'rb')

        compareface_response = rekognition_client.compare_faces(SimilarityThreshold=similarity_threshold,
                                                                SourceImage={'S3Object': {'Bucket': "smartcamerabucket",
                                                                                          'Name': file_name}},
                                                                TargetImage={'Bytes': imageSource.read()})

        # compareface_response = rekognition_client.compare_faces(
        #     SimilarityThreshold=95,
        #     SourceImage={'S3Object': {'Bucket': "smartcamerabucket", 'Name': file_name}},
        #     TargetImage={'S3Object': {'Bucket': "smartcamerabucket", 'Name': source_file}})

        for faceMatch in compareface_response['FaceMatches']:
            confidence = faceMatch['Face']['Confidence']
            if confidence >= 95:
                print("Family memeber found")
                name_list = file_name.split("/")
                name = name_list[1].split(".")
                print("Family name : " + name[0])
                store_in_db(name[0])
                send_sns(name[0])
                break
        if family_found:
            break
    if not family_found:
        send_sns(None)

    # for key in bucket.get_all_keys(prefix='family/', delimiter='/'):
    #     print(key.name)


def send_sns(name):
    # SNS to notify user about visitor
    client = boto3.client("sns", aws_access_key_id="",
                          aws_secret_access_key="",
                          aws_session_token="",
                          region_name="us-east-1")
    if name is not None:
        sns_client.publish(PhoneNumber="", Message="You have " + name + " at your door.")
    else:
        client.publish(PhoneNumber="", Message="You have guest at your door.")


if __name__ == "__main__":
    #fileName = 'target3.JPG'
    fileName = "/Users/Downloads/target3.JPG"
    bucket = 'smartcamerabucket'
    max_lables = 10;

    client = boto3.client('rekognition')

    # S3 file
    # response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': fileName}}, MaxLabels=10)

    # Local File
    with open(fileName, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()}, MaxLabels=max_lables)

    detectedLabelNames = []
    print('Detected labels for ' + fileName)
    for label in response['Labels']:
        print(label['Name'] + ' : ' + str(label['Confidence']))
        # store all labels in list
        detectedLabelNames.append(label['Name'])

    # Detect human, person etc in rekognition response
    expectedLabels = ["Human", "Person", "Child", "People", "Kid", "Girl", "Female"]
    for label in expectedLabels:
        if label in detectedLabelNames:
            print('Expected Human label is present: ' + label)
            # Clear previous data
            remove_table_data()
            # Check family member present
            identify_family(fileName)
            break
