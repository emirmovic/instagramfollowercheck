import tkinter
import tkinter as tk
from tkinter import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
import time

def analyzeFollowers(driver, followers):
    time.sleep(1)
    tabthrough = driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
    tabthrough.click()

    actionChain = webdriver.ActionChains(driver)
    actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
    tabthrough.click()

    numberOfFollowersInList = len(tabthrough.find_elements_by_css_selector('li'))
    while (numberOfFollowersInList < 153):
        tabthrough.click()
        actionChain.key_down(Keys.SPACE).perform()
        numberOfFollowersInList = len(tabthrough.find_elements_by_css_selector('li'))
        # print(numberOfFollowersInList)
        time.sleep(0.2)
    actionChain.key_up(Keys.SPACE).perform()
        
    
def goToProfile(driver, usernameInput):
    
    search = driver.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[2]/input')
    search.clear()
    search.send_keys(usernameInput)
    # time.sleep(2)
    search.send_keys(Keys.TAB)
    search.send_keys(Keys.ENTER)

    # time.sleep(2)
    # followers = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')
    followers = driver.find_element_by_partial_link_text("followers")
    followers.click()
    analyzeFollowers(driver, followers)
    

def instagramLogin(usernameInput, passwordInput):
    # driver = webdriver.Chrome('/Users/emiribrisimovic/Desktop/instagramfollowercheck/chromedriver_mac')
    driver = webdriver.Chrome('/Users/Test User/Documents/GitHub/instagramfollowercheck/chromedriver_windows')
    driver.get('https://www.instagram.com/accounts/login/?hl=en')
    
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys(usernameInput)
    
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(passwordInput)

    password.send_keys(Keys.RETURN)

    try:
        notnow = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[1]")
        notnow.click()
    except:
        pass

    # time.sleep(2)
    
    goToProfile(driver, usernameInput)
    

def setVariables():
    usernameInput = entry1.get()
    passwordInput = entry2.get()
    instagramLogin(usernameInput, passwordInput)    
    
master = tkinter.Tk()
master.title("Instagram Input")

entry1 = Entry(master)
entry2 = Entry(master, show="*")


tkinter.Label(master, text = "Username:").grid(row = 0) # this is placed in 0 0
entry1.grid(row = 0, column = 1)

tkinter.Label(master, text = "Password:").grid(row = 1)
entry2.grid(row = 1, column = 1)


    


# 'Entry' is used to display the input-field

button = Button(master, text="Submit", fg="red", command=setVariables)
button.grid(row=3,column=1)

master.mainloop()
