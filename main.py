import cv2
from google.cloud import vision_v1
from utils.text_extraction_utils import get_converted_image, get_annotations, get_votes
import google.auth
from utils.file_utils import find_files
import os
from tqdm import tqdm
credentials, project = google.auth.default()
vision_client = vision_v1.ImageAnnotatorClient(credentials=credentials)


if __name__ == "__main__":

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import Select

    # Set path to your Chrome driver executable
    webdriver_service = Service('/Users/samettaspinar/Documents/chromedriver_mac_arm64')

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=webdriver_service)

    # Navigate to the webpage
    url = 'https://tutanak.oyveotesi.org/'
    driver.get(url)

    # Wait for the dropdown menu to be present
    wait = WebDriverWait(driver, 5)
    dropdown_menu = wait.until(
        EC.presence_of_element_located((By.XPATH, "//label[text()='İl']/following-sibling::div//input")))

    # Click on the dropdown menu to expand it
    dropdown_menu.click()
    response_elements = driver.find_elements(By.CLASS_NAME, "v-list-item-title")

    for element in response_elements:
        if element.text == "ADANA":
            desired_option = element
            desired_option.click()

            desired_option_text = "CEYHAN"

            # Find the dropdown menu element
            dropdown_menu_ilce = driver.find_element(By.XPATH, "//label[text()='İlçe']/following-sibling::div//input")

            # Find all the option elements within the dropdown menu
            option_elements_ilce = driver.find_element(By.CLASS_NAME,
                "v-list-item-title")

            # Iterate through the option elements to find the desired option
            desired_option_ilce = None
            for element_ilce in option_elements_ilce:
                if element_ilce.text == desired_option_text:
                    desired_option_ilce = element_ilce
                    break

            # Click on the desired option
            desired_option.click()

            break

    # Quit the driver
    driver.quit()

    fold = "/users/samettaspinar/desktop/islak_imza/"
    input_fold = os.path.join(fold, "input")
    output_fold = os.path.join(fold, "output")

    image_names = find_files(input_fold)

    pbar = tqdm(image_names)
    for name in pbar:
        pbar.set_description(f"{name}")

        image_uri = os.path.join(input_fold, name)
        im_arr, annotations = get_annotations(vision_client, image_uri)
        res = get_votes(annotations)
        converted_image = get_converted_image(im_arr, annotations)
        cv2.imwrite(f"{output_fold}/{name}.png", converted_image)
