# Neo4j operations and helper functions 

# import required libraries
from connections import neo4j_driver
# import required MySQL operations
from mysql_operations import attendee_exists, get_attendee_name


# -------- Neo4j transaction functions -------------------

# get connected attendees 
def get_relations(tx, attendee):
    query = 'MATCH(n:Attendee{AttendeeID:$AttendeeID}) - [:CONNECTED_TO]- (n1:Attendee) RETURN n1.AttendeeID as id'
    results = tx.run(query, AttendeeID=attendee)

    relations = []
    for result in results:
        relations.append(result['id'])

    return relations


# create a new attendee node 
def create_attendee_node(tx, attendee_id):
    tx.run('MERGE (n:Attendee {AttendeeID: $attendee_id})', attendee_id=attendee_id)

# create a new connection between two attendees
def create_connection(tx, id1, id2):
    query = 'MATCH (n:Attendee {AttendeeID: $id1}), (n1:Attendee{AttendeeID: $id2})' \
            ' MERGE (n) - [:CONNECTED_TO] -> (n1)'

    tx.run(query, id1=id1, id2=id2)


# ----------- MENU FUNCTIONS ---------------

# view connected attendees (option 4 in the menu)
def view_connected_attendees():
    try:
        # get the attendee id from the user
        attendee_id = int(input('Enter Attendee ID: '))

        # get the connected attendees from the Neo4j database
        with neo4j_driver.session() as session:
            relations = session.execute_read(get_relations, attendee_id)

        # get the attendee name from the MySQL database 
        attendee = get_attendee_name(attendee_id)
        if attendee is not None:
            # print results 
            print(f'Attendee Name: {attendee}')
            print('--------')
            if len(relations) > 0:
                print('These attendees are connected:')
                for relation in relations:
                    relation_name = get_attendee_name(relation)
                    print(f'{relation}\t|\t{relation_name}')
            else:
                print('No connections')

    # handle exceptions
    except ValueError:
        print('*** ERROR *** Invalid Attendee ID')
    except Exception as e:
        print(f'Database error: {e}')


# add a connection between two attendees (option 5 in the menu)
def add_connection():
    # get the attendee ids from the user
    while True:
        id_1 = input('Enter Attendee 1 ID: ').strip()
        id_2 = input('Enter Attendee 2 ID: ').strip()

        # check if the attendee ids are numbers
        if not (id_1.isdigit() and id_2.isdigit()):
            print('*** ERROR *** Attendee IDs must be numbers ')
            continue

        # convert the attendee ids to integers
        attendee_1_id = int(id_1)
        attendee_2_id = int(id_2)

        # check if the attendees exist in the MySQL database
        if not (attendee_exists(attendee_1_id) and attendee_exists(attendee_2_id)):
            print('*** ERROR *** One or both attendees do not exist')
            continue
        # check if the attendees are the same
        if attendee_1_id == attendee_2_id:
            print('*** ERROR *** An attendee cannot connect to him/herself')
            continue

        # get the connected attendees from the Neo4j database
        with neo4j_driver.session() as session:
            relations = session.execute_read(get_relations, attendee_1_id)

        # check if the attendees are already connected
        if attendee_2_id in relations:
            print('*** ERROR *** These attendees are already connected')
            continue

        break

    try:
        # create a new connection between the two attendees in the Neo4j database
        with neo4j_driver.session() as session:
            session.execute_write(create_connection, attendee_1_id, attendee_2_id)
        # print success message
        print(f'Attendee {attendee_1_id} is now connected to Attendee {attendee_2_id}')

    # handle exceptions
    except Exception as e:
        print(f'Database Error: {e}')
