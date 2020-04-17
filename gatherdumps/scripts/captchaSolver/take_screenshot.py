from selenium import webdriver
from PIL import Image
from io import BytesIO

def take_screenshot(driver,element):

    location = element.location
    size = element.size
    
    png = driver.get_screenshot_as_png() # saves screenshot of entire page

    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']


    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png') # saves new cropped image