# Applied-Databases

Final project for the course "Applied Databases", Higher Diploma in Computing for Data Analytics, ATU Galway-Mayo, 2025/2026. 

## About this project

The project is a Python application allowing CRUD functionalities for a Business Fair. With the program, users can access and perform operations to two databases - a MySQL (relational) database, and a Neo4j (Graph) database - in their terminal. 

### Getting started 

The application was developed with Python. The required libraries are listed in [requirements.txt](requirements.txt). To install them:  

    pip install -r requirements.txt

To execute the code, run the following command: 

    python main.py

If the databases are not already imported and saved: 

**MySQL**

- *Open MySQL WorkBench/Database/Connect to Database*. Click *OK*. 
- From the pivot menu, import the database through *Server/Data Import/Import from Self Contained File* and select the path to [appdbproj.sql](db/appdbproj.sql)

**Neo4J**

In terminal, navigate to *Neo4j/bin*. Import the database [appdbprojNeo4j.json](db/appdbprojNeo4j.json) with the command: 

    type *Path_to_Lab7Part1Commands.json* | cypher-shell.bat -u neo4j -p neo4jneo4j --format plain

Make sure username and password are correct (-u and -p). 

### Project Structure

```
project/
├── main.py              # entry point
├── connections.py       # DB connection objects
├── mysql_operations.py  # MySQL helpers + MySQL-only menu actions
├── neo4j_operations.py  # Neo4j tx functions + menu actions using Neo4j
├── menu.py              # display_menu, main loop
├── requirements.txt     # required Python libraries
├── db/
    ├── mysql_schemas.md     # MySQL schema documentation
    ├── appdbproj.sql        # MySQL schema + seed data
    └── appdbprojNeo4j.json  # Neo4j seed data
├── innovation.txt
└── gitLink.txt
```

The project includes different python files to establish the database connections, store MySQL and Neo4j operations, and the application menu. 

It also includes a folder [db](db) with the databases and their schemas. The other files are innovation.pdf and gitLink.txt.
