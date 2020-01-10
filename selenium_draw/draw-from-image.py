import sys
import cv2
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

DRIVER_LOCATION = '../chromedriver'
DRAW_WEBSITE = 'https://kleki.com/'
COORDINATES_FILE = 'coordinates.csv'
STARTING_COORDINATES = { 'x': 100, 'y': 100}

file_path = ""
before = {'x':0,'y':0}

def draw():

    # try:
        driver = webdriver.Chrome(DRIVER_LOCATION)
        with open(COORDINATES_FILE) as file:
            driver.get(DRAW_WEBSITE)
            driver.find_element_by_css_selector("html")
            
            # move to starting pointx`
            actions = ActionChains(driver)
            actions.move_by_offset(STARTING_COORDINATES.get('x'), STARTING_COORDINATES.get('y'))
            before = {'x': 0,'y':0}
            # start painting
            for line in map(lambda line: line.rstrip('\n'), file):
                print('Creating move actions')
                xy = line.split(',') # split the x and y
                current = {'x': int(xy[0]), 'y': int(xy[1])} 
                move_to = {'x': current.get('x') - before.get('x'), 
                           'y': current.get('y') - before.get('y')}

                actions.move_by_offset(move_to.get('x'), move_to.get('y'))
                actions.click()
                before = current.copy()

            # finish painting
            actions.perform()

    # except Exception as ex:
    #     print(ex)

def generate_coordenates():
    print('Generating coordinates based on image')
    image=cv2.imread(file_path)
    black_coordinates = [] #initial position

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # find the black pixels
            if image[i,j,0]!=255 and image[i,j,1]!=255 and image[i,j,2]!=255:
                black_coordinates.append((j,i))

    print('Writing coordinates to file')
    # generate a coordinates file
    with open(COORDINATES_FILE, 'a') as out:
        for x, y in black_coordinates:
            out.write(f'{x},{y}\n')
    
    print('Finish generating coordinates file')


if __name__ == "__main__":
    # send the file path as the second arg. The first arg is always the file name
    file_path = sys.argv[1]

    print("Fun script to learn seleniun, python and drag & drop.")   
    start_time = time.time()
    generate_coordenates()
    draw()
    elapsed = int(time.time() - start_time)
    print(f'Completed. Time before completion: { int(elapsed / 60)} minutes.')
