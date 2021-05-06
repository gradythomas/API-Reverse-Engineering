import requests
import json
import os

def get_stream_link(song_id):
    request_headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://play.nugs.net/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': """__cfduid=d43ea3cae0c3e12db42ded1ead940b9f11619490964; _gcl_au=1.1.574648501.1619490971; _ga=GA1.2.2046220753.1619490971; _fbp=fb.1.1619490971070.836033997; __cq_seg=0~0.00\u00211~0.00\u00212~0.00\u00213~0.00\u00214~0.00\u00215~0.00\u00216~0.00\u00217~0.00\u00218~0.00\u00219~0.00; __cq_uuid=acAO4bYQ2cUtXwr6l0bhaihrGT; ubvt=ce699160-15bc-496e-b63e-bb08cc85126b; __utma=168320867.2046220753.1619490971.1620249410.1620249410.1; __utmz=168320867.1620249410.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gid=GA1.2.817797413.1620337332; amp_504fd2=QNTXt0uwfI7wJAvoSvua_B...1f51q35i4.1f51q35i5.8.0.8; amplitude_id_504fd2931526c709ffbabe5ec765d52anugs.net=eyJkZXZpY2VJZCI6IjM2NzBkYmVkLTBhNTYtNDI2MC1hMjFiLTk1MzNmMjcwMjAxNFIiLCJ1c2VySWQiOiI5NjU5NzEiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE2MjAzMzczNDgzODgsImxhc3RFdmVudFRpbWUiOjE2MjAzMzc0MDA1MDEsImV2ZW50SWQiOjMxLCJpZGVudGlmeUlkIjowLCJzZXF1ZW5jZU51bWJlciI6MzF9"""
    }

    html_response = requests.get('https://streamapi.nugs.net/bigriver/subplayer.aspx?orgn=nndesktop&HLS=1&app=1&callback=angular.callbacks._a&endDateStamp=1620996373&nn_userID=965971&startDateStamp=1618404373&subCostplanIDAccessList=net.nugs.multiband.monthly.subscription&subscriptionID=1fa01c65418738f780806905c7676b15&trackID=' + str(song_id), headers=request_headers)
    streaming_link = json.loads(html_response.text.split('(')[1].split(')')[0])['streamLink']
    print(streaming_link)
    return streaming_link, streaming_link.split('/')[7].split('?')[0]

def get_song_file(streaming_link, file_path):
    with open(file_path, 'wb') as file:
        file.write(requests.get(streaming_link).content)

def download_show(starting_id):
    for i in range(20):
        link, name = get_stream_link(starting_id + i)
        name_prefix = name.split('_')[0]
        track_title = name.replace(name_prefix + '_', '')
        print(track_title)
        try:
            os.mkdir('songs/' + name_prefix)
        except:
            pass
        get_song_file(link, 'songs/' + name_prefix + '/' + track_title)

download_show(453291)