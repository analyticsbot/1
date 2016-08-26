from ConfigParser import SafeConfigParser
import sys

## initializing the config parser
parser = SafeConfigParser()
parser.read('config.cfg')

""" ## setting up static variables ## """
## token for accessing the api from crowdkast
username = parser.get('datatree', 'username').replace("'",'').strip()
salutation = parser.get('datatree', 'salutation').replace("'",'').strip()
client_name = parser.get('datatree', 'client_name').replace("'",'').strip()
client_address = parser.get('datatree', 'client_address').replace("'",'').strip()
billing_card_number = parser.get('datatree', 'billing_card_number').replace("'",'').strip().strip()
card_cvv_number = parser.get('datatree', 'card_cvv_number').replace("'",'').strip()
billing_address = parser.get('datatree', 'billing_address').replace("'",'').strip()
billing_expiry_date = parser.get('datatree', 'billing_expiry_date').replace("'",'').strip()
billing_expiry_date = parser.get('datatree', 'billing_expiry_date').replace("'",'').strip()
url_login = parser.get('datatree', 'url_login').replace("'",'').strip()
pwd = parser.get('datatree', 'pwd').replace("'",'').strip()
state = parser.get('datatree', 'state').replace("'",'').strip()
county = parser.get('datatree', 'county').replace("'",'').strip()
keyword = parser.get('datatree', 'keyword').replace("'",'').strip()
input_file_name = parser.get('datatree', 'input_file_name').replace("'",'').strip()
last_document_type = parser.get('datatree', 'last_document_type').replace("'",'').strip()
text_box_left_parsed = parser.get('datatree', 'text_box_left_parsed').replace("'",'').strip()
right_side_name = parser.get('datatree', 'right_side_name').replace("'",'').strip()
right_side_address = parser.get('datatree', 'right_side_address').replace("'",'').strip()
right_side_date = parser.get('datatree', 'right_side_date').replace("'",'').strip()
MAX_PAGES_SCRAPE = int(parser.get('datatree', 'MAX_PAGES_SCRAPE').replace("'",'').strip())
doc_types = parser.get('datatree', 'doc_types').replace("'",'').strip().replace('[','').replace(']','').replace(' ','').split(',')
years = parser.get('datatree', 'years').replace("'",'').strip().replace('[','').replace(']','').replace(' ','').split(',')
verbosity = parser.get('datatree', 'verbosity').replace("'",'').strip()
headers = parser.get('datatree', 'headers').replace("'",'').strip().replace('[','').replace(']','').replace(' ','').split(',')
ignore_keywords = parser.get('datatree', 'ignore_keywords').replace("'",'').strip().replace('[','').replace(']','').replace(' ','').split(',')
flexi_search_url = parser.get('datatree', 'flexi_search_url').replace("'",'').strip()
