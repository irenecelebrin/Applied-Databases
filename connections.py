# Connect to the databases

# import required libraries
import pymysql
from neo4j import GraphDatabase

# connect to the MySQL database
conn = pymysql.connect(
    user='root',
    cursorclass=pymysql.cursors.DictCursor,
    password='root',
    host='localhost',
    db='appdbproj',
    port=3306,
)

# connect to the Neo4j database
uri = 'neo4j://localhost:7687'
neo4j_driver = GraphDatabase.driver(uri, auth=('neo4j', 'neo4jneo4j'))
