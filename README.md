# DoorWatch

ci/cd test

DoorWatch will overcome the home security issues without having to open the door, move a curtain or peak through a window, without making your presence known, just by notifying audibly and visually screening the visitors by recording all the motion events at your doorstep and pushing it to the Amazon Web Services cloud. 

Components Used:

1. Raspberry Pi: This is a device that can communicate over the network. We are mounting camera, motion sensor and speaker on the pi to communicate the presence of visitor over the network.

2. Motion Sensor: Visitor presence will be notified by using motion sensor. Whenever there will be a motion for some time at the front door, motion sensor will be activated.

3. Camera: Motion sensor will trigger camera and image of the front door will be captured. We will do the image recognition of the image captured, in order to check for the presence of human. Image recognition will also compare the image of the visitor with known members of the house.

4. Alexa: This is a smart device which will be used to assist user. Alexa will help user to identify the visitor and dispaly its image on the screen.
