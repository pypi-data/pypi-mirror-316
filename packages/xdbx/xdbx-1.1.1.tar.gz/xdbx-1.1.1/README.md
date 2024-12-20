[toc]

## 项目背景

> 目前每次我们存数据库的时候都会有这样的问题，所有的数据在同步。或者说在入库时我们需要写入库的相关代码【day by day】，本着：`DRY - Don't Repeat Yourself(不要重复你自己)`原则于是我想到了我们可以异步及批量数据操作器。

## 项目构想

- 我们只需要关注数据的问题，不用再太多费心操作相关的创建表，修改表相关字段问题

## 项目支持的数据库类型

- [x] MySQL
- [x] SqlServer
- [x] PostgreSQL
- [x] KafKa
- [x] ElasticSearch

## 实现的功能
- [x] 智能创建表和字段
- [x] 批量数据插入操作
- [x] 操作数据同一个表字段不同时，会到表中智能增加字段
- [x] 支持数据库的连接参数重写操作

## 配置文件

在`config.py`文件中配置数据库和消息队列的连接信息。您需要设置如下环境变量：

- `ES_HOST_PORT_LIST`: Elasticsearch的主机和端口列表。
- `KAFKA_HOST`, `KAFKA_PORT`, `KAFKA_TOPIC`: Kafka的主机、端口和主题。
- 数据库相关配置（如SQL Server、PostgreSQL、MySQL）。

## 文件说明

> DBOP(Database Operation)数据库操作相关代码

- x_sqlserver.py文件用来存储处理x_sqlserver数据的管道
- x_mysql.py文件用来存储处理x_mysql数据的管道
- x_kafka.py文件用来存储处理kafka数据的管道
- x_mongo.py文件用来存储处理Mongo数据的管道

## 基本实例

```python
# 导入mysql
from xdbx import x_mysql

# 导入sqlserver
# from xdbx import x_mssql

# 数据库ip
x_mysql.host = '127.0.0.1'
# 数据库端口 【mysql默认为3306】
x_mysql.port = 3306
# 数据库用户名
x_mysql.username = 'root'
# 数据库密码
x_mysql.password = '123456'
# 数据库名【需要先创建好的数据库】
x_mysql.db = 'test'
# 插入一条

x_mysql.insert_one(item={'a': 1, 'b': 2}, table='ceshi_20211229')
# 插入多条
x_mysql.insert_many(items=[{'a': 1, 'b': 2}, {'a': 1, 'b': 2}, {'a': 1, 'b': 2}, {'a': 1, 'b': 2}],
                    table='ceshi_20211229')
```

## 使用方法

### Elasticsearch 交互

使用`XES`类与Elasticsearch进行交互。示例代码如下：

```python
from xdbx import x_es

# 实例化并连接Elasticsearch
es = x_es.connect()

# 执行查询
query_json = '{"query": {"match_all": {}}}'
results = es.query(query_json)

# 将结果写入Excel
es.query(query_json, to_excel=True)
```

### Kafka 交互

> 将Kafka进行了封装,对平时我们爬虫的一些常规数据存储做操作，利用单例模式开发支持多线程操作【加锁】 使用`XKafka`类与Kafka进行交互。示例代码如下：

```python
from xdbx import x_kafka

# 实例化Kafka生产者
kafka_producer = x_kafka._connect()

# 发送消息
message = {'key': 'value'}
kafka_producer.insert(message)
```

### SQL Server 交互

> 将SqlServer进行了封装，会自动智能的去创建一些表和字段相关的东西，会省爬虫开发者一些时间 使用`SqlServerPipeline`类与SQL Server进行交互。示例代码如下：

```python
from xdbx import x_mssql

# 实例化SQL Server管道
sql_server = x_mssql()

# 插入数据
item = {'column1': 'value1', 'column2': 'value2'}
table = 'your_table_name'
sql_server.insert_one(item, table)
```

### PostgreSQL 交互

> 将PostgreSQL进行了封装，会自动智能的去创建一些表和字段相关的东西，会省爬虫开发者一些时间。 使用`PostgrePipeline`类与PostgreSQL进行交互。示例代码如下：

```python
from xdbx import x_pgsql

# 实例化PostgreSQL管道
postgres = x_pgsql()

# 执行SQL查询
sql = 'SELECT * FROM your_table'
results = postgres.find(sql)
```

### MySQL 交互

> 将MySQL进行了封装，会自动智能的去创建一些表和字段相关的东西，会省爬虫开发者一些时间。因为mysql<=5.5版本可能有些创建更新时间不稳定的问题，我已经把相关的代码先暂时不开放，如果有更好的方案我们再优化一下。 使用`MysqlDB`类与MySQL进行交互。示例代码如下：

```python
from xdbx import x_mysql

# 实例化MySQL数据库连接
mysql = x_mysql()

# 执行SQL查询
sql = 'SELECT * FROM your_table'
results = mysql.find(sql)
```

## 错误处理

在使用过程中，如果遇到连接错误或查询错误，请检查配置文件中的连接信息是否正确，并查看日志输出的错误详情。

## 联系我们

如果有任何问题或需要进一步的帮助，请联系我们。


## Q&A

### Q0:解决触发器的问题

> 注：相同数据库中不能有相同的触发器，虽然作用于这个表，但是他的范围是相对于数据库，相当于函数名

![DBEDF650-1E0D-42ff-A3FC-D32E8FF93CD6.png](http://tva1.sinaimg.cn/large/9aec9ebdgy1gxgzmytbhgj21y410ab29.jpg)

### Q1:解决字段名大小写不同判断有误的问题

> 使用字段做对比时全进行转换成小写后再对比
