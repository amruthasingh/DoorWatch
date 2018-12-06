import boto3


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
            break
