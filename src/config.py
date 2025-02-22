un = 'MANUAL'
pw = 'MANUAL'
fee = 0.075
initial_amount = 10000

# Custom xpaths

custom_xpath_replay = '/html/body/div[9]/div/div[2]/div[3]/div'
custom_xpath_play_replay = 'a'
custom_xpath_last_price = '/html/body/div[1]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[3]/div[1]/div/span[4]/span[2]'

# GUI

font = "Arial"
font_weight = "bold"
font_size = 14

# Use larger number for slower internet.
sleep = 2

# URLS
signin_url = "https://www.tradingview.com/#signin"
report_path = './output/trade_report.csv'
# Colors
textarea_color = "#000000"
bg_color = "#FFFFFF"
entry_bg_color = "#EEEBEB"
profit_color = "#237221"
loss_color = "red"
width=424
height=814

# X paths

next_button_xpath = '/html/body/div[5]/div/div[2]/div[3]'

play_pause_button_xpath = '/html/body/div[5]/div/div[2]/div[2]'

# open_price_xpath = '/html/body/div[2]/div[5]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]'
open_price_xpath = '/html/body/div[2]/div[5]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]'

open_price_xpath_2 = '//div[@class="valuesAdditionalWrapper-1WIwNaDF"]/div[2]/div[2]'

high_price_xpath = '/html/body/div[2]/div[5]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[3]/div[2]'
high_price_xpath_2 = '//div[@class="valuesAdditionalWrapper-1WIwNaDF"]/div[3]/div[2]'

low_price_xpath = '/html/body/div[2]/div[5]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[4]/div[2]'
low_price_xpath_2 = '//div[@class="valuesAdditionalWrapper-1WIwNaDF"]/div[4]/div[2]'

close_price_xpath = '/html/body/div[2]/div[5]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[5]/div[2]'
close_price_xpath_2 = '//div[@class="valuesAdditionalWrapper-1WIwNaDF"]/div[5]/div[2]'

last_price_xpath = '/html/body/div[2]/div[5]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[8]/div[2]'

symbol_xpath = '//*[@id="header-toolbar-symbol-search"]/div'

buy_button_xpath = '/html/body/div[2]/div[5]/div[1]/div/div/div[4]/div[2]/button'
sell_button_xpath = '/html/body/div[2]/div[5]/div[1]/div/div/div[4]/div[1]/button'
flatten_button_xpath = '/html/body/div[2]/div[5]/div[1]/div/div/div[4]/div[3]/button'

volume_xpath='//*[@id="overlap-manager-root"]/div/span/div[1]/div/div/div/div[1]/span/span[1]/input'
volume_button_xpath='/html/body/div[2]/div[5]/div[1]/div/div/div[4]/button'
