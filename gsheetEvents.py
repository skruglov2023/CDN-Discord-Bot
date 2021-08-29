import gdown

url = 'https://docs.google.com/spreadsheets/d/1ciDwVxGTlD7Gf6jnPWBlJl2DYT9WFJioan3xhFJnfVY/export?format=csv'
output = 'CDNEvents.txt'
gdown.download(url, output, quiet=False)
