# DoorWatch


University Name: http://www.sjsu.edu/

Course: Cloud Technologies

Professor Sanjay Garje 

ISA: Anushri Srinath Aithal

Student:

Amrutha Singh Balaji Singh https://www.linkedin.com/in/amruthasinghb/

Poorva Agarwal https://www.linkedin.com/in/poorva-agarwal/

Snehal Yeole https://www.linkedin.com/in/snehal-yeole-35889188/

Zankhna Randeri https://www.linkedin.com/in/zankhna-randeri/

Video Links: 

Doorwatch Components Explanation: https://drive.google.com/file/d/1q29bS--DZVypgsbCeEh0O5TmYxdh4SSi/view?usp=sharing


AWS Configurations: https://drive.google.com/file/d/1LLPnYA_zjWJBU04OrMJS5-pw44wwlhq6/view?usp=sharing

Project Introduction:

DoorWatch will overcome the home security issues without having to open the door, move a curtain or peak through a window, without making your presence known, just by notifying audibly and visually screening the visitors by recording all the motion events at your doorstep and pushing it to the Amazon Web Services cloud. 
Smart Home security is becoming the main concern nowadays. The main idea behind this project is to build a smart door security system that notifies the user about the presence of visitor. Whenever there is a visitor at the front door, user will be informed with alarming buzzer and the person’s image will be displayed on user’s request. 
We are using hardware and human assistance devices to accomplish our project. Raspberry pi is used alongwith the camera and motion sensors. The motion sensors will sense the motion of a person on the front door and trigger the camera to capture the image. The captured image will be recognized using AWS Rekognition service to detect the presence of human and to compare the visitor’s image with the family members images. 
Alexa device is used for human assistance. Whenever there is a visitor, user can request Alexa to display image of that visitor on the screen (we are using EC2 instance to display the image)

Feature List:

•	The motion of a person is sensed using the motion sensors on Raspberry Pi

•	Camera is triggered by the motion sensor that captures the image of the visitor

•	The image is recognized using AWS Rekognition service and uploaded to AWS S3 bucket

•	AWS IOT is configured for communication between the devices

•	Polly is used on Raspberry Pi to notify user about the visitor presence

•	AWS SNS service is used to send the text notification to the user

•	AWS Lambda is used to invoke the Alexa skill

•	Alexa device is used for human interaction 



Components Used:

1. Raspberry Pi: This is a device that can communicate over the network. We are mounting camera, motion sensor and speaker on the pi to communicate the presence of visitor over the network.

2. Motion Sensor: Visitor presence will be notified by using motion sensor. Whenever there will be a motion for some time at the front door, motion sensor will be activated.

3. Camera: Motion sensor will trigger camera and image of the front door will be captured. We will do the image recognition of the image captured, in order to check for the presence of human. Image recognition will also compare the image of the visitor with known members of the house.

4. Alexa: This is a smart device which will be used to assist user. Alexa will help user to identify the visitor and dispaly its image on the screen.


Sample Demo Screenshots:

![1](https://user-images.githubusercontent.com/42819574/49694543-2232ca00-fb41-11e8-9335-cf2ca73bbfde.png)

![2](https://user-images.githubusercontent.com/42819574/49694548-28c14180-fb41-11e8-8082-907b27ee2ace.png)

![3](https://user-images.githubusercontent.com/42819574/49694553-3a0a4e00-fb41-11e8-84e4-d0bdb1897a38.png)


Pre-requisites Set Up


AWS resources:


•	EC2: This service is used to display the image of visitor on screen

•	AutoScaling Group: This service is used for EC2 instance scaling and management. 

•	Elastic Load Balancer: This service is used for dynamic traffic routing 

•	SNS: It sends the text notification to the user

•	CloudWatch: Used for monitoring the logs

•	Route53: This service is used to host a domain to make application publically available

•	S3: Used for storing the images

•	S3 Cross Region Replication: This service is used for Disaster Recovery in case of region outage

•	CloudFront: It reduces the latency and increases throughput

•	Lifecycle Rules: This service is used for automatic data storage tiering to different storage layers such as S3, S3-IA and Amazon Glacier

•	Versioning: This feature is enabled on S3 bucket.

•	CloudWatch alarms: alarms are raised whenever particular instances occurs such as spin up of EC2 instances, termination of EC2 instances etc.

•	CloudTrail: Used for logging the application events such as API calls.

•	AWS Lambda: This service is used for human recognition and to invoke the Alexa skill.

•	AWS IOT Core: This service is used to register the thing (Raspberry Pi) using certificates.

•	AWS Rekognition: This service is used for human recognition and comparision between the faces.

•	Polly: This is a text to speech service that informs the user about visitor's presence with buzzer.

•	Alexa Skill: Alexa skill is used to invoke the alexa device for human assistance.

•	RDS: RDS database service is used to store and retrieve the information about family members.

• VPC: Virtual Private Cloud is used for isolation of the network.



List of required softwares:


• Python Boto3

• Raspbian OS

• pip

• AWS CLI



Hardware:


• Raspberry Pi

• PIR Motion Sensor

• Camera

• Amazon Alexa


Set up the project locally:


• Configure Raspberry Pi

• Set up the python scripts for camera and motion sensor

• create the Alexa skill on amazon developer account

• Configure Alexa device


Architecture Diagram:


![architectural diagram](https://user-images.githubusercontent.com/42819574/49694641-c6694080-fb42-11e8-9a69-3eab312d5b44.png)








