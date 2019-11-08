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
        self.favicon = False
        self.title = ''
    def parseWebsite(self):
        print(self.url)
        page = requests.get(self.url, stream=True)
        content = BeautifulSoup(page.content, 'html.parser')

        self.html_sizes = Website.calculate_file_size(page)

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
        return self.html_sizes['bytes'] + self.css_files['total_size_bytes'] + self.js_files['total_size_bytes'] + self.image_files['total_size_bytes']
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
                'html_size_bytes': self.html_sizes['bytes'],
                'html_size_kibibytes': self.html_sizes['kibibytes'],
                'html_size_kilobytes': self.html_sizes['kilobytes'],
                'url': self.url,
                'friendly_url': self.friendly_url,
                'total_size_bytes': totalSize,
                'total_size_kibibytes': totalSize/Website.BYTES_PER_KIB,
                'total_size_kilobytes': totalSize/Website.BYTES_PER_KB,
                'floppy_size_bytes': Website.FLOPPY_SIZE,
                'floppy_size_kibibytes': Website.FLOPPY_SIZE/Website.BYTES_PER_KIB,
                'floppy_size_kilobytes': Website.FLOPPY_SIZE/Website.BYTES_PER_KB,
                'floppies': math.ceil(totalSize/Website.FLOPPY_SIZE)
            }
            
            return {
                'statusCode': str(200),
                'body': json.dumps(data),
            }
        except Exception as e:
            print(e)
            return {
                'statusCode': str(400),
                'body': {
                    'error': 'Error in processing website'
                },
            }
    # Static values and functions
    FLOPPY_SIZE = 1474560.0
    BYTES_PER_KIB = 1024.0
    BYTES_PER_KB = 1000.0
    @staticmethod
    def calculate_file_size(file_request):
        with file_request as response:
            size = sum(len(chunk) for chunk in response.iter_content(8))

        return {
            'bytes': size,
            'kibibytes': size/Website.BYTES_PER_KIB,
            'kilobytes': size/Website.BYTES_PER_KB
        }
    @staticmethod
    def get_total_size(files):
        totalSize = 0
        for f in files:
            totalSize += f['bytes']
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

            file_sizes = Website.calculate_file_size(asset_file)

            parsed_files.append({
                'file_path': full_filename,
                'filename': filename,
                'bytes': file_sizes['bytes'],
                'kibibytes': file_sizes['kibibytes'],
                'kilobytes': file_sizes['kilobytes'],
            })
        total_size = Website.get_total_size(parsed_files)
        return {
            'files': parsed_files,
            'title': title,
            'total_size_bytes': total_size,
            'total_size_kibibytes': total_size / Website.BYTES_PER_KIB,
            'total_size_kilobytes': total_size / Website.BYTES_PER_KB
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