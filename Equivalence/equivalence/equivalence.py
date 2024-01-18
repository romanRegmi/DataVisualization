from selenium import webdriver
import time
import json
from selenium.webdriver.common.by import By

import equivalence.constants as const

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Equivalence:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome()
        except Exception as e:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
        
        self.words_to_check = ["health", "safety"]

    def land_first_page(self):
        self.driver.get(const.BASE_URL)
        try:
            element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.close[data-dismiss='modal'][aria-label='Close']")))
        except Exception as e:
            print("The element cannot be found")
        if(element):
            element.click()

    def login(self):
        self.driver.find_element(By.ID, "email").send_keys(const.EMAIL)
        self.driver.find_element(By.ID, "password").send_keys(const.PWD)
        time.sleep(30)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
    def apply(self):
        apply_button = self.driver.find_element(By.XPATH, "//a[@class='btn btn-success']")
        apply_button.click()

    def contains_keyword(self, sentence):
        lower_sentence = sentence.lower()

        for word in self.words_to_check:
            if word.lower() in lower_sentence:
                return True

        return False

    def selectUni(self):
        uni = Select(self.driver.find_element(By.ID, "university_id"))
        options_uni = [option.text for option in uni.options]


        # Initialize an empty dictionary to store the results
        result_dict = {}
        counter = 0
        # Loop through each option in dropdown A
        for option_a in options_uni:
            counter = counter + 1
            # Select an option in dropdown A
            uni.select_by_visible_text(option_a)
            
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "degree_title")))
            degree = Select(self.driver.find_element(By.ID, "degree_title"))
            time.sleep(3)
            # Get all options in dropdown B for the selected option in A
            options_b = []
            try:
                for option in degree.options:
                    if(self.contains_keyword(option.text)):
                        options_b.append(option.text)
            except Exception as e:
                print(f"Error: Error occured {e}")

            time.sleep(3)
            # Store the options in a dictionary with dropdown A option as key
            if(options_b):
                result_dict[option_a] = options_b
            print(counter)

        

        with open('result_data.json', 'w') as json_file:
            json.dump(result_dict, json_file)
        
        print("Data saved as 'result_data.json'")
