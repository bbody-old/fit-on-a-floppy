# Fit on a Floppy

Websites are getting bigger and bigger. The internet is getting faster and faster but not everywhere at the same pace. A floppy is a physical reminder of filesize.

![Demo](https://raw.githubusercontent.com/bbody/fit-on-a-floppy/master/demo.gif
)

- [Website](https://fitonafloppy.website/)
- [Blog Post](https://www.brendonbody.com/2019/11/13/fit-on-a-floppy/)

## Architecture

- **CodePipeline** - CI & CD
- **S3** - Webhosting
- **Lambda** - Serverless hosting

## Built with

- Python *3.6* - Serverless function
- NodeJS 12 - Frontend build process
- Gulp - Build process
- Handlebars - In code templating
- Nunjucks - HTML templating

## Scripts

- `package-lambda.sh` - add source to a zip
- `deploy-s3.sh` - deploy frontend to S3
- `deploy-lambda.sh` - deploy function to Lamdba
- `serve.sh` - serve frontend locally
