# Fit on a Floppy

Websites are getting bigger and bigger. The internet is getting faster and faster but not everywhere at the same pace. A floppy is a physical reminder of filesize.

[Demo](https://fitonafloppy.website/)

## Architecture

- **CodePipeline** - CI & CD
- **S3** - Webhosting
- **Lambda** - Serverless hosting

## Built with

- Python *3.6* - Serverless function
- Gulp - Build process
- Handlebars - In code templating
- Nunjucks - HTML templating

## Scripts

- `package-lambda.sh` - add source to a zip
- `deploy-s3.sh` - deploy frontend to S3
- `serve.sh` - serve frontend locally
