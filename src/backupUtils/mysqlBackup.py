import pymysql
import os
from datetime import datetime

def export_mysql_to_sql(output_file="mysql_export.sql"):
    """
    导出 MySQL 数据库所有表到单个 SQL 文件（包含结构+数据）
    :param host: 数据库主机地址
    :param port: 端口号
    :param user: 数据库用户名
    :param password: 数据库密码
    :param db_name: 要导出的数据库名
    :param output_file: 输出的 SQL 文件路径
    """
    host = "sjc1.clusters.zeabur.com"
    port = 20036
    user = "root"
    password = "VQo9u08smD6inSx52ZedW7OP1hAL3k4T"
    db_name = "memos2"
    # 1. 连接 MySQL 数据库
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            charset="utf8mb4",  # 兼容中文和特殊字符
            cursorclass=pymysql.cursors.DictCursor  # 返回字典格式的结果
        )
        cursor = conn.cursor()
        print(f"✅ 成功连接到 MySQL 数据库: {db_name}")

        # 2. 获取数据库中所有表名
        cursor.execute("SHOW TABLES")
        tables = [table[f"Tables_in_{db_name}"] for table in cursor.fetchall()]
        if not tables:
            print("⚠️ 数据库中无表可导出")
            return

        # 3. 打开 SQL 文件，准备写入（覆盖已有文件，编码为 utf8）
        with open(output_file, "w", encoding="utf8") as f:
            # 写入文件头（可选，标注导出时间）
            f.write(f"-- MySQL 数据库导出文件\n")
            f.write(f"-- 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- 数据库名: {db_name}\n")
            f.write("SET NAMES utf8mb4;\n")
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

            # 4. 遍历每个表，导出结构+数据
            for table in tables:
                print(f"🔄 正在导出表: {table}")

                # 4.1 导出表结构（CREATE TABLE 语句）
                cursor.execute(f"SHOW CREATE TABLE `{table}`")
                create_table_sql = cursor.fetchone()["Create Table"]
                f.write(f"-- ----------------------------\n")
                f.write(f"-- 表结构: {table}\n")
                f.write(f"-- ----------------------------\n")
                f.write(f"DROP TABLE IF EXISTS `{table}`;\n")  # 避免导入时表已存在
                f.write(f"{create_table_sql};\n\n")

                # 4.2 导出表数据（INSERT INTO 语句）
                cursor.execute(f"SELECT * FROM `{table}`")
                rows = cursor.fetchall()
                if not rows:
                    f.write(f"-- 表 {table} 无数据\n\n")
                    continue

                # 获取表的所有列名
                columns = [desc[0] for desc in cursor.description]
                columns_str = ", ".join([f"`{col}`" for col in columns])

                # 拼接 INSERT 语句（批量插入，提升效率）
                f.write(f"-- 表 {table} 数据\n")
                f.write(f"INSERT INTO `{table}` ({columns_str}) VALUES\n")

                # 处理每一行数据（转义特殊字符，适配 MySQL 格式）
                values_list = []
                for row in rows:
                    values = []
                    for col in columns:
                        val = row[col]
                        if val is None:
                            values.append("NULL")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, datetime):
                            # 时间类型转为 MySQL 兼容格式
                            values.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
                        else:
                            # 字符串转义（单引号、换行符等）
                            val_str = str(val).replace("'", "\\'").replace("\n", "\\n")
                            values.append(f"'{val_str}'")
                    values_str = ", ".join(values)
                    values_list.append(f"({values_str})")

                # 拼接所有行，最后一行用分号，其余用逗号
                f.write(",\n".join(values_list))
                f.write(";\n\n")

            # 写入文件尾
            f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
            print(f"✅ 导出完成！SQL 文件路径: {os.path.abspath(output_file)}")

    except Exception as e:
        print(f"❌ 导出失败: {str(e)}")
    finally:
        # 确保关闭数据库连接
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()

def downFileMySql():
    print("1.downFileMySql")
    output_file="../sqlback/mysql_all_tables.sql"
    export_mysql_to_sql(output_file)
    return output_file
# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 替换为你的 MySQL 连接信息
   downFileMySql()