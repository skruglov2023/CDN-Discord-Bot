import gdown
url='https://docs.google.com/spreadsheets/d/1ciDwVxGTlD7Gf6jnPWBlJl2DYT9WFJioan3xhFJnfVY/export?format=csv'
output = '/home/pi/Desktop/scripts/CDN-Discord-Bot/CDNEvents.txt'
gdown.download(url, output, quiet=False)
