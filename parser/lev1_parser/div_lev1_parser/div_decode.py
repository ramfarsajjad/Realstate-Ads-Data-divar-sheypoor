import codecs

def decode_unicode(data):
        if isinstance(data, dict):
            return {key: decode_unicode(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [decode_unicode(item) for item in data]
        elif isinstance(data, str):
            try:
                # ابتدا تلاش کنید به utf-8 دیکد کنید
                return data.encode('latin1').decode('utf-8')
            except UnicodeEncodeError:
                # اگر خطا داشت، از unicode_escape استفاده کنید
                return data.encode('latin1').decode('unicode_escape')
        else:
            return data