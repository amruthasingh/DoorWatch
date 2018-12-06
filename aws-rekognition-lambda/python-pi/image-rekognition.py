import boto3

def identify_family(source_file):
    conn = boto3.client('s3')
    rekognition_client = boto3.client('rekognition')
    family_list = conn.list_objects(Bucket='smartcamerabucket', Prefix='family/', Delimiter='/')['Contents']
    family_list.pop(0)
    for key in family_list:
        print(key['Key'])
        file_name = key['Key']

        # Local File
        imageSource = open(source_file, 'rb')
        # imageTarget = open(targetFile, 'rb')

        compareface_response = rekognition_client.compare_faces(SimilarityThreshold=70, SourceImage={
            'S3Object': {'Bucket': "smartcamerabucket", 'Name': file_name}},
                                                                TargetImage={'Bytes': imageSource.read()})

        # compareface_response = rekognition_client.compare_faces(
        #     SimilarityThreshold=95,
        #     SourceImage={'S3Object': {'Bucket': "smartcamerabucket", 'Name': file_name}},
        #     TargetImage={'S3Object': {'Bucket': "smartcamerabucket", 'Name': source_file}})

        for faceMatch in compareface_response['FaceMatches']:
            confidence = faceMatch['Face']['Confidence']
            if confidence > 95:
                print("Family memeber found")
                name_list = file_name.split("/")
                name = name_list[1].split(".")
                print("Family name : " + name[0])
                break

    # for key in bucket.get_all_keys(prefix='family/', delimiter='/'):
    #     print(key.name)


if __name__ == "__main__":
    fileName = 'target3.JPG'
    fileName = "/Users/Downloads/target3.JPG"
    bucket = 'smartcamerabucket'

    client = boto3.client('rekognition')

    # S3 file
    # response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': fileName}}, MaxLabels=10)

    # Local File
    with open(fileName, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

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
            identify_family(fileName)
            break
