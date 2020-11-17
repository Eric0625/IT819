import re
import time
import requests
import pymysql
import logging
import random

# mysql 数据库链接信息
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Dandpak2020'
DB_NAME = 'mafengwo'
timeOut = 25
maxSleepTime = 20
#评论内容所在的url，？后面是get请求需要的参数内容
comment_url='http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?'
comment_url2="http://www.mafengwo.cn/gonglve/ajax.php?"
commentCategoryName = {
    11: '差评',
    12: '中评',
    13: '好评'
}

class PoiComments:
    def __init__(self):
        self.date_list = []
        self.star_list = []
        self.user_list = []

def getPoiComments():
    #获取poi列表
    # 连接数据库
    connection = pymysql.connect(
        DB_HOST,
        DB_USER,
        DB_PASSWORD,
        DB_NAME)
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT `poi_id`, `name` FROM `poi`')
            result = cursor.fetchone()
            while result:
                poiId = str(result[0])
                startTime = int(time.time())
                #在评论表里读取该地点，如果有则跳过
                commentConn = pymysql.connect(
                                DB_HOST,
                                DB_USER,
                                DB_PASSWORD,
                                DB_NAME)
                with commentConn.cursor() as commentCursor:
                    commentCursor.execute('SELECT `poi_id` FROM `poi_ratings` WHERE `poi_id`='+poiId)
                    commentPoiResult = commentCursor.fetchall()
                    if len(commentPoiResult) != 0:
                        result = cursor.fetchone()
                        continue
                commentConn.close()
                poiName = result[1]
                poiCommentsTotalEntity = PoiComments()
                ret = getFirstTypeComment(poiId, poiCommentsTotalEntity)
                if ret == -1:
                    msg = "***poi:{}的评论没找到，转向第二版本评论***".format(poiId)
                    logging.info(msg)
                    print(msg)
                    ret = getSecondTypeComment(poiId, poiCommentsTotalEntity)
                    if ret == -1:
                        #两个地方都找不到
                        msg = "===poi:{}的评论没找到===".format(poiId)
                        logging.info(msg)
                        print(msg)
                        result = cursor.fetchone()
                        continue
                endTime = int(time.time())
                msg = '爬取'+poiId+'完毕，花费'+str(endTime-startTime)+'秒，爬取了{}个评论'.format(
                        len(poiCommentsTotalEntity.date_list))
                print(msg)
                logging.info(msg)
                #写入数据库
                writeCon = pymysql.connect(
                            DB_HOST,
                            DB_USER,
                            DB_PASSWORD,
                            DB_NAME)
                try:
                    totalCommentNum = len(poiCommentsTotalEntity.user_list)
                    with writeCon.cursor() as wcursor:
                        sql = "INSERT IGNORE INTO poi_ratings(created_time, poi_id, poi_name, user_id, rating, comment_time) \
                            VALUES (%s, %s, %s, %s, %s, %s);"
                        params = []
                        for index in range(0, totalCommentNum):
                            params.append((time.strftime('%Y-%m-%d %H:%M:%S'),
                            poiId, poiName, 
                            poiCommentsTotalEntity.user_list[index],
                            poiCommentsTotalEntity.star_list[index],
                            poiCommentsTotalEntity.date_list[index]
                            ))
                        wcursor.executemany(sql, params)
                        writeCon.commit()
                except Exception as e:
                    print(e)
                    logging.error(e)
                    writeCon.rollback()
                finally:
                    writeCon.close()
                result = cursor.fetchone()
    except Exception as e:
        logging.error(e)
        # 如果发生错误则回滚
        connection.rollback()
    finally:
        connection.close()

def getFirstTypeComment(poiId, entity):
    for commentCategory in [11, 12, 13]:
        pageIndex = 1
        subEntity = PoiComments()
        sleepTime = 0.3 + random.randint(1, maxSleepTime)/10
        print('开始爬取poi:{}的{}，等待{}秒'.format(
            poiId, 
            commentCategoryName[commentCategory], 
            sleepTime))
        time.sleep(sleepTime)
        total_comment = getComment(poiId, commentCategory, pageIndex, subEntity)
        if total_comment == -1: continue
        msg = '读取poi:{}的{},共{}个评论'.format(
            poiId, 
            commentCategoryName[commentCategory],
            total_comment)
        logging.info(msg)
        print(msg)
        while len(subEntity.date_list) < 75 and len(subEntity.date_list) < total_comment:
            pageIndex += 1
            sleepTime = 0.3 + random.randint(1, maxSleepTime)/10
            print('爬取第{}页，休息{}秒'.format(pageIndex, sleepTime))
            time.sleep(sleepTime)
            ret = getComment(poiId, commentCategory, pageIndex, subEntity)
            if ret == -1:
                break
        entity.user_list += subEntity.user_list
        entity.date_list += subEntity.date_list
        entity.star_list += subEntity.star_list
    if len(entity.user_list) == 0: return -1
    return 0

