import requests
from bs4 import BeautifulSoup

GPX_HEADER = """<?xml version="1.0" encoding="utf-8"?><gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" creator="https://www.mtbproject.com">"""


def get_trail_ids(state):
    area_id = 0

    if state == 'GA':
        area_id = 8007899
    trail_ids = []
    
    for i in range(1, 20):
        html_str = requests.get('http://mtbproject.com/ajax/area/' + str(area_id) + '/trails?idx=' + str(i)).json()['markup']
        html_obj = BeautifulSoup(html_str, 'html.parser')
        rows = html_obj.find_all('tr')
        
        for row in rows:
            #print(row['data-href'])
            trail_ids.append(row['data-href'].split('/')[4])
    print(trail_ids)
    return trail_ids

def get_gpx_files(trail_ids, file_path):
    request_headers = {
        'authority': 'www.mtbproject.com',
        'referer': 'https://www.mtbproject.com/trail/7002910/forest-road-93',
        'cookie': 'user=v%3D3%26id%3D201004791%26sec%3D%26t%3D1609447856%26md5%3D7c183bc008a0a3e99c9ad4c9b09afaae; ids=a%3A1%3A%7Bi%3A0%3Bi%3A201004791%3B%7D; photosTitle=Nearby+Photos; photoIds=%5B%5D; pageCount=482; XSRF-TOKEN=eyJpdiI6IktkRnR5M0gwRmZwUWdUVkViajJNV0E9PSIsInZhbHVlIjoiakh1eUtvYkFFSHpFRDlEbkN6bkhFc1NCc0hmcWplR2htZGpDUHpId1wvZDczMnhlN0QzWTdFbHM3NkNpbnF6VksiLCJtYWMiOiJmYzlhZmQ5YTBjMDczMWU5NmVjYTFlMmU5ODg1YmYwZjFlZjNhYTNkMDFmYWI2MmM4ODYzYjRlMTQwMzVlNjgyIn0%3D; laravel_session=eyJpdiI6IisrTE5BcmQ0eXVHT2ZnZytJdFdTOWc9PSIsInZhbHVlIjoiSHV1THAyTWJKMmlpTzljVlUzcmVtTmJNT2RZV1JZeFdPcUQ0WjBINEg4bklOMmhzRFlKODhvSG9sdUhsSVFrSSIsIm1hYyI6ImQzN2UxMDUzYzYxNWM3MzRjMmNjZTY0OGI5YWZjYmUwOGUxN2ZjOTM0YzY2NWQyNGY1YzBiYzNiMjlhZjdjNjIifQ%3D%3D; prefs=%5BcommentSort%7Coldest%5D%5BmapX%7C-8738335%5D%5BmapY%7C4731387%5D%5BmapZoom%7C11.9%5D'
    }

    with open(file_path, 'w') as gpx_file:
        gpx_file.write(GPX_HEADER)

    with open(file_path, 'a') as gpx_file:
        for trail in trail_ids:
            http_response = requests.get('https://www.mtbproject.com/trail/gpx/' + trail, headers=request_headers)
            gps_xml = BeautifulSoup(http_response.text, 'xml')
            print(gps_xml.metadata.text)
            gpx_file.write(str(getattr(gps_xml.metadata, 'name')))
            gpx_file.write(str(gps_xml.trk))
        gpx_file.write('</gpx>')

trail_ids = get_trail_ids('GA')
get_gpx_files(trail_ids, 'test_gpx.gpx')