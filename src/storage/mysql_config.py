"""
file:mysql_config.py change to your db config
"""
db_config = {
    'local': {
        'host': "10.95.130.118", 'port': 8899,
        'user': "root", 'passwd': "123456",
        'db': "marry", 'charset': "utf8",
    },
    'product': {
        'host': "192.168.0.245", 'port': 3306,
        'user': "root", 'passwd': "****",
        'db': "poi_relation", 'charset': "utf8",
    },
}