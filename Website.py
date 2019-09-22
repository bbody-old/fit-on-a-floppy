from bs4 import BeautifulSoup
import requests
import json
import urllib.parse
import math

class Website:
    def __init__(self, url):
        self.url = Website.parseURL(url)
        self.friendly_url = Website.parseFriendlyURL(url)
        self.js_files = []
        self.css_files = []
        self.image_files = []
        self.html_size = 0
        self.favicon = False
        self.title = ''
    def parseWebsite(self):
        page = requests.get(self.url, stream=True)
        content = BeautifulSoup(page.content, 'html.parser')
        self.html_size = int(Website.calculate_file_size(page))

        self.setTitle(content)
        self.setFavicon(content)
        self.setJSFiles(content)
        self.setCSSFiles(content)
        self.setImageFiles(content)
    def setTitle(self, content):
        meta_title = content.select('meta[itemprop="name"]')

        if (len(meta_title) == 0):
            title = content.title.string
        else:
            title = meta_title[0]['content']
        
        self.title = title
    def setFavicon(self, content):
        favicon_selector = content.select('link[rel="shortcut icon"]')
        
        if (len(favicon_selector) > 0):
            favicon = favicon_selector[0]['href']
        else:
            favicon = False
        self.favicon = favicon
    def setJSFiles(self, content):
        js_files = content.select('script[src]:not([async])')
        self.js_files = Website.parse_files('Scripts', self.url, js_files, 'src')
    def setCSSFiles(self, content):
        css_files = content.select('link[rel="stylesheet"]')
        self.css_files = Website.parse_files('Styles and Fonts', self.url, css_files, 'href')
    def setImageFiles(self, content):
        image_query = content.select('img')
        image_files = []

        for image in image_query:
            if (not image['src'].startswith('data:')):
                image_files.append(image)

        self.image_files = Website.parse_files('Images', self.url, image_files, 'src')
    def getTotalSize(self):
        return self.html_size + self.css_files['total_size'] + self.js_files['total_size'] + self.image_files['total_size']
    def getWebsiteContent(self):
        try:
            self.parseWebsite()
            totalSize = self.getTotalSize()

            data = {
                'title': self.title,
                'favicon': self.favicon,
                'js_files': self.js_files,
                'css_files': self.css_files,
                'image_files': self.image_files,
                'html_size': self.html_size,
                'url': self.url,
                'friendly_url': self.friendly_url,
                'total_size': totalSize,
                'floppy_size': Website.FLOPPY_SIZE,
                'floppies': math.ceil(totalSize/Website.FLOPPY_SIZE)
            }
            
            return {
                'statusCode': str(200),
                'body': json.dumps(data),
            }
        except:
            return {
                'statusCode': str(400),
                'body': {
                    'error': 'Error in processing website'
                },
            }
    # Static values and functions
    FLOPPY_SIZE = 1423.5*1024
    @staticmethod
    def calculate_file_size(file_request):
        with file_request as response:
            size = sum(len(chunk) for chunk in response.iter_content(8196))
        return size
    @staticmethod
    def get_total_size(files):
        totalSize = 0
        for f in files:
            totalSize += f['file_size']
        return totalSize
    @staticmethod
    def parse_files(title, url, files, attribute):
        parsed_files = []
        for f in files:
            file_name_components = f[attribute].split('/')
            filename = file_name_components[len(file_name_components) - 1]
            full_filename = f[attribute]

            if (('https://' not in full_filename) and ('http://' not in full_filename)):
                full_filename = urllib.parse.urljoin(url, full_filename)
            
            asset_file = requests.get(full_filename, stream=True)

            file_size = Website.calculate_file_size(asset_file)

            parsed_files.append({
                'file_path': full_filename,
                'filename': filename,
                'file_size': int(file_size)
            })
        return {
            'files': parsed_files,
            'title': title,
            'total_size': Website.get_total_size(parsed_files)
        }
    @staticmethod
    def parseFriendlyURL(url):
        url = url.replace('https://', '')
        url = url.replace('http://', '')
        return url
    @staticmethod
    def parseURL(url):
        if (('https://' not in url) and ('http://' not in url)):
            return 'https://' + url
        return url