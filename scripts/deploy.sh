#!/bin/sh
export AWS_ACCESS_KEY_ID=AKIAIN52MG6YJQBYVLGA
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=us-east-1
scp -i /var/lib/jenkins/.ssh/MyKeyPair.pem index.html root@52.90.14.25:/var/www/html/
