# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class GiteePipeline:
    def __init__(self):
        self.connection = pymysql.connect(
            user='root',  # 换上你自己的账密和数据库
            password='123456',
            db='scrapy_demo',
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        table = """
        CREATE TABLE IF NOT EXISTS gitee (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            stars INT NOT NULL,
            href VARCHAR(255) NOT NULL
        )CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        """
        self.cursor.execute(table)
        self.connection.commit()

    def process_item(self, item, spider):
        try:
            sql = "INSERT INTO gitee(name, title, stars, href) VALUES (%s, %s, %s, %s)"
            data = (item['name'], item['title'], item['stars'], item['href'])
            # print(f"Executing SQL: {sql} with data: {data}")
            self.cursor.execute(sql, data)
            self.connection.commit()
        except pymysql.MySQLError as e:
            spider.logger.error(f"Error saving item: {e}")
            print(e)
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()


