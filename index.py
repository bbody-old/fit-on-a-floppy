import json
from Website import Website

origin = "http://fitonafloppy.website"

def handler(event, context):
    url = json.loads(event['body'])['url']

    print("Processing " + url)

    website = Website(url)
    response = website.getWebsiteContent()
    
    response['headers'] = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': origin
    }
    
    return response

if __name__ == '__main__':
    event = {"body": "{\"url\": \"http://wwww.fitonafloppy.website\"}"}
    print(json.dumps(handler(event, None), indent = 4, sort_keys=True))
