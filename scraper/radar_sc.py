import requests
import json
from pprint import pprint
import csv
import os
import time
import logging

dir_main = os.path.dirname(os.path.abspath(__name__))

dir_log = os.path.join(dir_main, 'logs')
log_file = os.path.join(dir_log, 'radar_sc_log.log')
logging.basicConfig(
    level=logging.INFO,  # تنظیم سطح لاگ (می‌توانید به دلخواه تغییر دهید)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]  # ذخیره لاگ در فایل و نمایش در کنسول
)

logger = logging.getLogger(__name__)
pg_num = 0
# URL API

while True:
    try:
        pg_num += 1
        url = 'https://realtorpanel.melkradar.com/odata/ClientApp/realtorEstateMarker/getRealtorEstateMarkers'

        payload = {
            "Filter": {
                "AdverTypeFilter": [],
                "EstateTypeFilter": [],
                "FilterMortgageFrom": None,
                "FilterMortgageTo": None,
                "FilterRentFrom": None,
                "FilterRentTo": None,
                "FilterSellPriceFrom": None,
                "FilterSellPriceTo": None,
                "FilterAreaSizeFrom": None,
                "FilterAreaSizeTo": None,
                "FilterBedroomFrom": None,
                "FilterBedroomTo": None,
                "IsFullMortgage": False,
                "FilterCityAreaGroupIds": [],
                "FilterCityAreaGroupCityAreas": [],
                "ShouldHaveWarehouse": None,
                "ShouldHaveElevator": None,
                "ShouldHaveParking": None,
                "ShouldHaveBalcony": None,
                "GetNoPriceAdvers": None,
                "SearchText": None,
                "BuildingAgeRanges": [],
                "FilterAdverDateFromStr": "1403-3-15",
                "FilterAdverDateToStr": "1403-6-31",
                "RadarCode": None,
                "FileCode": None
            },
            "PageSize": 1000,
            "PageNumber": pg_num
        }

        # افزودن توکن به هدر


        cookies = {
            "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IkMwOTYyNEZGNUQ5OTkyNkJFQkM4RTgwNkMxMUFGQjVDQ0I0NEI0NTkiLCJ4NXQiOiJ3SllrXzEyWmttdnJ5T2dHd1JyN1hNdEV0RmsiLCJ0eXAiOiJKV1QifQ.eyJuYmYiOjE3MjczMzkxNjUsImV4cCI6MTczNTExNTE2NSwiaXNzIjoiSWRlbnRpdHlTZXJ2ZXJDTiIsImF1ZCI6IklkZW50aXR5U2VydmVyQ04vcmVzb3VyY2VzIiwiY2xpZW50X2lkIjoiTWVsa1JhZGFyQ2xpZW50QXBwIiwic2NvcGUiOltbXSxbXSxbXV0sInN1YiI6IjcyMWZiNzAzLTlhN2QtNDEyZi05OTMxLTExNDZlYjJhZDNhYSIsImF1dGhfdGltZSI6MTcyNzMzOTE2NSwiaWRwIjoiaWRzcnYiLCJuYW1lIjoiNzIxZmI3MDMtOWE3ZC00MTJmLTk5MzEtMTE0NmViMmFkM2FhIiwibG9naW5fdHlwZSI6InJlYWx0b3IiLCJ0b2tlbiI6IjI4Yjc3Mzk0LWQzNzMtNGNhNi1iNDhkLTZjYzYyNzJjOWZjMCIsImp0aSI6InY0TjZlLW9LTjBYWjI1c3oyUnV5RVljUGtkR1Vsb2p6M1RTVkdfVXRGOVEiLCJhbXIiOltbXV19.YWnhYwxI8pPMMEv3JAbeh6FNZqmymNBLsHdo0zhI-0sq6xpK7wDPT4LPv-6EYZ5rl9CYoVY1OEcJN67kMmovWu50U8pWKq0iVOWJIRb7Ne92TSGE33SNDWspOi4C-1JKskeUez42FG8LlgE31XyjVH3_iLraDdfLaVj7D0KdW3niO_TcrD6uv4amI_S98p8AOagy0ZuVOJ2TKToXZtmH-Zwz60jDKuPtv4Zweth3TyYwjm0hVD-rzxGgeBhltMfGATvxN711xDW_m_wmO_PeK5jPrUob-N5w1_RgEL8iRGL6rWRswmauQ8u3Q_vFETJmsB3H7MdtWplDzmPufHwCqw"
        }        
        headers = {
            'Authorization': f'Bearer {cookies["access_token"]}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, json=payload, cookies=cookies, headers=headers)

        # بررسی پاسخ
        if response.status_code == 200:
            # print("Success:", response.json())
            pass
        else:
            print(f"Error {response.status_code}: {response.text}")


        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            # تبدیل داده‌های دریافتی به فرمت JSON
            data = response.json()
            # چاپ داده‌ها
            # pprint(data)/home/sjd/Desktop/Realstate-Ads-Data-divar-sheypoor-/sc_ads/
            api_dir = os.path.join(dir_main, "archieved_files/api_firstpage/radar_api_firstpage")
            all_api_files_and_dirs = os.listdir(api_dir)
            all_api_files = [f for f in all_api_files_and_dirs if os.path.isfile(os.path.join(api_dir, f))]
            api_name = os.path.join(api_dir, f"apidiv{len(all_api_files)}.json")
            
            for ads in data['value']:
                ads_folder =  os.path.join(dir_main, "archieved_files/scraped_ads/radar_scraped_ads")
                file_name = os.path.join(ads_folder,f"{ads['Id']}.json")
                with open(file_name, 'w', encoding='utf-8') as file:
                    json.dump(ads, file, ensure_ascii=False, indent=4)
                logger.info('radar ads downloaded successfully')

        


            
            
            
        else:
            print(f'Error fetching data: {response.status_code}')

        
        

    except:
        logger.exception('CAN NOT  DOWNLOAD RADAR ADS!\nERORR:')

    time.sleep(5)
