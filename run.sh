#!/bin/sh
aws s3 cp s3://test-sort/index.html /var/www/html/index.html
service httpd restart
