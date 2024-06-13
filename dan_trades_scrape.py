import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# In characters
MAX_SNIPPET_LENGTH = 1000

VARIETY_URL = 'https://variety.com/v/film/'
VARIETY_FILE = 'variety_trades.html'

HOLLYWOOD_URL = 'https://www.hollywoodreporter.com/c/movies/'
HOLLYWOOD_FILE = 'hollywood_trades.html'

WRAP_URL = 'https://www.thewrap.com/category/movies/'
WRAP_FILE = 'wrap_trades.html'

DEADLINE_TV_URL = 'https://deadline.com/v/tv/'
DEADLINE_TV_FILE = 'deadline_tv_trades.html'

DEADLINE_FILM_URL = 'https://deadline.com/v/film/'
DEADLINE_FILM_FILE = 'deadline_film_trades.html'

SCREENDAILY_URL = 'https://www.screendaily.com/latest/45187.more?navcode=24&page='
SCREENDAILY_FILE = 'screendaily_trades.html'

CSS_STYLE_HEADER = '<p style=\"font-size:16px; font-family:\'Calibri\'\">'

WEBSITE_CLASSES = [
	#['Variety', VARIETY_URL, VARIETY_FILE, 'o-tease__primary lrv-u-width-100p', 'vy-cx-page-content', 'title-of-a-story', True],
	['Variety', VARIETY_URL, VARIETY_FILE, 'o-tease__primary u-flex-2@tablet', 'c-title__link', 'c-title__link', False],
	['Hollywood Reporter', HOLLYWOOD_URL, HOLLYWOOD_FILE, 'lrv-u-flex lrv-u-flex-direction-column lrv-u-height-100p lrv-u-justify-content-center', 'a-article-grid__main', 'title-of-a-story', True],
	['The Wrap', WRAP_URL, WRAP_FILE, 'post-item--archive', 'wp-block-post-excerpt__excerpt', 'wp-block-post-title', False],
	['Deadline TV', DEADLINE_TV_URL, DEADLINE_TV_FILE, 'pmc-a-grid pmc-a-cols3 pmc-a-cols4@desktop-xl', 'a-content', 'c-title__link', False],
	['Deadline Film', DEADLINE_FILM_URL, DEADLINE_FILM_FILE, 'pmc-a-grid pmc-a-cols3 pmc-a-cols4@desktop-xl', 'a-content', 'c-title__link', False],
	['Screendaily', SCREENDAILY_URL, SCREENDAILY_FILE, 'storyDetails', 'storytext', 'storyDetails', False]
]

#last_article, website_name, website_url, out_file, html_class, text_class, title_class, search_by_id

BAD_PARAGRAPHS = ['Related Story', 'Primetime-Panic', 'Watch on Deadline',
'Related Stories', 'A version of this story ', 'issue of TheWrap magazine']

