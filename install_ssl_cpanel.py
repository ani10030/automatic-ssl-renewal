from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import time
import sys
from datetime import timedelta
import datetime
import ssl,socket

def open_browser():
	try:
		driver = webdriver.PhantomJS(executable_path='/path/to/phantomjs')
		return driver
	except:
		return 'ERROR'

def get_SSL_expiry():
	try:
		hostname = 'example.com'
		context = ssl.create_default_context()
		conn = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=hostname)
		conn.connect((hostname, 443))

		ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
		ssl_info = conn.getpeercert()
		expiry = datetime.datetime.strptime(ssl_info['notAfter'],ssl_date_fmt)
		ssl_expiry_date = expiry.strftime('%m-%d-%Y')

		return ssl_expiry_date
	except Exception,e:
		print '[X]- Error Occured while obtaining SSL expiry date -[X]'
		print 'Error : '+str(e)
		return False


def verify_installation(old_expiry_date,new_expiry_date):
	try:
		print '-- Verifying Certificate Installation --'
		print '\n\n\n'
		print '----------------------------------------------------------'
		print 'Previous Expiry Date	:	'+old_expiry_date
		print 'Current Expiry Date	:	'+new_expiry_date
		print '----------------------------------------------------------'
		print '\n\n\n'

		if old_expiry_date != new_expiry_date:
			return True
		else:
			print '[X]- New Expiry Date is same as Old Expiry Date -[X]'
			return False
	except:
		print '[X]- Error Occured while Verifying the installed Certificate -[X]'
		return False

def main():
	try:
		print '** Start Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
		print '------- Program Started -------'
		print 'Opening Browser ...'

		count = 1
		print '-- Attempt 1 to open webdriver --'
		driver = open_browser()
		if driver == 'ERROR':
			print '-- Attempt 2 to open webdriver --'
			driver = open_browser()
			if driver == 'ERROR':
				print '** End Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
				driver.close()
				print '|ERROR|'
				exit()

		print '[OK]- Browser Opened -[OK]\n'

		print '-- Opening Cpanel --'
		driver.get("http://www.example.com/cpanel")
		time.sleep(5)

		if driver.current_url != 'https://www.example.com:2083/':
			print '[X]- CPanel Page is not as expected -[X]'
			driver.close()
			print '** End Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
			print '|ERROR|'
			exit()

		print '-- Logging IN --'
		try:
			username = driver.find_element_by_id("user")
		except:
			time.sleep(5)
			username = driver.find_element_by_id("user")

		username.clear()
		username.send_keys("username")
		password = driver.find_element_by_id("pass")
		password.clear()
		password.send_keys("password")
		login_btn = driver.find_element_by_id("login_submit")
		login_btn.click()
		print 'Login Button Clicked'
		time.sleep(5)
		
		try:
			verify_login = driver.find_element_by_id("stats_homedir_value")
			print "[!] - Keyword : "+verify_login.text

			if verify_login.text.upper() != '/HOME/USERNAME':
				print '[X]- Login Page is not as expected -[X]'
				driver.close()
				print '** End Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
				print '|ERROR|'
				exit()
		except:
			if '?login=1' in driver.current_url:
				print '-- Login Validation completed with URL --\n'

		print '-- Logged In Successfully --\n' 
		
		try:
			ssl_link = driver.find_element_by_id("item_ssl_tls")
		except:
			time.sleep(5)
			ssl_link = driver.find_element_by_id("item_ssl_tls")

		ssl_link.click()
		time.sleep(5)

		try:
			manage_ssl = driver.find_element_by_id("lnkInstall")
		except:
			time.sleep(5)
			manage_ssl = driver.find_element_by_id("lnkInstall")

		print "[!] - Keyword : "+manage_ssl.text
		if manage_ssl.text.upper() != 'MANAGE SSL SITES.':
			print '[X]- SSL Manager Page is not as expected -[X]'
			driver.close()
			print '** End Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
			print '|ERROR|'
			exit()

		print '-- Navigated to SSL Manager page --\n'
		manage_ssl.click()
		time.sleep(5)

		try:
			install_ssl_page = driver.find_element_by_id("hdrInstallWebsite")
		except:
			time.sleep(5)
			install_ssl_page = driver.find_element_by_id("hdrInstallWebsite")
			
		print "[!] - Keyword : "+ install_ssl_page.text
		if install_ssl_page.text.upper() != 'INSTALL AN SSL WEBSITE':
			print '[X]- SSL Installer Page is not as expected -[X]'
			driver.close()
			print '** End Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
			print '|ERROR|'
			exit()

		print '-- Navigated to SSL Installer page --\n'
		old_expiry_date = get_SSL_expiry()

		print '[!] - Old Exipry Date Obtained  : '+old_expiry_date+'\n'

		domain = Select(driver.find_element_by_id('ssldomain'))
		domain.select_by_value('example.com')

		print '-- Selected Domain as example.com --'
		cert_textarea = driver.find_element_by_id("sslcrt")
		cert_textarea.clear()
		cert_textarea.send_keys(certificate)

		print '-- New Certificate copied to certificate textarea --'
		key_textarea = driver.find_element_by_id("sslkey")
		key_textarea.clear()
		key_textarea.send_keys(key)

		print '-- New Key copied to certificate textarea --'
		time.sleep(5)

		install_btn = driver.find_element_by_id("btnInstall")
		install_btn.click()

		print '-- Installing New Certificate. Wait for 30 seconds --\n'
		time.sleep(30)
		
		print '-- Get new expiry date --'
		new_expiry_date = get_SSL_expiry()

		print '[!] - New Exipry Date Obtained  : '+new_expiry_date+'\n'

		print '-- Logging Out --'
		driver.get("https://www.example.com:2083/logout/?locale=en")

		print '-- Logged Out Successfully --\n'
		
		vertify_ssl = verify_installation(old_expiry_date,new_expiry_date)
		if vertify_ssl == True:
			driver.close()
			print '** End Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
			print '|SUCCESS|'
			exit()
		else:
			driver.close()
			print '** End Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
			print '|ERROR|'
			exit()

	except Exception,e:
		print '[X]- Exception Occured : '+str(e) + ' -[X]'
		print '** End Time : {time} **'.format(time = format(datetime.datetime.now()+timedelta(hours=12.5),'%d-%b-%Y %H:%M:%S'))
		print '|ERROR|'
		driver.close()
		exit()

certificate = sys.argv[1]
key = sys.argv[2]

# Call the main function
main()