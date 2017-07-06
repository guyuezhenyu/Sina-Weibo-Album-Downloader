#! /usr/bin/python
#coding=utf-8 
import os, threading, requests, math, re, random, time


# Configuration Start
OID = 1005055043530082
COOKIES = "_s_tentry=-; ALF=1530752886; Apache=615134228475.589.1499216815768; SCF=AlhaukV6bGsBATT9pIhRnvJ8iIjXT-_rakNHghRXVAgA3vn9416YHMaOX9d-dxtU6k4SiY7TQRibSMCywkU9V1w.; SINAGLOBAL=2121825392574.679.1497883210661; SSOLoginState=1499216887; SUB=_2A250WEuoDeRhGeNK7VQX8C7MzD2IHXVXLDpgrDV8PUNbmtBeLVHBkW9Ck-1mYuDvJBs6oUb5o0QMZ0mbLw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5.3GcNdOs6pTGo3SUVrwQ25JpX5KMhUgL.Fo-XSoqceh57S022dJLoIpzLxK.L1KMLB.zLxKML12BL1-et; SUHB=0laFjnwxMCyYjR; ULV=1499216815793:14:3:2:615134228475.589.1499216815768:1499164333276; UM_distinctid=15ce3c18c52933-09e0587e252c55-38750f56-100200-15ce3c18c58b1e; UOR=www.xilinjie.com,widget.weibo.com,www.bing.com; wvr=6; YF-Page-G0=140ad66ad7317901fc818d7fd7743564; YF-Ugrow-G0=8751d9166f7676afdce9885c6d31cd61; YF-V5-G0=69afb7c26160eb8b724e8855d7b705c6;" 
CRAWL_PHOTOS_NUMBER = 130
# Configuration END


COOKIES = dict((l.split('=') for l in COOKIES.split('; ')))
#先创建保存图片的目录
SAVE_PATH="image"+str(OID) + "/"
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
TEMP_LastMid = ""

def save_image(image_name):
    #if not os.path.isfile(SAVE_PATH + image_name):
    sina_image_url = 'http://ww1.sinaimg.cn/large/' + image_name
    response = requests.get(sina_image_url, stream=True)
    image = response.content
    try:
        print(image_name)
        with open(SAVE_PATH+image_name,"wb") as image_object:
            image_object.write(image)
            return
    except IOError:
        print("IO Error\n")
        return
    finally:
        image_object.close



def get_album_photos_url(page):
    global TEMP_LastMid
    data={
        'ajwvr':6,
        'filter':'wbphoto|||v6',
        'page': page,
        'count':20,
        'module_id':'profile_photo',
        'oid':OID,
        'uid':'',
        'lastMid':TEMP_LastMid,
        'lang':'zh-cn',
        '_t':1,
        'callback':'STK_' + str(random.randint(10000000000000, 900000000000000))
    }
    #print(data)
    #print(COOKIES)
    album_request_result = requests.get('http://photo.weibo.com/page/waterfall',  params = data, cookies = COOKIES).text
    #print(album_request.headers)
    TEMP_LastMid = re.compile(r'"lastMid":"(\d+)"').findall(album_request_result)
    print(TEMP_LastMid)
    return (re.compile(r'(\w+.png|\w+.gif|\w+.jpg)').findall(album_request_result))

if __name__ == '__main__':
#   for i in range(1, int(math.ceil(CRAWL_PHOTOS_NUMBER / 20.0))):
#       threads = []
#       for image_name in get_album_photos_url(i):
#           #save_image(image_name);
#           threads.append(threading.Thread(target=save_image, args=(image_name,)))
#       for t in threads:
#           #t.setDaemon(True)
#           t.start()
    url_file = open(SAVE_PATH + 'list',"w")
    for i in range(1, int(math.ceil(CRAWL_PHOTOS_NUMBER / 20.0))):
        for image_name in get_album_photos_url(i):
            url_file.write('http://ww1.sinaimg.cn/large/' + image_name +'\n')
            time.sleep(2)
    url_file.close()
