import sys
import urllib2, urllib
from time import time
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser

NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2

def fetch_home_logo(WEBSITE_ROOT):
	status = []
	try:
		result = urllib2.urlopen(WEBSITE_ROOT)
		html = result.read()
		soup = BeautifulSoup(html)
		img_tag = soup.find('img', attrs={'alt':'Home'})
		logo_heading = img_tag['alt']
		logo_url = ''
		if img_tag.has_key('src'):
			logo_url = '%s' % img_tag['src']
		else:
			status = [NAGIOS_CRITICAL, 'ERROR: Logo image has no link']
		urllib.urlretrieve(logo_url, '/dev/null')
		status = [NAGIOS_OK, logo_heading]
	except:
		status = [NAGIOS_CRITICAL, 'ERROR: Failed to retrieve the logo']
	return status

def main():
	parser = OptionParser() 
	parser.add_option('-w', dest='time_warn', default=1.8,
				help="Warning threshold in seconds, default: %default") 
	parser.add_option('-c', dest='time_crit', default=3.8,
				help="Critical threshold in seconds, default: %default") 
	(options, args) = parser.parse_args()
	if options.time_crit < options.time_warn:
		options.time_warn = options.time_crit
	
	start = time()
	code, message = fetch_home_logo(args[0])
	elapsed = time() - start
	if code != 0:
		print message
		sys.exit(code)
	else:
		msg = "%s:Logo '%s' retrieved in %f seconds"
		if elapsed < float(options.time_warn):
			print msg % ('OK', message, elapsed)
			sys.exit(NAGIOS_OK)
		elif elapsed < float(options.time_crit):
			print msg % ('WARNING', message, elapsed)
			sys.exit(NAGIOS_WARNING)
		else:
			print msg % ('CRITICAL', message, elapsed)
			sys.exit(NAGIOS_CRITICAL)

if __name__ == '__main__':
	main()
