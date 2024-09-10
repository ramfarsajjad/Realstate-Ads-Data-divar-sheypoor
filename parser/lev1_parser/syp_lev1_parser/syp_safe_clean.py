import json 


def data_cleaner(data):
    buffer = dict()
    buffer = data['main'].pop('attributes')
    data['main'].update(buffer)
    spamkeys = ['labels', 'resumeJobRequester', 'carInspection', 'topCategoryId', 'categoryId', 'deliveryPrices', 'phone', 'isPhoneVerified', 'isShopProfile',
                 'isSecurePurchase', 'showInsertRateButton', 'paidTags', 'actions', 'hideChat', 'showAttributesIcon', 'marketingBanner', 'certificate',
                   'position', 'approximatePosition', 'ministryInquiry', 'priceRange', 'showPriceRangeFeedback', 'securePurchaseToman', 'hideContactInfo',
                     'isSecurable' ]
    for spkey in spamkeys:
        data['main'].pop(spkey, None)

    buffer = dict()
    buffer['seller'] = data['main'].pop('seller')
    data['sell_box'] = buffer
    buffer = dict()
    buffer['consultant'] = data['main'].pop('consultant')
    data['sell_box'].update(buffer)
    buffer = dict()
    
    


def image_cleaner(data):

    buffer = []
    for item in data['main']['images']:
        buffer.append(item['source']['desktop'])
    data['main']['IMAGE'] = buffer
    data['main'].pop('images')





def prop_cleaner(data):

    listbuf =[]
    for item in data['main']['attributes']:
        buffer = dict()
        buffer[item['key']] = item['value']
        listbuf.append(buffer)
    data['main']['property'] = listbuf
    data['main'].pop('attributes')
    


def categ_cleaner(data):

    listbuf =[]
    for item in data['main']['breadcrumbs']:
        buffer = dict()
        if item['type'] == 'category':
            if item['subType'] == 1:
                buffer['category_1'] = item['title']
            elif item['subType'] == 2:
                buffer['category_2'] = item['title']
        else:
            buffer[item['type']] = item['title']
        listbuf.append(buffer)
    data['main']['category'] = listbuf
    data['main'].pop('breadcrumbs')
    