cookies = {
    'WV_SESSION': 'mszesqr1skezcropvq33jwqq',
    'AnonUserCookie': 'bc05e667-47f9-4e02-95df-f48f7043d320',
    '_js': '1',
    '_fbp': 'fb.1.1717002836953.23989282376886537',
    'OptanonAlertBoxClosed': '2024-05-29T17:14:01.237Z',
    'AgentCookie': '38FCE9807ADB449287F0519438923559',
    'ADConCtrlCookie': '392f725c-7b1b-4397-9b85-a2628733be4b',
    '_hjSessionUser_136299': 'eyJpZCI6IjNkMWUwMGExLWJhMDMtNWI0Ni05OGJkLTMwYzgzZDk3NDBkOSIsImNyZWF0ZWQiOjE3MTcwMDI4MzczNTIsImV4aXN0aW5nIjp0cnVlfQ==',
    'js': '1',
    '_gcl_au': '1.1.602341478.1717007652',
    '_hjSessionUser_133458': 'eyJpZCI6IjI5NjA5ZTdjLTMzZTQtNWRlNy1iMmFhLWJhM2YyYTJmM2ExYSIsImNyZWF0ZWQiOjE3MTcwMDc2NTIyNzcsImV4aXN0aW5nIjp0cnVlfQ==',
    '_ga_MKDW83Y87G': 'GS1.1.1717007652.1.1.1717008134.60.0.0',
    '_gid': 'GA1.2.1543171604.1718299250',
    '_hjSession_136299': 'eyJpZCI6IjhkNGUzZmE2LWEyY2QtNGJiNi1iZDBjLTAxNmVkMWNlZTk1ZiIsImMiOjE3MTgyOTkyNTAyNzQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
    '.ASPXAUTH': 'C0B1585930775F43EFF7455A824EE1DF2D4146B68F19483A6F99A3BE03E48F9D94F77537C5E7691F7FB8E4DE4CCCD23127611140BE95E2285DF7E820A4B08C9013B39CD7C13B883C7461312117118E37675A59656449FCB818E8D44CAACA07B9B0AE9B9BE4EC0B7D25CAEE03A7C1A24FF0CD9440139ECFD1121EF46FFA35C086EEB0828696BF1484CB16044086EB0B5920E9A9B10C5D371175B0A916141D43D818CB57DC06D154EE4CC40BA95759C33B130CD9271A3258A451EBDD2341B399611F826E0391215797B5D78F373D61E3AD2A78E38222256D7633EC87470D527C11D8BB264E0FC0D39483DD65FE4E7FE0787315FB6A62EA5A6B2D1CD42D7D97224153AE9DD4AC5E30AD88AF2AE5ECA2D46E43F4A97F4F2A909ACF684F3B6BF53AD223C68C1DC3F60934EB5855F181775EF3812A9BB8FFBFA282092B21C07E083552E20790667739BB066D87FBB477414FED1540D3E1408E347D100971CFFC0DED3AC11AC7AA4E3253E61F4D66204B56F14D547F56359F17165FE86A55DCB862D285C943989A2C2982CEDE1EF404C8E94C182C5BD5CC4093AB9EA110E3FC43CBE9F0B498B4AB993B55BA55779EEA249518FC0C0447490029D28DAC8209807EB39D716E614F873133548E9480E7E76D9D6B4B18DD7C2024BE8648FB506DB90898844A3AFCA27F0F6F256955B7342B2EBFD12D16171287ECE5ABE75614A8FEFC37008CBDA9C2A695A466E2C199EE5E914D8621639A325213CB073D4F3C3D620E4A0A61237C48540A59DC3F78B7DD01261A400959959AC155F4009215BCF90D66865094ACA8253993B8446EBC7839FC9C948FA9C0B990792F976A9A6504435766E866720274791C1571F30B4EBF3E0FD79427C303BBBEB9F87DC264FAF1E1E35B2EE0FAA407C74D6BCD089D926FC3279B3884C6CCC49A88919FCADD4C171C05603C578154723182AC9B3009CA4C7AFD55D5159DBDEFD1561ED1957DAB91E8CBA5E51A18E33C61CC84DC7E64CEE84EBEC93B09D10B6600DE809D716BE02275AF6C0ABBD9B82CA0E34D5908652B956B603847D07D993A13753FCC159711126D62FAA65529E624B014C036E82366005DC9AFE4E37A141E9D2A79378C21F3CC6B9E636B74A918DD522F05AADF87526F5FBF4A88A6BDB8B65C794F9B28896359C0600200DC8172B51B499D578B2DD1FEE4C6F46925950DF4A747402EC65D50012215D6F74F84EE9C05F42ECC58B9FBF41B2C0EC437BB9F8B15A8C43336F6405E0ABC81CDE7C4B1FB44C510873DB90C5F84DF359D469A12778AC9079D20A528E122EF11C8B117376F53DB0D0AF8D2ACB960185CC649F5C00207FF9E72C8E22F7651A7AA4F8DD19E1E736A9128D8A5A5AEC28268FD00E5706634B5DC907CC9A47508FBC9532F5A76676DBCA2C4A65D5076A2801E4A49CCFA485FDC61146B9D256FD6BEC2C252ABDA921F050441794576C09BC12A8BD2BADA7B71E24B3B612B89F4BA064C4287F3DF2ABA8C5BD092763F16ABFCA68F1ADEE80DD4C49532A5327BE413951D9D31E892C77DAD629D42D5D449179D7C821203E813F5B74398349921A8EE3E6913E911',
    'ADFEAuthCookie': 'CMBYLZ4_F0B17A46656B3478655330356246753942476A39434B3371416B646A624452416A3971423044304A6B307836634C62386E4970496962726E675375346D61686963756549475575475245424744524666766E554A4B496A74417A354349782F33647558436664575051554A4F3333496B3874625844312F5438307073696447426A596A45414E42654E7A58376D48576C6B45334B314A6251387956687461576C4E316B626F3759683777355865325A6B37504D596F6D4E4A5330546F4E6952326133',
    '__gads': 'ID=1e018f936cde8834:T=1717002837:RT=1718299562:S=ALNI_MbkTKpaVbi97jjnmL3JDkq3B1dPog',
    '__gpi': 'UID=00000e0ea2461596:T=1717002837:RT=1718299562:S=ALNI_MYCujeQkDW4OWqeCiZQ-QB9hoQZ4w',
    '__eoi': 'ID=8f67b8d92564968b:T=1717002837:RT=1718299562:S=AA-AfjYLiD5uSdPAYWla3XBXBoN4',
    'sp_': '{12.207.239.194}{5193952[ID3617|S36|LV|0]}{5194102[ID7032|S69|LV|0]}{5194479[ID7214|S71|LV|0]}{5194483[ID6326|S62|LV|0]}',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Jun+13+2024+10%3A28%3A22+GMT-0700+(Pacific+Daylight+Time)&version=6.25.0&isIABGlobal=false&consentId=bb63563e-1807-45aa-a396-4630dfa8d745&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0002%3A1&hosts=H5%3A1%2CH43%3A1%2CH47%3A1&genVendors=&geolocation=US%3BCA&AwaitingReconsent=false',
    '_ga_1XQNN4CBP7': 'GS1.1.1718299250.8.1.1718299702.0.0.0',
    '_ga_SWCENS45CR': 'GS1.1.1718299250.8.1.1718299702.0.0.0',
    '_ga': 'GA1.2.97075042.1717002837',
    '_gat_UA-37114222-3': '1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'WV_SESSION=mszesqr1skezcropvq33jwqq; AnonUserCookie=bc05e667-47f9-4e02-95df-f48f7043d320; _js=1; _fbp=fb.1.1717002836953.23989282376886537; OptanonAlertBoxClosed=2024-05-29T17:14:01.237Z; AgentCookie=38FCE9807ADB449287F0519438923559; ADConCtrlCookie=392f725c-7b1b-4397-9b85-a2628733be4b; _hjSessionUser_136299=eyJpZCI6IjNkMWUwMGExLWJhMDMtNWI0Ni05OGJkLTMwYzgzZDk3NDBkOSIsImNyZWF0ZWQiOjE3MTcwMDI4MzczNTIsImV4aXN0aW5nIjp0cnVlfQ==; js=1; _gcl_au=1.1.602341478.1717007652; _hjSessionUser_133458=eyJpZCI6IjI5NjA5ZTdjLTMzZTQtNWRlNy1iMmFhLWJhM2YyYTJmM2ExYSIsImNyZWF0ZWQiOjE3MTcwMDc2NTIyNzcsImV4aXN0aW5nIjp0cnVlfQ==; _ga_MKDW83Y87G=GS1.1.1717007652.1.1.1717008134.60.0.0; _gid=GA1.2.1543171604.1718299250; _hjSession_136299=eyJpZCI6IjhkNGUzZmE2LWEyY2QtNGJiNi1iZDBjLTAxNmVkMWNlZTk1ZiIsImMiOjE3MTgyOTkyNTAyNzQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; .ASPXAUTH=C0B1585930775F43EFF7455A824EE1DF2D4146B68F19483A6F99A3BE03E48F9D94F77537C5E7691F7FB8E4DE4CCCD23127611140BE95E2285DF7E820A4B08C9013B39CD7C13B883C7461312117118E37675A59656449FCB818E8D44CAACA07B9B0AE9B9BE4EC0B7D25CAEE03A7C1A24FF0CD9440139ECFD1121EF46FFA35C086EEB0828696BF1484CB16044086EB0B5920E9A9B10C5D371175B0A916141D43D818CB57DC06D154EE4CC40BA95759C33B130CD9271A3258A451EBDD2341B399611F826E0391215797B5D78F373D61E3AD2A78E38222256D7633EC87470D527C11D8BB264E0FC0D39483DD65FE4E7FE0787315FB6A62EA5A6B2D1CD42D7D97224153AE9DD4AC5E30AD88AF2AE5ECA2D46E43F4A97F4F2A909ACF684F3B6BF53AD223C68C1DC3F60934EB5855F181775EF3812A9BB8FFBFA282092B21C07E083552E20790667739BB066D87FBB477414FED1540D3E1408E347D100971CFFC0DED3AC11AC7AA4E3253E61F4D66204B56F14D547F56359F17165FE86A55DCB862D285C943989A2C2982CEDE1EF404C8E94C182C5BD5CC4093AB9EA110E3FC43CBE9F0B498B4AB993B55BA55779EEA249518FC0C0447490029D28DAC8209807EB39D716E614F873133548E9480E7E76D9D6B4B18DD7C2024BE8648FB506DB90898844A3AFCA27F0F6F256955B7342B2EBFD12D16171287ECE5ABE75614A8FEFC37008CBDA9C2A695A466E2C199EE5E914D8621639A325213CB073D4F3C3D620E4A0A61237C48540A59DC3F78B7DD01261A400959959AC155F4009215BCF90D66865094ACA8253993B8446EBC7839FC9C948FA9C0B990792F976A9A6504435766E866720274791C1571F30B4EBF3E0FD79427C303BBBEB9F87DC264FAF1E1E35B2EE0FAA407C74D6BCD089D926FC3279B3884C6CCC49A88919FCADD4C171C05603C578154723182AC9B3009CA4C7AFD55D5159DBDEFD1561ED1957DAB91E8CBA5E51A18E33C61CC84DC7E64CEE84EBEC93B09D10B6600DE809D716BE02275AF6C0ABBD9B82CA0E34D5908652B956B603847D07D993A13753FCC159711126D62FAA65529E624B014C036E82366005DC9AFE4E37A141E9D2A79378C21F3CC6B9E636B74A918DD522F05AADF87526F5FBF4A88A6BDB8B65C794F9B28896359C0600200DC8172B51B499D578B2DD1FEE4C6F46925950DF4A747402EC65D50012215D6F74F84EE9C05F42ECC58B9FBF41B2C0EC437BB9F8B15A8C43336F6405E0ABC81CDE7C4B1FB44C510873DB90C5F84DF359D469A12778AC9079D20A528E122EF11C8B117376F53DB0D0AF8D2ACB960185CC649F5C00207FF9E72C8E22F7651A7AA4F8DD19E1E736A9128D8A5A5AEC28268FD00E5706634B5DC907CC9A47508FBC9532F5A76676DBCA2C4A65D5076A2801E4A49CCFA485FDC61146B9D256FD6BEC2C252ABDA921F050441794576C09BC12A8BD2BADA7B71E24B3B612B89F4BA064C4287F3DF2ABA8C5BD092763F16ABFCA68F1ADEE80DD4C49532A5327BE413951D9D31E892C77DAD629D42D5D449179D7C821203E813F5B74398349921A8EE3E6913E911; ADFEAuthCookie=CMBYLZ4_F0B17A46656B3478655330356246753942476A39434B3371416B646A624452416A3971423044304A6B307836634C62386E4970496962726E675375346D61686963756549475575475245424744524666766E554A4B496A74417A354349782F33647558436664575051554A4F3333496B3874625844312F5438307073696447426A596A45414E42654E7A58376D48576C6B45334B314A6251387956687461576C4E316B626F3759683777355865325A6B37504D596F6D4E4A5330546F4E6952326133; __gads=ID=1e018f936cde8834:T=1717002837:RT=1718299562:S=ALNI_MbkTKpaVbi97jjnmL3JDkq3B1dPog; __gpi=UID=00000e0ea2461596:T=1717002837:RT=1718299562:S=ALNI_MYCujeQkDW4OWqeCiZQ-QB9hoQZ4w; __eoi=ID=8f67b8d92564968b:T=1717002837:RT=1718299562:S=AA-AfjYLiD5uSdPAYWla3XBXBoN4; sp_={12.207.239.194}{5193952[ID3617|S36|LV|0]}{5194102[ID7032|S69|LV|0]}{5194479[ID7214|S71|LV|0]}{5194483[ID6326|S62|LV|0]}; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jun+13+2024+10%3A28%3A22+GMT-0700+(Pacific+Daylight+Time)&version=6.25.0&isIABGlobal=false&consentId=bb63563e-1807-45aa-a396-4630dfa8d745&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0004%3A1%2CC0002%3A1&hosts=H5%3A1%2CH43%3A1%2CH47%3A1&genVendors=&geolocation=US%3BCA&AwaitingReconsent=false; _ga_1XQNN4CBP7=GS1.1.1718299250.8.1.1718299702.0.0.0; _ga_SWCENS45CR=GS1.1.1718299250.8.1.1718299702.0.0.0; _ga=GA1.2.97075042.1717002837; _gat_UA-37114222-3=1',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}




def request_website(website_name, website_url, page_count):

	if website_name == 'Screendaily':
		request_url = website_url + str(page_count)
		return requests.get(request_url, headers=headers, cookies=cookies)
	elif page_count > 1:
		request_url = website_url + 'page/' + str(page_count) + '/'
	else:
		request_url = website_url

	return requests.get(request_url, allow_redirects=False)

def get_article_link(website_name, article, search_by_id):

	if website_name == 'Screendaily':
		title_element = article.find('h3')
	elif search_by_id:
		title_element = article.find(id= title_class)
	else:
		title_element = article.find(class_= title_class)

	link_element = title_element.find('a')

	if link_element:
		return link_element['href'].strip()
	else:
		return title_element['href'].strip()


def scrape_website(last_article, website_name, website_url, out_file, html_class, text_class, title_class, search_by_id):

	output_file = open(out_file, 'w', encoding='utf-8')

	print('Starting ' + website_name + ' request')

	print('Checking link...')

	# MAKE SURE THE LINK HASN'T CHANGED.
	check_link_page = request_website(website_name, last_article, 0)
	check_link_soup = BeautifulSoup(check_link_page.content, 'html.parser')

	if check_link_page.status_code == 301:
		if 'location' in check_link_page.headers:
			new_link = check_link_page.headers['location']
			return 'The link was changed to ' + '\n\n' + new_link + '\n\n Please check that this article is still in the section: ' + '\n\n' + website_url + '\n\n And retry with the correct link.'


	article_count = 0
	page_count = 1

	current_link = ''

	article_stack = []

	last_article_header = ''
	last_article_link = ''


	while current_link != last_article:


		print('Reading page ' + str(page_count))

		page = request_website(website_name, website_url, page_count)
		#print(page.encoding)

		if 'Response [503]' in str(page):
			print('It appears that ' + website_url + ' is down.' )

		soup = BeautifulSoup(page.text, 'html.parser')
		articles = soup.find_all('div', class_= html_class)
		for article in articles:

			# For the wrap sidebar articles
			article_spans = article.find("span",{'class':'category'})
			if article_spans == None:

				entry_text = ''

				if website_name == 'Screendaily':
					title_element = article.find('h3')
				elif search_by_id:
					title_element = article.find(id= title_class)
					#print(title_element)
				else:
					title_element = article.find(class_= title_class)

				link_element = title_element.find('a')

				if link_element:
					current_link = link_element['href'].strip()
				else:
					current_link = title_element['href'].strip()
					print('currentlink' + current_link)

				if current_link == last_article:
					break


				link_href = '<a href=\"' + current_link + '\">' + current_link + '</a>'
				entry_text = CSS_STYLE_HEADER + '<b>' + title_element.text.strip() + '</b>'

				article_text = read_article(current_link, text_class)

				if article_text:
					entry_text += '<br>' + article_text

				entry_text += '<br>' + link_href + '</p>'

				article_stack.append(entry_text)

				if article_count == 0:
					last_article_header = title_element.text.strip()
					last_article_link = link_href

				article_count = article_count + 1

		page_count = page_count + 1

	print_trades_info(output_file, website_name, last_article_header, last_article_link)

	while len(article_stack) > 0:
		output_file.write(article_stack.pop())

	print('Found ' + str(article_count) + ' articles')
	output_file.close()
	print('Done')


def print_trades_info(output_file, website_name, last_article_header, last_article_link):

	current_date = datetime.now()
	current_date_str = current_date.strftime('%m/%d/%y')
	last_article_string = CSS_STYLE_HEADER + '<b>' + current_date_str + ' // ' + website_name + ' // ' + last_article_header + '</b><br>'
	last_article_string += last_article_link + '<br><br>'

	output_file.write(CSS_STYLE_HEADER + 'Last article processed (post to slack): ' + '<br>')
	output_file.write(last_article_string)

	prev_date = current_date + timedelta(days=-1)

	if datetime.today().weekday() == 0:
		prev_date = current_date + timedelta(days=-3)

	prev_date = prev_date.strftime('%m/%d').lstrip('0').replace(' 0', ' ')
	current_date_str = current_date.strftime('%m/%d').lstrip('0').replace(' 0', ' ')

	if 'Film' in website_name:
		website_name = website_name.replace('Film', '(Film)')
	elif 'TV' in website_name:
		website_name = website_name.replace('TV', '(TV)')

	output_file.write('Trades - ' + prev_date + ' - ' + current_date_str + ' - ' + website_name)


def read_article(link, text_class):

	if 'screendaily' in link:
		page = requests.get(link, headers=headers, cookies=cookies)
	else:
		page = requests.get(link, allow_redirects=False)

	soup = BeautifulSoup(page.text, 'html.parser')
	content = soup.find('div', class_= text_class)

	# Feature articles have different formatting
	if 'thewrap' in link:
		if content is None:
			#content = soup.find('div', class_= 'wrappro-non-paywall')
			content = soup.find('div', class_= 'entry-content')
		if content is None:
			content = soup.find('section', class_= 'aesop-content')
		if content is None:
			content = soup.find('div', class_= 'tpd-wrapmagazine-content')

	if 'hollywoodreporter' in link:
		if content is None:
			content = soup.find('div', class_= 'a-featured-article-grid__content a-featured-article-image-offsets box')

	if 'variety' in link:
		if content is None:
			#content = soup.find('div', class_= 'a-featured-article-grid lrv-a-wrapper')
			 content = soup.find('div', class_= 'pmc-paywall')


	if 'deadline' in link:
		if content is None:
			content = soup.find('article')

	text = ''

	if content:

		paragraphs = content.find_all('p')

		p_count = 0

		return get_article_text(paragraphs, 2, link)


def get_article_text(paragraphs, ending_p, link):

    p_count = 0
    text = ''

    for p in paragraphs:

        if p.text != '':
            bad_p = False
            for bad_word in BAD_PARAGRAPHS:
                if bad_word in p.text:
                    bad_p = True
                    break

            # Screendaily articles sometimes have image captions in <p> within the article
            if 'screendaily' in link:
                if 'inline_source' in p.attrs.get('class', []) or 'inline_caption' in p.attrs.get('class', []):
                    bad_p = True


            if not bad_p:
                if p_count < ending_p:
                    if len(text) > MAX_SNIPPET_LENGTH:
                        break
                    text += p.text + ' '
                p_count = p_count + 1


    return text



if __name__ == '__main__':

	print()
	print('********** Trades Scraper by Vivienne Shaw *****************')
	print()

	while True:
		print('Enter website name')
		print('(screendaily, hollywood reporter, the wrap, variety, deadline tv, deadline film)')
		print('or \'all\' for all.')
		input_type = input(': ')
		if input_type == 'all':
			for website in WEBSITE_CLASSES:
				print()
				end_link = input("Enter last " + website[0] + " article: ")
				scrape_website(end_link.strip(), website[0], website[1], website[2], website[3], website[4], website[5], website[6])
				print()
		else:
			for website in WEBSITE_CLASSES:
				if input_type.lower() == website[0].lower():
					print()
					end_link = input("Enter last " + website[0] + " article: ")
					scrape_website(end_link.strip(), website[0], website[1], website[2], website[3], website[4], website[5], website[6])
