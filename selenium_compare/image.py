from PIL import Image, ImageDraw
from selenium import webdriver
import os
import sys

DRIVER_LOCATION = '../chromedriver'

class VisualValidation:

    RESOLUTION = {'x':1024, 'y':768}
    STAGING_URL = 'https://www.google.com/?q=hola'
    TEST_NAME = 'google_test'
    SCREENSHOTS_DIR = 'screenshots'
    BASE_DIR = 'base'
    DIFFERENCE_DIR = 'difference'
    RECENT_DIR = 'recent'

    driver = None
    new_test = False
    file_name = ''
    screenshot_dir = ''
    base_dir = ''
    difference_dir = ''
    recent_dir = ''


    def __init__(self):
        self.setup_folders()
        self.set_up()
        self.capture_screens()
        self.analyze()
        self.clean_up()


    def setup_folders(self):
        self.screenshots_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.SCREENSHOTS_DIR)
        self.base_dir = os.path.join(self.screenshots_dir,self.BASE_DIR)
        self.difference_dir = os.path.join(self.screenshots_dir,self.DIFFERENCE_DIR)
        self.recent_dir = os.path.join(self.screenshots_dir,self.RECENT_DIR)

        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)    
        if not os.path.exists(self.difference_dir):
            os.makedirs(self.difference_dir)    
        if not os.path.exists(self.recent_dir):
            os.makedirs(self.recent_dir)    

    def set_up(self):
        self.driver = webdriver.Chrome(DRIVER_LOCATION)

    def clean_up(self):
        self.driver.close()

    def capture_screens(self):
        self.file_name = f'{ self.TEST_NAME }_{self.RESOLUTION.get("x")}x{self.RESOLUTION.get("y")}.png'
        self.screenshot(self.STAGING_URL, self.file_name)

    def screenshot(self, url, file_name):
        print (f"** Capturing {url} screenshot as {file_name} ...")
        self.driver.get(url) # navigate to test URL
        self.driver.set_window_size(self.RESOLUTION.get('x'),self.RESOLUTION.get('y')) # set desired resolution

        # check if baseline exist
        if not os.path.isfile(os.path.join(self.base_dir , file_name)):
            print('*** NO baseline image was found ...')
            self.new_test = True
            self.driver.save_screenshot(os.path.join(self.base_dir , file_name))       
            print('*** Baseline was recorded. Test will not be executed ...')
        else:
            print('*** Baseline image was found ...')
            self.driver.save_screenshot(os.path.join(self.recent_dir , file_name))
            print('*** New screen capture recorded ...')
        
        self.driver.get_screenshot_as_png()

        print (f"** Finish image capturing ...")

    def analyze(self):

        file_name = self.file_name

        if not self.new_test:
            print('** Executing test.')
            screenshot_base = Image.open(os.path.join(self.base_dir , file_name))
            screenshot_test = Image.open(os.path.join(self.recent_dir , file_name))
            columns = 60
            rows = 80
            test_failed = False
            screen_width, screen_height = screenshot_test.size

            block_width = ((screen_width - 1) // columns) + 1 # this is just a division ceiling
            block_height = ((screen_height - 1) // rows) + 1

            for y in range(0, screen_height, block_height+1):
                for x in range(0, screen_width, block_width+1):
                    region_test = self.process_region(screenshot_test, x, y, block_width, block_height)
                    region_base = self.process_region(screenshot_base, x, y, block_width, block_height)

                    if region_base is not None and region_test is not None and region_base != region_test:
                        test_failed = True
                        draw = ImageDraw.Draw(screenshot_test)
                        draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")

            if test_failed:
                print('*** There are visual differences. Saving results to /difference.')
                screenshot_test.save(os.path.join( self.difference_dir , file_name))
            else:
                print('*** No visual differences.')

    def process_region(self, image, x, y, width, height):
        region_total = 0

        # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
        factor = 100

        for coordinateY in range(y, y+height):
            for coordinateX in range(x, x+width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel)/4
                except:
                    return

        return region_total/factor

if __name__ == "__main__":
    print('******************************************')
    print('***** Starting visual test execution *****')
    VisualValidation()
    print('****** Finished visual test execution ****')
    print('******************************************')