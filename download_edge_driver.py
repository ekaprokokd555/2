from selenium import webdriver
from webdriver_manager.microsoft import EdgeDriverManager

# Automatically download and use the correct Edge WebDriver
driver = webdriver.Edge(EdgeDriverManager().install())

# Open a website (for example, Google)
driver.get("https://www.google.com")

# Print the page title
print(driver.title)

# Close the browser
driver.quit()
