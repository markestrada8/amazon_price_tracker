import requests
from bs4 import BeautifulSoup
import smtplib

PRODUCT_URL = 'https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6'
HEADERS = ({'User-Agent':
                'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15.36 (KHTML, like Gecko) Mobile/15E148',
            'Accept-Language': 'en-US, en;q=0.5'})
TARGET_LOW_PRICE = 100.00
sender_email = ""
recipient_email = ""
password = ""

# Amazon will apparently prevent any desktop browser from scraping, so pose as mobile browser
# https://myhttpheader.com/
response = requests.get(PRODUCT_URL, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')
price = soup.select('.priceToPay .a-offscreen')[0].getText()
# pprint(float(int(price.strip("'$"))) < TARGET_LOW_PRICE)
if float(price.strip("'$")) < TARGET_LOW_PRICE:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()

        connection.login(user=sender_email, password=password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=recipient_email,
            msg=f"Your item is now on sale! It has been listed below your target price of ${TARGET_LOW_PRICE} for ${price}"
        )