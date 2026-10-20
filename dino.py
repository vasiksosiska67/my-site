import webbrowser
import time
import sys

print("Приготовьтесь!")


for i in range(3, 0, -1):
    sys.stdout.write(f"\rИгра откроется через: {i}...")
    sys.stdout.flush() 
    time.sleep(1)      # Ждем ровно 1 секунду

print("\n\nБум! Запуск!")

# сайт с Динозавриком
webbrowser.open("https://dino-chrome.com")

