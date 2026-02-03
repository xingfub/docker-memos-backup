```
参考
services:
  memos:
    image: neosmemo/memos:stable
    container_name: memos
    restart: always
    networks:
      - memos_network
    volumes:
      - ./memos/:/var/opt/memos
    ports:
      - "5230:5230"
    environment:
      - MEMOS_DRIVER=mysql
      - MEMOS_DSN=账号:密码@tcp(IP地址:3306)/数据库名
      - TZ=Asia/Shanghai
 
networks:
  memos_network:
    driver: bridge

```


MEMOS_DRIVER=mysql
MEMOS_DSN=root:VQo9u08smD6inSx52ZedW7OP1hAL3k4T@tcp(mysql.zeabur.internal:3306)/memos?charset=utf8mb4&parseTime=True&loc=Local

公网 sjc1.clusters.zeabur.com:20036