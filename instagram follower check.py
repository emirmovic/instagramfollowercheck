import tkinter
import tkinter as tk
from tkinter import *
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
import time

def goToProfile(driver, usernameInput):
    
    search = driver.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[2]/input')
    search.clear()
    search.send_keys(usernameInput)
    time.sleep(2)
    search.send_keys(Keys.TAB)
    search.send_keys(Keys.ENTER)

    time.sleep(2)
    # followers = driver.find_element_by_xpath('/html/body/span/section/main/div/ul/li[2]/a')
    # followers.click()
    
    

def instagramLogin(usernameInput, passwordInput):
    driver = webdriver.Chrome('/Users/emiribrisimovic/Desktop/instagramfollowercheck/chromedriver')
    # driver = webdriver.Chrome('/Users/Test User/Desktop/chromedriver')
    driver = webdriver.Chrome('/Users/Test User/Documents/GitHub/instagramfollowercheck/chromedriver_windows')
    driver.get('https://www.instagram.com/accounts/login/?hl=en')
    
    time.sleep(1)
    
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys(usernameInput)
    
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(passwordInput)

    password.send_keys(Keys.RETURN)

    time.sleep(2)

    try:
        notnow = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[1]")
        notnow.click()
    except:
        pass

    time.sleep(2)
    
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
