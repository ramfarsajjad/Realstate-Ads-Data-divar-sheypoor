def decnum(data, obj):
    coun = 0
    for item in data['sections']:
        if obj in item:
            return coun
        coun += 1

    return None    