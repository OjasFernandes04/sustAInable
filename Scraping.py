from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PIL import Image
import os, time
from selenium.webdriver.support.ui import WebDriverWait
import threading
from selenium.webdriver.common.by import By
import config
from selenium.webdriver.support import expected_conditions as EC

class Scraping:
    def __init__(self):
        self.driver = None
        self.wait = None

    def openWebDriver(self):
        """Manually sets up Chrome WebDriver with error handling."""
        try:
            chromeOptions = Options()
            chromeOptions.add_argument("--log-level=3")
            chromeOptions.add_argument("--disable-notifications")
            # chromeOptions.add_argument('--headless')  # Uncomment for headless mode
            chromeOptions.add_extension("ublock_origin.crx")

            # Manually specify ChromeDriver path
            chrome_driver_path = "/Users/anubhavdixit/Desktop/Investopedia-Bot-master/chromedriver"

            # Initialize WebDriver
            self.driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chromeOptions)
            self.wait = WebDriverWait(self.driver, 10)

            print("[INFO] Chrome WebDriver started successfully.")

        except Exception as e:
            print(f"[ERROR] Failed to start WebDriver: {e}")

    def getFinviz(self, ticker):
        """Loads stock data from Finviz."""
        if self.driver:
            self.driver.get(f"https://finviz.com/quote.ashx?t={ticker}")

    def takeScreenshot(self):
        """Takes a screenshot of the current stock page."""
        if self.driver:
            self.driver.get_screenshot_as_file("currentStock.png")
            self.image = Image.open("currentStock.png")

    def cropImage(self):
        """Crops the screenshot to focus on relevant stock data."""
        area = (20, 290, 1250, 800)
        croppedImage = self.image.crop(area)
        os.remove("currentStock.png")
        croppedImage.save("currentStock.png")
        self.image = Image.open("currentStock.png")

    def resizeImage(self):
        """Resizes the cropped image for better visualization."""
        newHeight = 300
        newWidth = int(newHeight / self.image.height * self.image.width)
        resizedImage = self.image.resize((newWidth, newHeight))
        os.remove("currentStock.png")
        resizedImage.save("currentStock.png")
        self.image.close()

    def quitDriver(self):
        """Safely closes the WebDriver session."""
        if self.driver:
            self.driver.quit()
            print("[INFO] WebDriver closed.")

    def login(self):
        """Logs into Investopedia with credentials from config.py."""
        if self.driver:
            self.driver.get("https://www.investopedia.com/simulator/home.aspx")
            try:
                self.wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config.INVESTOPEDIA_EMAIL)
                self.wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config.INVESTOPEDIA_PASSW)
                self.driver.find_element(By.ID, "login").click()
                print("[INFO] Logged in successfully.")
            except Exception as e:
                print(f"[ERROR] Login failed: {e}")

    def getTradePage(self):
        """Navigates to the trading page."""
        if self.driver:
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/main/div/div[2]/div/a[2]/span'))).click()
            except Exception as e:
                print(f"[ERROR] Failed to open trade page: {e}")

    def scrapeAccCash(self):
        """Retrieves account value and cash balance."""
        if self.driver:
            try:
                account = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-cy="account-value"]'))).text
                cash = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-cy="cash"]'))).text
                account = account.replace("$", "").replace(",", "")
                cash = cash.replace("$", "").replace(",", "")
                return float(account), float(cash)
            except Exception as e:
                print(f"[ERROR] Failed to scrape account balance: {e}")
                return None, None

    def setStock(self, ticker):
        """Searches for a stock symbol in the trading page."""
        if self.driver:
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Look up Symbol/Company Name"]'))).send_keys(ticker)
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-cy="symbol-description"]'))).click()
            except Exception as e:
                print(f"[ERROR] Failed to set stock ticker: {e}")

    def executeOrder(self, ticker, transaction, quantity, orderType, limitPrice, sendEmail=True):
        """Executes a trade order on Investopedia."""
        self.openWebDriver()
        self.login()
        self.getTradePage()
        self.setStock(ticker)

        try:
            self.removePopup()
        except:
            pass

        if transaction != "Buy":
            self.setTransaction(transaction)

        maxQuantity = self.getMaxQuantity()
        if maxQuantity < quantity:
            quantity = maxQuantity

        self.setQuantity(quantity)

        if orderType != "Market":
            self.setOrderType(orderType, limitPrice)

        self.preview()
        self.submit()
        print(f"[INFO] Order executed: {transaction} {quantity} shares of {ticker}.")

    def removePopup(self):
        """Closes popups if they appear."""
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@style="color: rgb(255, 255, 255);"]'))).click()
        except:
            pass

    def preview(self):
        """Clicks the Preview Order button."""
        if self.driver:
            try:
                self.driver.find_element(By.XPATH, '(//span[@class="v-btn__content"])[9]').click()
            except Exception as e:
                print(f"[ERROR] Failed to preview order: {e}")

    def submit(self):
        """Submits the trade order."""
        if self.driver:
            time.sleep(2)
            try:
                self.driver.find_element(By.XPATH, '(//span[@class="v-btn__content"])[11]').click()
                print("[INFO] Order submitted successfully.")
            except Exception as e:
                print(f"[ERROR] Failed to submit order: {e}")
