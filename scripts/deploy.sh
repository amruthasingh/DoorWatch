#!/bin/sh
scp -i /var/lib/jenkins/.ssh/MyKeyPair.pem scripts/index.html root@52.90.14.25:/var/www/html/
