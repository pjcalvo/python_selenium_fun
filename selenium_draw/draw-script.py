import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

DRIVER_LOCATION = '../chromedriver'
DRAW_WEBSITE = 'https://kleki.com/'

file_path = ""

def draw():

    with open(file_path) as file:
        driver.get(DRAW_WEBSITE)
        driver.find_element_by_css_selector("html")
        
        actions = ActionChains(driver)
        lines = [line.rstrip('\n') for line in file.readlines()]

        # start painting
        for line in file.readlines():
            if line == "release":
                actions.release()
            else:
                xy = line.split(',')
                print(f'Move to coordinates: {xy}')
                actions.move_by_offset(xy[0],xy[1])
                actions.click_and_hold()
            
        # finish painting
        actions.perform()


if __name__ == "__main__":
    # send the file path as the second arg. The first arg is always the file name
    file_path = sys.argv[1]
    print("Fun script to learn seleniun, python and drag & drop.")
    
    driver = webdriver.Chrome(DRIVER_LOCATION)
    try:
        draw()
    except Exception as e:
        print(e)
    finally:
        driver.close()
