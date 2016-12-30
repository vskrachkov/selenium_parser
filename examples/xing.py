import csv
import time
import string
import logging

from selenium import webdriver
# from pyvirtualdisplay import Display


# setup logging
logging.basicConfig(filename='xing.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

logging.info('Creating result file.')
result_file = open('result.csv', 'w')
csw_writer = csv.writer(result_file)

logging.info('Starting virtual display.')
# display = Display(visible=0, size=(800, 600))
# display.start()

logging.info('Starting chrome_driver.')
driver = webdriver.Chrome('../drivers/chromedriver')

logging.info('Getting initial url for searching companies.')
companies = ('https://www.xing.com/companies/industries' \
             '/170000-marketing-pr-and-design?page={}'.format(p)
             for p in range(1, 280 + 1))

for company in companies:
    logging.info(company)
    driver.get(company)
    logging.info('Getting link to company page and go by this link.')
    elements = (elem.get_property('href') for elem
                in driver.find_elements_by_xpath('//a[@class="company-link"]'))
    for href in elements:
        print(href)
        print( '=' * 20)
        try:
            driver.get(href)
            logging.info('Go to employees tab.')
        except:
            print( 'except here !!!')
        try:
            a = driver.find_element_by_xpath('//li[@id="employees-tab"]/a')
            a.click()
        except Exception as err:
            logging.warning(
                '{} error when trying to get employees tab.'.format(err))
        logging.info('Getting all employees of company')
        time.sleep(.5)
        for l in string.ascii_uppercase:
            try:
                letter = driver.find_element_by_xpath(
                    '//*[text()="{}"]'.format(l))
                letter.click()
                time.sleep(.5)
                employees = driver.find_elements_by_xpath(
                    '//ul[@class="user-card-information"]')
                for em in employees:
                    if not ('Anonymous' in em.text):
                        cols = em.text.split('\n')

                        csw_writer.writerow(cols)
            except Exception as err:
                logging.warning(
                    '{} error when trying to get employee profile info'.format(err))
                continue
        driver.execute_script("window.history.go(-2)")

logging.info('Closing browser ...')
driver.close()
logging.info('Stopping display ...')
# display.stop()
