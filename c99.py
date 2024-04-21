import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import sys
from colorama import Fore,init
init()

def c99_nl():
    try:
        target = sys.argv[1]
        today = datetime.now()
        for i in range(0,10):
            mines_days = timedelta(days=i)
            now = today - mines_days
            formatted_date = now.strftime("%Y-%m-%d")
            url = f"https://subdomainfinder.c99.nl/scans/{formatted_date}/{target}"

            response = requests.get("https://subdomainfinder.c99.nl/")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                hidden_inputs = soup.find_all('input', type='hidden')
                
                data = {}
                for hidden_input in hidden_inputs:
                    data[hidden_input['name']] = hidden_input['value']
                
                data['jn'] = 'JS aan'
                data['T'] = 'aangeroepen'
                data['CSRF'] = 'aangepast'
                data['domain'] = target
                data['scan_subdomains'] = ''

                post_response = requests.post(url, data=data)
                
                if post_response.status_code == 200:
                    soup = BeautifulSoup(post_response.text, 'html.parser')
                    subdomain_links = re.findall(r'(?:\b\w+(?:[-.]\w+)*\.\w+\b)', soup.text)
                    checker = subdomain_links.count(target)
                    if checker > 0:
                        for link in subdomain_links:
                            if "." + target in link:
                                link = link.strip()
                                print(link)
                    else:
                        pass
                else:
                    print("Failed to retrieve subdomains")
            else:
                print("Failed to retrieve the webpage")
    except Exception as e:
        print(Fore.RED + "c99_nl encountered with error:", e)


c99_nl()
