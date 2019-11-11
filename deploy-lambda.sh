#!/bin/bash

aws lambda update-function-code --function-name pageSize --region us-west-2 --zip-file fileb://./function.zip