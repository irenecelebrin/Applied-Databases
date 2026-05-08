# Applied-Databases

Final project for the Course "Applied Databases", Higher Diploma in Computing for Data Analytics, ATU Galway-Mayo, 2025/2026. 

## About this project

The project is a Python application allowing CRUD functionalities for a Business Fair. Through the program, users can access and perform operations to two databases, a MySQL (relational) database, and a Neo4j (Graph) database. 

### Getting started 

The application was developed with Python. The required libraries are listed in [requirements.txt](requirements.txt). They can be installed with the command: 


    pip install -r requirements.txt


### Project Structure

```
project/
├── main.py              # entry point
├── connections.py       # DB connection objects
├── mysql_operations.py  # MySQL helpers + MySQL-only menu actions
├── neo4j_operations.py  # Neo4j tx functions + menu actions using Neo4j
├── menu.py              # display_menu, get_valid_company_id, main loop
├── requirements.txt     # required Python libraries
├── db/
    ├── mysql_schemas.md     # MySQL schema documentation
    ├── appdbproj.sql        # MySQL schema + seed data
    └── appdbprojNeo4j.json  # Neo4j seed data
├── innovation.txt
└── gitLink.txt
```

The project includes several python files to establish the datababse conections, store MySQL and Neo4j operations, and the application menu. 

It also includes a folder [db](db) with the databases and their schemas. The other files are innovation.txt and gitLink.txt.

