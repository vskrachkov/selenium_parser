import csv
import logging
import string
import sys
import time


from selenium import webdriver

from utils import virtualdisplay, PlatformException


# setup logging
logging.basicConfig(filename='.xing.log', level=logging.INFO,
                    format='%(asctime)s %(message)s')


with virtualdisplay(on=False):
    logging.info('Starting chrome_driver.')
    if sys.platform == 'linux2':
        driver = webdriver.Chrome('drivers/chromedriver_linux')
    elif sys.platform == 'darwin':
        driver = webdriver.Chrome('drivers/chromedriver_mac')
    else:
        raise PlatformException

    logging.info('Getting initial url for searching companies.')
    # companies = ('https://www.xing.com/companies/industries'
    #              '/170000-marketing-pr-and-design?page={}'.format(p)
    #              for p in range(1, 280 + 1))
    companies = ('https://www.xing.com/companies/industries'
                 '/170000-marketing-pr-and-design', )
    for company in companies:
        logging.info('Company: {}'.format(company))
        driver.get(company)
        logging.info('Getting link to company page and go by this link.')
        elements = [elem.get_property('href') for elem
                    in driver.find_elements_by_xpath('//a[@class="company-link"]')]
        elements = list(elements)
        for href in elements:
            logging.info(href)
            driver.get(href)
            logging.info('Go to employees tab.')
            try:
                a = driver.find_element_by_xpath('//li[@id="employees-tab"]/a')
                a.click()
            except Exception as err:
                logging.info(
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
                    logging.info('Writing to result file.')
                    with open('xing_com_result.csv', 'a') as result_file:
                        csw_writer = csv.writer(result_file)
                        for em in employees:
                            if not ('Anonymous' in em.text):
                                cols = em.text.split('\n')
                                csw_writer.writerow(cols)
                except Exception as err:
                    logging.info('{} error when trying to get '
                                 'employee profile info'.format(err))
                    continue
            logging.info('Go to 2 pages back')
            driver.execute_script("window.history.go(-2)")

    logging.info('Closing browser ...')
    driver.close()