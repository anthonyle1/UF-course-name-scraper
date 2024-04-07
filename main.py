"""
###########################################
##   WEB SCRAPER FOR UF CLASSES NAMES    ##
###########################################
   * pulls class names from the University of Florida's Class Search based upon a user-given course-code
   * developed by: https://github.com/anthonyle1
"""

# FIXME: also consider cleaning up the course code so it is always in the format CODE# instead of code # or code# etc.
# FIXME: (essentially removing the spaces and capitalizing everything)

from selenium import webdriver
from bs4 import BeautifulSoup
import time

def findCourseNames(course_code, term):
    # loading the website html
    my_url = f'https://one.uf.edu/soc/?category=%22CWSP%22&term=%22{term}%22&course-code=%22{course_code}%22'
    driver = webdriver.Chrome()
    driver.get(my_url)
    time.sleep(2) # allows data to be fully web-scraped by selenium, increase value for more time.
                  # in a app-development setting, this would be good to have a loading screen
    source = driver.page_source
    webhtml = BeautifulSoup(source, 'html.parser')
    webhtml = webhtml.find_all("p")  # class-names are all found under </p> in webhtml

    course_code_found = []

    # finds where class-names are found in html code
    for p in webhtml:
        if course_code.upper() in p.getText(): # .getText() converts the html to a string
            course_code_found.append(p.getText())

    course_names = []
    for a in course_code_found:
        startIndex = a.find("-") + 2
        course_names.append(a[startIndex:])
    return course_names

 # display function
def displayCourseNames(course_names):
    for course in course_names:
        print(course)

def main():
    course_code = "IDS2935"
    term = "2245"
    course_names = findCourseNames(course_code, term)
    displayCourseNames(course_names)

main()

"""
####################
## guide to terms ##
####################
terms : 2 + year (last 2 digits) + month started

month started guide:---------------*
* 8 - fall     | * 56W1 - summer a |
* 1 - spring   | * 56W2 - summer b |
* 56 - summer  | * 561 -> summer c |
-----------------------------------*
examples:
* 2248 -> fall 24
* 22456 -> summer 24
* 22456W1 -> summer A 24
* 22456W2 -> summer B 24
* 224561 -> summer C 24
* 22451 -> spring 24
* 2238 -> fall 23

##################
##  resources:  ##
##################
* https://stackoverflow.com/questions/74349320/not-getting-complete-data-using-selenium 
"""