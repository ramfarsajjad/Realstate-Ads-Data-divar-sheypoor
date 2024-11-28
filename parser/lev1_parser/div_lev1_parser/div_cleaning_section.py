from div_secfind import dicfdr
from div_desireitem import deslis

def section_cleaner(data, seckey):
    des_list = data
    if seckey == "MAP":
        if bool(dicfdr(data, "section_name", seckey)):
            des_num1 = deslis(data, "section_name", seckey)
            if bool(dicfdr(data[des_num1]['widgets'], "widget_type",  "MAP_ROW")):
                des_num2 = deslis(data[des_num1]['widgets'], "widget_type",  "MAP_ROW")
                data[des_num1]['widgets'][des_num2]['data'].pop('@type', None)
                data[des_num1]['widgets'][des_num2]['data'].pop('image_url', None)
            data[des_num1]['location'] = data[des_num1]['widgets'][des_num2]['data'].pop('location')
            data[des_num1].pop('widgets')
                
    elif seckey == "IMAGE":
        if bool(dicfdr(data, "section_name", seckey)):
            des_num1 = deslis(data, "section_name", seckey)
            if bool(dicfdr(data[des_num1]['widgets'], "widget_type",  "IMAGE_CAROUSEL")):
                des_num2 = deslis(data[des_num1]['widgets'], "widget_type",  "IMAGE_CAROUSEL")
                try:
                    data[des_num1]['widgets'][des_num2]['data'].pop('@type', None)
                    data[des_num1]['widgets'][des_num2]['data'].pop('image_aspect_ratio', None)
                    data[des_num1]['widgets'][des_num2]['data'].pop('has_preview', None)
                    data[des_num1]['widgets'][des_num2]['data'].pop('has_thumbnails', None)
                    for i in data[des_num1]['widgets'][des_num2]['data']['items']:
                        i['image'].pop('alt', None)
                        i['image'].pop('thumbnail_url', None)

                    data[des_num1]['images'] = data[des_num1]['widgets'][des_num2]['data'].pop('items')
                    data[des_num1].pop('widgets')
                except:
                    pass

    elif seckey == "BUSINESS_SECTION":
        if bool(dicfdr(data, "section_name", seckey)):
            des_num1 = deslis(data, "section_name", seckey)
            if bool(dicfdr(data, "section_name", seckey)):
                des_num2 = deslis(data[des_num1]['widgets'], "widget_type",  "EVENT_ROW")
                if des_num2 == None:
                    des_num2 = deslis(data[des_num1]['widgets'], "widget_type",  "LAZY_SECTION")
                try:
                    data[des_num1]['widgets'][des_num2]['data'].pop('@type')
                    data[des_num1]['widgets'][des_num2]['data'].pop('subtitle')
                    data[des_num1]['widgets'][des_num2]['data'].pop('type')
                    data[des_num1]['widgets'][des_num2]['data'].pop('last_notification_time')
                except:
                    pass
                


def section_basic_clean(data):
    if bool(dicfdr(data, "section_name", "TITLE")):
        des_num1 = deslis(data, "section_name", "TITLE")
        data.pop(des_num1)
    if bool(dicfdr(data, "section_name", "NOTE")):
        des_num1 = deslis(data, "section_name", "NOTE")
        data.pop(des_num1)
    if bool(dicfdr(data, "section_name", "INSPECTION")):
        des_num1 = deslis(data, "section_name", "INSPECTION")
        data.pop(des_num1)    
    if bool(dicfdr(data, "section_name", "DESCRIPTION")):
        des_num1 = deslis(data, "section_name", "DESCRIPTION")
        data.pop(des_num1)
    if bool(dicfdr(data, "section_name", "STATIC")):
        des_num1 = deslis(data, "section_name", "STATIC")
        data.pop(des_num1)
    if bool(dicfdr(data, "section_name", "TAGS")):
        des_num1 = deslis(data, "section_name", "TAGS")
        data.pop(des_num1)
    if bool(dicfdr(data, "section_name", "BREADCRUMB")):
        des_num1 = deslis(data, "section_name", "BREADCRUMB")
        data.pop(des_num1)        
    if bool(dicfdr(data, "section_name", "SUGGESTION")):
        des_num1 = deslis(data, "section_name", "SUGGESTION")
        data.pop(des_num1)




