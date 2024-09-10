import requests
import json
from pprint import pprint
import csv
import os
import time
import logging

    
# URL API

def div_sc():
    
    dir_main = os.path.dirname(os.path.abspath(__name__))

    dir_log = os.path.join(dir_main, 'logs')
    log_file = os.path.join(dir_log, 'div_sc_log.log')
    logging.basicConfig(
        level=logging.INFO,  # تنظیم سطح لاگ (می‌توانید به دلخواه تغییر دهید)
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()]  # ذخیره لاگ در فایل و نمایش در کنسول
    )

    logger = logging.getLogger(__name__)

    try:
        url = 'https://api.divar.ir/v8/postlist/w/search'
    # pgnum = int(input("enter yout page numger: "))

        payload = {"city_ids":["853","759","760","5","852","761","762","763","764","10","859","765","766","767","857",
                        "768","858","856","769","792","770","17","771","772","1741","1743","773","1742","1737",
                        "1723","4","1747","1727","1750","1724","1725","1744","849","1745","1746","30","848","1749",
                        "1748","31","1722","1721","1739","1740","850","1751","2","1738","1720","1753","1752","774",
                        "1754","778","1756","779","780","25","1757","1755","775","32","776","777","1823","1709","1715",
                        "1714","29","1764","1707","1768","1760","1767","1766","781","1","1718","782","783","1765","1769",
                        "1763","1713","1717","1759","1712","1710","1716","1772","1770","1758","1761","1708","1719","1706",
                        "1771","784","1711","1762","785","1833","36","786","787","34","788","789","790","1735","1729","791",
                        "1776","1732","1736","316","1775","1774","1733","1777","1773","847","3","1778","318","793","794","39",
                        "795","24","1779","796","7","797","798","37","314","1782","1784","799","23","1781","800","756","1780",
                        "754","602","317","1783","802","803","20","804","805","35","707","806","807","747","1785","706","11","1787",
                        "865","1786","851","1728","808","1793","809","1791","6","810","1789","1734","1790","1730","1731","1788","1792",
                        "1794","1726","869","1795","872","811","1796","19","873","8","662","868","1798","812","28","813","1797","814",
                        "1804","1805","1807","815","816","817","867","818","13","1803","1806","819","1801","820","854","855","1800",
                        "9","821","1802","1799","874","822","1808","38","1691","748","2010","1991","2013","751","1973","2008","1981",
                        "1980","1975","1984","1979","1968","1966","2003","2006","1972","823","1996","1970","2012","750","1692","1832",
                        "21","1986","749","743","1974","1999","1693","1976","1990","1985","2002","824","825","1852","1812","2004","1688",
                        "1854","708","1841","2011","829","1855","2007","1850","864","1686","1844","1847","1689","1809","1814","1851",
                        "1839","1835","12","1684","1810","1849","826","1683","1811","861","1994","1813","1845","827","2000","1983","860",
                        "863","1840","1843","1687","1846","746","1690","828","1836","1842","1837","1848","862","1815","1853","1834","1969",
                        "870","1816","830","26","1817","27","752","831","753","1995","1993","1871","663","1987","1988","1703","1701","1978",
                        "664","710","1873","832","1865","1965","1702","1997","833","834","835","1694","2005","1861","1868","1992","1967","745",
                        "1860","1698","1872","1982","1859","22","1700","1699","1862","1863","1989","1998","1697","1819","836","1875","665",
                        "1858","2001","1695","1696","1870","1869","1864","1866","1876","1856","1971","837","1867","1874","1818","838","744","709",
                        "1977","2009","15","839","1824","671","1825","840","1826","18","1822","1820","660","33","841","1821","842","1828","866",
                        "1827","843","844","14","846","1829","1831","871","1830","845","16"],
                        # "pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":"2024-08-07T13:47:02.642959Z",
                        #                     "page":1,"layer_page":1,"search_uid":"a5dd0011-acc6-48d8-a96f-4fdf12a1c5df"},
                                            "search_data":{"form_data":{"data":{"category":{"str":{"value":"real-estate"}},"sort":{"str":{"value":"sort_date"}}}}}}

        # ارسال درخواست GET به URL مشخص شده
        response = requests.post(url, json= payload)

        # بررسی وضعیت پاسخ
        if response.status_code == 200:
            # تبدیل داده‌های دریافتی به فرمت JSON
            data = response.json()
            # چاپ داده‌ها
            # pprint(data)/home/sjd/Desktop/Realstate-Ads-Data-divar-sheypoor-/sc_ads/
            api_dir = os.path.join(dir_main, "archieved_files/api_firstpage/div_api_firstpage")
            all_api_files_and_dirs = os.listdir(api_dir)
            all_api_files = [f for f in all_api_files_and_dirs if os.path.isfile(os.path.join(api_dir, f))]
            api_name = os.path.join(api_dir, f"apidiv{len(all_api_files)}.json")
            try:
                with open(api_name, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
            except Exception as e:
                print(e)


            dir_tokfile = os.path.join(dir_main, 'scraper')
            myfile = os.path.join(dir_tokfile, "div_tokbase.json")
            if os.path.isfile(myfile):
                print(f"{myfile} exists.")
                with open(myfile, 'r') as file:
                    tokcell = json.load(file)
                    bdata = set(tokcell)
            else:
                print(f"{myfile} is not exists. created a new one")
                bdata = set()


            newtok = set(data["action_log"]["server_side_info"]["info"]["tokens"])
            bdata.update(newtok)

            setdata_list = list(bdata)

            # f = open('a1.json', "a+")
            # f.write(json.dumps(data))
            # f.close()

            f = open(myfile , "w")
            f.write(json.dumps(setdata_list))
            f.close()


            logger.info('div tokens downloaded successfully')
            
            
        else:
            logger.exception(f'Error fetching data: {response.status_code}\nERORR:')

        
        

    except:
        logger.exception('CAN NOT  DOWNLOAD DIV TOKENS!\nERORR:')

    
