import requests
from lxml import etree
import re

def get_domain_info(domain: str) -> dict:
    try:
        res = requests.get(url=f"https://{domain}", stream=True, allow_redirects=True, timeout=5)
        try:
            res.raise_for_status()
            ip, port = res.raw._connection.sock.getpeername()
            return {
                    'msg': f'Website is accesible.\nIP: {ip}', 
                    'status': True,
                    'html': res.text
            }
        except Exception:
            return {
                    'msg': 'Failed to access', 
                    'status': False
            }
    except Exception:
        return {
            'msg': f'Not connect to {domain}', 
            'status': False
        }
    

def parse_phone_number(html: str) -> str:
    try:
        dom = etree.HTML(str(html))
        return dom.xpath('//*[@id="top"]/div[1]/div[1]/div/div/div[2]/div[1]/a')[0].text.replace(' ', '')
    except:
        return None


def validate_phone_number(phone_number: str) :
    pattern = r'^(\+\d{1,3})?(\(\d{1,}\))?(\d{1,})-\d{1,}-\d{1,}$'

    match = re.match(pattern, phone_number)
    if match:
        print(f"Phone number {phone_number} is valid.")
    else:
        print(f"Phone number {phone_number} is not valid.")
    

if __name__ == '__main__':
    result = get_domain_info('sstmk.ru')
    print(result["msg"])
    if result['status']:
        number = parse_phone_number(result['html'])
        if number:
            print(f'Company number: {number}')
            validate_phone_number(number)
        else:
            print('Phone number not found')

