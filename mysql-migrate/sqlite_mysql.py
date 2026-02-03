import sqlite3
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

class SQLiteToMySQL:
    def __init__(self, sqlite_db_path, mysql_config):
        """
        初始化SQLite到MySQL迁移工具
        
        Args:
            sqlite_db_path (str): SQLite数据库文件路径
            mysql_config (dict): MySQL连接配置
        """
        self.sqlite_db_path = sqlite_db_path
        self.mysql_config = mysql_config
        self.sqlite_conn = None
        self.mysql_conn = None
        self.mysql_cursor = None
    
    def connect_sqlite(self):
        """
        连接到SQLite数据库
        
        Returns:
            bool: 连接成功返回True，失败返回False
        """
        try:
            self.sqlite_conn = sqlite3.connect(self.sqlite_db_path)
            print(f"成功连接到SQLite数据库: {self.sqlite_db_path}")
            return True
        except Exception as e:
            print(f"SQLite连接失败: {str(e)}")
            return False
    
    def connect_mysql(self):
        """
        连接到MySQL数据库
        
        Returns:
            bool: 连接成功返回True，失败返回False
        """
        try:
            self.mysql_conn = mysql.connector.connect(
                host=self.mysql_config['host'],
                port=self.mysql_config['port'],
                user=self.mysql_config['user'],
                password=self.mysql_config['password'],
                database=self.mysql_config['database']
            )
            if self.mysql_conn.is_connected():
                self.mysql_cursor = self.mysql_conn.cursor()
                print(f"成功连接到MySQL数据库: {self.mysql_config['host']}:{self.mysql_config['port']}/{self.mysql_config['database']}")
                return True
            return False
        except Error as e:
            print(f"MySQL连接失败: {str(e)}")
            return False

    def migrate_user_table(self):
        """
        迁移user表数据从SQLite到MySQL
        
        Returns:
            int: 迁移的记录数
        """
        if not self.sqlite_conn or not self.mysql_conn:
            print("数据库未连接，请先调用connect方法")
            return 0
        
        try:
            # 2. 读取SQLite中的user表数据
            sqlite_cursor = self.sqlite_conn.cursor()
            select_sql = "SELECT id, created_ts, updated_ts, row_status, username, role, email, nickname, password_hash, avatar_url, description FROM user"
            sqlite_cursor.execute(select_sql)
            user_data = sqlite_cursor.fetchall()
            sqlite_cursor.close()
            
            print(f"从SQLite中读取到 {len(user_data)} 条user记录")
            
            if not user_data:
                print("SQLite中没有user数据，迁移结束")
                return 0
            
            # 3. 获取SQLite表结构，确定列名
            cursor = self.sqlite_conn.cursor()
            cursor.execute("PRAGMA table_info(user)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            cursor.close()
            
            # 4. 插入数据到MySQL
            inserted_count = 0
            sql = """
            INSERT INTO user 
            (id, created_ts, updated_ts, row_status, username, role, 
            email, nickname, password_hash, avatar_url, description) 
            VALUES 
            (%(id)s, %(created_ts)s,
             %(updated_ts)s, %(row_status)s, %(username)s, %(role)s, 
             %(email)s, %(nickname)s, %(password_hash)s, %(avatar_url)s, %(description)s)
            """
           
            print("开始迁移user数据到MySQL...")
            
            for row in user_data:
                print(row)
                data = {
                    'id': row[0],
                    'created_ts': datetime.fromtimestamp(row[1]),
                    'updated_ts': datetime.fromtimestamp(row[2]),
                    'row_status': row[3],
                    'username': row[4],
                    'role': row[5],
                    'email': row[6],
                    'nickname': row[7],
                    'password_hash': row[8],
                    'avatar_url': row[9],
                    'description': row[10]
                }
                try:
                    self.mysql_cursor.execute(sql, data)
                    inserted_count += 1
                    # 每10条记录提交一次
                    if inserted_count % 10 == 0:
                        self.mysql_conn.commit()
                        print(f"已迁移 {inserted_count} 条记录")
                except Exception as e:
                    print(f"插入记录失败: {str(e)}")
                    print(f"记录数据: {row}")
            # 提交剩余的记录
            self.mysql_conn.commit()
            print(f"user表数据迁移完成，共迁移 {inserted_count} 条记录")
            
            return inserted_count
            
        except Exception as e:
            print(f"迁移user表失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return 0
    

             
    def migrate_memos_table(self):
        """
        迁移user表数据从SQLite到MySQL
        
        Returns:
            int: 迁移的记录数
        """
        if not self.sqlite_conn or not self.mysql_conn:
            print("数据库未连接，请先调用connect方法")
            return 0
        
        try:
            # 2. 读取SQLite中的user表数据
            sqlite_cursor = self.sqlite_conn.cursor()
            select_sql = """SELECT id, uid ,creator_id ,created_ts, updated_ts ,row_status,content,
                        visibility,pinned,payload FROM memo"""
            sqlite_cursor.execute(select_sql)
            user_data = sqlite_cursor.fetchall()
            sqlite_cursor.close()
            
            print(f"从SQLite中读取到 {len(user_data)} 条user记录")
            
            if not user_data:
                print("SQLite中没有user数据，迁移结束")
                return 0
            
            # 4. 插入数据到MySQL
            inserted_count = 0
            sql = """
            INSERT INTO memo
            ( id, uid ,creator_id ,created_ts, updated_ts ,row_status,content,visibility,pinned,payload) 
            VALUES 
            (%(id)s, %(uid)s, %(creator_id)s, %(created_ts)s, %(updated_ts)s, %(row_status)s, %(content)s,
             %(visibility)s, %(pinned)s, %(payload)s)
            """
           
            print("开始迁移user数据到MySQL...")
            
            for row in user_data:
                print(row)
                data = {
                    'id': row[0],
                    'uid': row[1],
                    'creator_id': row[2],
                    'created_ts': datetime.fromtimestamp(row[3]),
                    'updated_ts': datetime.fromtimestamp(row[4]),
                    'row_status': row[5],
                    'content': row[6],
                    'visibility': row[7],
                    'pinned': row[8],
                    'payload': row[9]
                }
                try:
                    self.mysql_cursor.execute(sql, data)
                    inserted_count += 1
                    # 每10条记录提交一次
                    if inserted_count % 10 == 0:
                        self.mysql_conn.commit()
                        print(f"已迁移 {inserted_count} 条记录")
                except Exception as e:
                    print(f"插入记录失败: {str(e)}")
                    print(f"记录数据: {row}")
            # 提交剩余的记录
            self.mysql_conn.commit()
            print(f"user表数据迁移完成，共迁移 {inserted_count} 条记录")
            
            return inserted_count
            
        except Exception as e:
            print(f"迁移user表失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return 0
    

    def close(self):
        """
        关闭数据库连接
        """
        try:
            if self.sqlite_conn:
                self.sqlite_conn.close()
                print("SQLite连接已关闭")
            if self.mysql_cursor:
                self.mysql_cursor.close()
            if self.mysql_conn and self.mysql_conn.is_connected():
                self.mysql_conn.close()
                print("MySQL连接已关闭")
        except Exception as e:
            print(f"关闭连接失败: {str(e)}")

# 使用示例
if __name__ == "__main__":
    # 配置SQLite数据库路径
    sqlite_db_path = "../20260201-0422/memos_prod.db"
    
    # 配置MySQL连接信息
    mysql_config = {
        'host': os.environ.get('MYSQL_HOST', 'sjc1.clusters.zeabur.com'),
        'port': int(os.environ.get('MYSQL_PORT', '20036')),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', 'VQo9u08smD6inSx52ZedW7OP1hAL3k4T'),
        'database': os.environ.get('MYSQL_DATABASE', 'memos2')
    }
    
    print(f"SQLite数据库路径: {sqlite_db_path}")
    print(f"MySQL配置: {mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}")
    
    # 创建迁移工具
    migrator = SQLiteToMySQL(
        sqlite_db_path=sqlite_db_path,
        mysql_config=mysql_config
    )
    
    try:
        # 连接数据库
        if migrator.connect_sqlite() and migrator.connect_mysql():
            # 迁移user表
            print("开始迁移memo表...")
            # migrator.migrate_user_table()
            migrator.migrate_memos_table()
    finally:
        # 关闭连接
        migrator.close()
