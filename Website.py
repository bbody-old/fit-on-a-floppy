from bs4 import BeautifulSoup
import requests
import json
import urllib.parse
import math

class Website:
    FLOPPY_SIZE = 1423.5*1024
    def __init__(self, url, protocol):
        self.url = protocol + "://" + url
        self.friendly_url = url
        self.js_files = []
        self.css_files = []
        self.image_files = []
    
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
    @staticmethod
    def calculate_file_size(file_request):
        with file_request as response:
            size = sum(len(chunk) for chunk in response.iter_content(8196))
        return size
        # if ('Content-length' in file_request.headers.keys()):
        #     return file_request.headers['Content-length']
        # else:
        #     return len(file_request.content) * 8
    @staticmethod
    def getTotalSize(files):
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
            'total_size': Website.getTotalSize(parsed_files)
        }

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
    def getWebsiteContent(self):
        self.parseWebsite()
        totalSize = self.html_size + self.css_files['total_size'] + self.js_files['total_size'] + self.image_files['total_size']
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
            'body': data,
        }
    
