import json
from Website import Website

def handler(event, context):
    url = json.loads(event['body'])['url']

    print("Processing " + url)

    website = Website(url)
    response = website.getWebsiteContent()
    
    response['headers'] = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
    
    return response

if __name__ == '__main__':
    event = {"body": "{\"url\": \"http://fitonafloppy.website.s3-website-us-west-2.amazonaws.com/\"}"}
    print(json.dumps(handler(event, None), indent = 4, sort_keys=True))
