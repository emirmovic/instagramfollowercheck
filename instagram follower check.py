import tkinter
import tkinter as tk
from tkinter import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
import time

def analyzeFollowers(driver, followers):
    driver.implicitly_wait(2)
    tabthrough = driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
    tabthrough.click()

    actionChain = webdriver.ActionChains(driver)
    actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
    tabthrough.click()

    i = 0
    numberOfFollowersInList = len(tabthrough.find_elements_by_css_selector('li'))
    while (numberOfFollowersInList < 153):
        if i < 4:
            tabthrough.click()
            i += 1
        actionChain.key_down(Keys.SPACE).perform()
        numberOfFollowersInList = len(tabthrough.find_elements_by_css_selector('li'))
        time.sleep(0.25)
    actionChain.key_up(Keys.SPACE).perform()


    ### Put the followers into an array ###
    arrayOfFollowers = []

    for i in range(1, numberOfFollowersInList+1):
        account = driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li[' + str(i) + ']/div/div[1]/div[2]/div[1]/a')
        arrayOfFollowers.append(account.get_attribute("title"))

    pressexit = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div[2]/button')
    pressexit.click()


    ### Scrolls down followers list ###

    driver.implicitly_wait(2)

    following = driver.find_element_by_partial_link_text("following")
    following.click()

    driver.implicitly_wait(2)

    #following
    tabthrough = driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
    tabthrough.click()

    actionChain = webdriver.ActionChains(driver)
    actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
    tabthrough.click()

    n = 0
    numberOfFollowingInList = len(tabthrough.find_elements_by_css_selector('li'))
    while (numberOfFollowingInList < 116):
        if n < 4:
            tabthrough.click()
            n += 1
        actionChain.key_down(Keys.SPACE).perform()
        numberOfFollowingInList = len(tabthrough.find_elements_by_css_selector('li'))
        time.sleep(0.25)
    actionChain.key_up(Keys.SPACE).perform()

    arrayOfFollowing = []

    for i in range(1, numberOfFollowingInList+1):
        account = driver.find_element_by_xpath('//html/body/div[3]/div/div[2]/ul/div/li[' + str(i) + ']/div/div[1]/div[2]/div[1]/a')
        arrayOfFollowing.append(account.get_attribute("title"))

    finalArray = []

    for i in range(len(arrayOfFollowing)):
        if arrayOfFollowing[i] not in arrayOfFollowers:
            finalArray.append(arrayOfFollowing[i])

    print("List of people that don't follow you back: " + str(finalArray))



def goToProfile(driver, usernameInput, seconds):
    driver.implicitly_wait(2)
    search = driver.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[2]/input')
    search.clear()
    search.send_keys(usernameInput)
    time.sleep(seconds)
    search.send_keys(Keys.TAB)
    search.send_keys(Keys.ENTER)


    driver.implicitly_wait(2)
    followers = driver.find_element_by_partial_link_text("followers")
    followers.click()
    analyzeFollowers(driver, followers)


def instagramLogin(usernameInput, passwordInput):
    # driver = webdriver.Chrome('/Users/emiribrisimovic/Desktop/instagramfollowercheck/chromedriver_mac')
    driver = webdriver.Chrome('/Users/Test User/Documents/GitHub/instagramfollowercheck/chromedriver_windows')
    driver.get('https://www.instagram.com/accounts/login/?hl=en')

    driver.implicitly_wait(1)
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys(usernameInput)

    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(passwordInput)

    password.send_keys(Keys.RETURN)

    driver.implicitly_wait(2)
    try:
        notnow = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[1]")
        notnow.click()
    except:
        pass

    try:
        goToProfile(driver, usernameInput, 0.55)
    except:
        goToProfile(driver, usernameInput, 2)


def setVariables():
    usernameInput = entry1.get()
    passwordInput = entry2.get()
    instagramLogin(usernameInput, passwordInput)


master = tkinter.Tk()
master.title("Instagram Input")

entry1 = Entry(master)
entry2 = Entry(master, show="*")

tkinter.Label(master, text = "Username:").grid(row = 0)
entry1.grid(row = 0, column = 1)

tkinter.Label(master, text = "Password:").grid(row = 1)
entry2.grid(row = 1, column = 1)

button = Button(master, text="Submit", fg="red", command=setVariables)
button.grid(row=3,column=1)

master.mainloop()
