import json

def rec_date(data):
    expired = data['unavailable_after'].split('T')
    day = (expired[0].split('-'))[2]
    month = int((expired[0].split('-'))[1]) - 1
    year = (expired[0].split('-'))[0]    
    birthday = f'{day}-{month}-{year}'
    data['register_date'] = birthday
    data.pop('unavailable_after')


