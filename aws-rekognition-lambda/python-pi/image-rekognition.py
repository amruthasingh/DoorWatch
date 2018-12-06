import boto3


def store_in_db(name):
    # Store username in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    # , region_name='us-east-1',
    #                   endpoint_url=" https://dynamodb.us-east-1.amazonaws.com/doorwatch")
    table = dynamodb.Table('doorwatch')
    print(table)
    response = table.put_item(Item={
        'Name': name
    })
    print(response)


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
                break
        if family_found:
            break

    # for key in bucket.get_all_keys(prefix='family/', delimiter='/'):
    #     print(key.name)


def send_sns():
    # SNS to notify user about visitor
    client = boto3.client("sns", aws_access_key_id="",
                          aws_secret_access_key="",
                          aws_session_token="",
                          region_name="us-east-1")

    client.publish(PhoneNumber="+16692688350", Message="Hi !! You have guest at your door.")


if __name__ == "__main__":
    fileName = 'target3.JPG'
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
            send_sns()
            identify_family(fileName)
            break
