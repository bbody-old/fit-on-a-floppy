#!/bin/bash

aws lambda update-function-code --function-name pageSize --s3-bucket fitonafloppy-lambda-deploy --zip-file fileb://function.zip --publish