import json
from Website import Website

origin = "*"

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
    event = {"body": "{\"url\": \"https://wwww.bonds.com.au\"}"}
    # print(json.dumps(, indent = 4, sort_keys=True))
    handler(event, None)
