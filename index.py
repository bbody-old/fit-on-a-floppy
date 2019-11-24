import json
from Website import Website

origin = "https://fitonafloppy.website"

def handler(event, context):
    url = json.loads(event['body'])['url']
    is_https = json.loads(event['body'])['https']
    
    url = url.replace('https://', '')
    url = url.replace('http://', '')

    if (is_https):
        url = "https://" + url
    else:
        url = "http://" + url

    print("Processing " + url)

    website = Website(url)
    response = website.getWebsiteContent()
    
    response['headers'] = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': origin
    }
    
    return response

if __name__ == '__main__':
    event = {"body": "{\"url\": \"www.brendonbody.com\", \"https\": true}"}
    print(json.dumps(handler(event, None), indent = 4, sort_keys=True))
