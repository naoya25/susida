from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
from PIL import Image
import pytesseract
from time import sleep

SUSIDA_URL = "https://sushida.net/"


def main(course, mode):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(SUSIDA_URL)
    sleep(5)

    if mode == 0:
        driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/a[2]/img').click()
    else:
        driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/a[1]/img').click()
    sleep(5)

    canvas_element = driver.find_element(By.XPATH, '//*[@id="#canvas"]')
    window_position = driver.get_window_position()
    element_location = canvas_element.location
    element_size = canvas_element.size
    x = window_position["x"] + element_location["x"] + element_size["width"] / 2
    y = window_position["y"] + element_location["y"] + element_size["height"] / 2 + 170

    pyautogui.moveTo(x, y)
    pyautogui.click()
    sleep(1)

    if course == 0:
        y -= 50
    elif course == 2:
        y += 60
    pyautogui.moveTo(x, y)
    pyautogui.click()
    sleep(3)

    # ゲーム開始
    pyautogui.press("space")
    sleep(3)
    while True:
        canvas_element = driver.find_element(By.XPATH, '//*[@id="#canvas"]')
        canvas_element.screenshot("./images/game-img.png")
        sleep(1)
        img = Image.open("./images/game-img.png")
        img = img.crop((50, 230, 450, 270))
        img.save("./images/game-img.png")
        ocr_text = pytesseract.image_to_string(img, lang="eng")

        if ocr_text.strip() == "":
            continue
        text = max(ocr_text.split(), key=len)
        print(text)
        pyautogui.write(text)
        sleep(1)

    driver.quit()


if __name__ == "__main__":
    course = int(input("コースを選択してください\n0:お手軽\n1:お勧め\n2:高級\n>>> "))
    mode = int(input("モードを選択してください\n0:無音モード\n1:通常モード\n>>> "))

    main(course, mode)
