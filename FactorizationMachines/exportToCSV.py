import pymysql
import csv

# mysql 数据库链接信息
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'test'
DB_NAME = 'mafengwo'

connection = pymysql.connect(
        DB_HOST,
        DB_USER,
        DB_PASSWORD,
        DB_NAME)
try:
    with connection.cursor() as cursor, open('PoiRatings1.csv', 'w', newline='', encoding="utf-8") as csvfile :
        csvfile.write('\ufeff')
        csvWriter = csv.writer(csvfile)
        # cursor.execute('SELECT `rating`, `poi_id`, `poi_name`, `user_id`, `comment_time`  FROM `poi_ratings`')
        cursor.execute('SELECT `user_id`, `poi_id`, `rating`, `comment_time`  FROM `poi_ratings`')
        # csvWriter.writerow(['rating', 'poi_id', 'poi_name', 'user_id', 'comment_time'])
        csvWriter.writerow(['user','item','rating','timestamp'])
        poiResult = cursor.fetchone()
        while poiResult:
            csvWriter.writerow(poiResult)
            poiResult = cursor.fetchone()
        csvfile.close()
except Exception as e:
    print(e)
finally:
    connection.close()
print('done')