def listdata_basic_clean(data):
    if bool(dicfdr(data, "section_name", "LIST_DATA")):
        des_num1 = deslis(data, "section_name", "LIST_DATA")
        if 'widgets' in data[des_num1]:
            coun = 0
            spam = []
            for index in data[des_num1]['widgets']:
                if 'widget_type' in index:
                    if index['widget_type'] == 'UNEXPANDABLE_ROW':
                        # data[des_num1]['widgets'].pop(coun)
                        spam.append(coun)
                    elif index['widget_type'] == 'SECTION_TITLE_ROW':
                        spam.append(coun)
                    elif index['widget_type'] == 'FEATURE_ROW':
                        spam.append(coun)
                    elif index['widget_type'] == 'RENT_SLIDER':
                        spam.append(coun)

                    coun +=1
            for i in reversed(spam):
                        data[des_num1]['widgets'].pop(i)


            if bool(dicfdr(data[des_num1]['widgets'], "widget_type", "GROUP_INFO_ROW")):
                des_num2 = deslis(data[des_num1]['widgets'], "widget_type", "GROUP_INFO_ROW")
                data[des_num1]['widgets'][des_num2]['data'].pop('@type', None)
                data[des_num1]['widgets'][des_num2]['data'].pop('has_divider', None)
                data[des_num1]['widgets'][des_num2]['items'] = data[des_num1]['widgets'][des_num2]['data'].pop('items')
                data[des_num1]['widgets'][des_num2].pop('data')

            if bool(dicfdr(data[des_num1]['widgets'], "widget_type", "GROUP_FEATURE_ROW")):
                des_num2 = deslis(data[des_num1]['widgets'], "widget_type", "GROUP_FEATURE_ROW")
                data[des_num1]['widgets'][des_num2]['data'].pop('@type', None)
                data[des_num1]['widgets'][des_num2]['data'].pop('action_text', None)
                data[des_num1]['widgets'][des_num2]['data'].pop('has_divider', None)
                if 'action' in data[des_num1]['widgets'][des_num2]['data']:
                    data[des_num1]['widgets'][des_num2]['data']['action'].pop('type', None) 
                   
                    ckno = 0
                    for no, index in enumerate(reversed(data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'])):
                        if 'widget_type' in index:
                            if ckno == 0:
                                initlen = len(data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'])
                                ckno += 1
                            rno = initlen - no -1    
                            if index['widget_type'] == 'UNEXPANDABLE_ROW':
                                data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'][rno]['data'].pop('@type', None)
                                data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'][rno]['data'].pop('has_divider', None)
                                data[des_num1]['widgets'][des_num2]['data']['items'].append(data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'][rno]['data'])
                            elif index['widget_type'] == 'FEATURE_ROW':
                                data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'][rno]['data'].pop('@type', None)
                                if 'has_divider' in data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'][rno]['data']:
                                    data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'][rno]['data'].pop('has_divider', None)
                                data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'][rno]['data'].pop('icon', None)

                            elif index['widget_type'] == 'TITLE_ROW':
                                data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page']['widget_list'].pop(rno)

                    data[des_num1]['widgets'][des_num2]['possibilty'] = data[des_num1]['widgets'][des_num2]['data']['action']['payload']['modal_page'].pop('widget_list')       
                    
                    

                if 'items' in data[des_num1]['widgets'][des_num2]['data']:
                    ckno = 0
                    for no, val in enumerate(reversed(data[des_num1]['widgets'][des_num2]['data']['items'])):
                        if ckno == 0:
                            initlen = len(data[des_num1]['widgets'][des_num2]['data']['items'])
                            ckno += 1
                        rno = initlen - no -1
                        data[des_num1]['widgets'][des_num2]['data']['items'][rno].pop('icon', None)
                    data[des_num1]['widgets'][des_num2]['option'] =  data[des_num1]['widgets'][des_num2]['data'].pop('items')
                    data[des_num1]['widgets'][des_num2].pop('data')

                            


                


                    