def getSecondTypeComment(poiId, entity):
    for commentCategory in range(1, 6):
        pageIndex = 1
        subEntity = PoiComments()
        sleepTime = 0.3 + random.randint(1, maxSleepTime)/10
        print('开始爬取poi:{}的{}星评论，等待{}秒'.format(
            poiId, 
            commentCategory,
            sleepTime))
        time.sleep(sleepTime)
        total_comment = getComment2(poiId, commentCategory, pageIndex, subEntity)
        if total_comment == -1: continue
        msg = '读取poi:{}的{}星评论,共{}个评论'.format(
            poiId, 
            commentCategory,
            total_comment)
        logging.info(msg)
        print(msg)
        while len(subEntity.date_list) < 75 and len(subEntity.date_list) < total_comment:
            pageIndex += 1
            sleepTime = 0.3 + random.randint(1, maxSleepTime)/10
            print('爬取第{}页，休息{}秒'.format(pageIndex, sleepTime))
            time.sleep(sleepTime)
            ret = getComment2(poiId, commentCategory, pageIndex, subEntity)
            if ret == -1:
                break
        entity.user_list += subEntity.user_list
        entity.date_list += subEntity.date_list
        entity.star_list += subEntity.star_list
    if len(entity.user_list) == 0: return -1
    return 0

def getComment2(poi_id, category, page_num, entity):
    requests_headers={
    'Referer': 'http://www.mafengwo.cn/poi/' + poi_id + '.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }#请求头
    requests_data={
        "category":str(category),
        "poi_id":poi_id,
        "page":str(page_num),
        "act":"get_poi_comments",
        "ts":str(int(round(time.time() * 1000))),
        "type":"1",
        "order":"0"
        }
    try:
        response =requests.get(url=comment_url2,headers=requests_headers,params=requests_data, timeout=timeOut)
        if 200==response.status_code:
            page = response.content.decode('unicode-escape', 'ignore').encode('utf-8', 'ignore').decode('utf-8')#爬取页面并且解码
            page = page.replace('\\/', '/')#将\/转换成/
            #日期列表
            date_pattern = r'<div class="ar-hd clearfix">.*?<span class="time">(.*?)</span>'
            dateListGroup = re.compile(date_pattern, re.DOTALL).findall(page)
            if len(dateListGroup) == 0:
                return -1
            entity.date_list += dateListGroup
            #星级列表
            star_pattern = r'<span class="rank-star">.*?<span class="star(\d)"></span>'
            entity.star_list += re.compile(star_pattern, re.DOTALL).findall(page)
            #评论列表
            #comment_pattern = r'<p class="rev-txt">([\s\S]*?)</p>'
            #comment_list = re.compile(comment_pattern).findall(page)
            #用户id
            user_pattern = r'<span class="user-avatar"><a href="/u/(.*?).html"'
            entity.user_list += re.compile(user_pattern).findall(page)
            #总评论数
            if page_num == 1:
                total_num_pattern = r'"total":(\d*)'
                total_num = re.compile(total_num_pattern).search(page)
                if total_num:
                    return int(total_num[1])
            return len(entity.star_list)
        else:
            msg = "爬取"+poi_id+"的第"+page+"页失败"
            print(msg)
            logging.info(msg)
    except requests.exceptions.RequestException as e:
        logging.error(e)
        print(e)
        return -1

def getComment(poi_id, category, page_num, entity):
    requests_headers={
    'Referer': 'http://www.mafengwo.cn/poi/' + poi_id + '.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}#请求头
    requests_data={
        'params': '{"poi_id":"' + poi_id + '","type":"1","category":"%d","page":"%d","just_comment":1}' % (category, page_num)   #经过测试只需要用params参数就能爬取内容
        }
    try:
        response =requests.get(url=comment_url,headers=requests_headers,params=requests_data, timeout=timeOut)
        if 200==response.status_code:
            page = response.content.decode('unicode-escape', 'ignore').encode('utf-8', 'ignore').decode('utf-8')#爬取页面并且解码
            page = page.replace('\\/', '/')#将\/转换成/
            #日期列表
            date_pattern = r'<a class="btn-comment _j_comment" title="添加评论">评论</a>.*?\n.*?<span class="time">(.*?)</span>'
            dateListGroup = re.compile(date_pattern).findall(page)
            if len(dateListGroup) == 0:
                return -1
            entity.date_list += dateListGroup
            #星级列表
            star_pattern = r'<span class="s-star s-star(\d)"></span>'
            entity.star_list += re.compile(star_pattern).findall(page)
            #评论列表
            #comment_pattern = r'<p class="rev-txt">([\s\S]*?)</p>'
            #comment_list = re.compile(comment_pattern).findall(page)
            #用户id
            user_pattern = r'<a class="avatar" href="/u/(.*).html" target="_blank">.*</a>'
            entity.user_list += re.compile(user_pattern).findall(page)
            #总评论数
            if page_num == 1:
                total_num_pattern = r'<span class="count">共<span>.*</span>页.*?<span>(.*?)</span>'
                total_num = re.compile(total_num_pattern).search(page)
                if total_num:
                    return int(total_num.group(1))
            return len(entity.star_list)
        else:
            msg = "爬取"+poi_id+"的第"+page+"页失败"
            print(msg)
            logging.info(msg)
            return 0
    except requests.exceptions.RequestException as e:
        logging.error(e)
        print(e)
        return -1

logging.basicConfig(level=logging.INFO,
                            filename='logs/mafengwo_comments.'+str(int(time.time()))+'.log',
                            format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            )
getPoiComments()