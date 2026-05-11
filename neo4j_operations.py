from connections import neo4j_driver
from mysql_operations import attendee_exists, get_attendee_name


# -------- Neo4j transaction functions -------------------

def get_relations(tx, attendee):
    query = 'MATCH(n:Attendee{AttendeeID:$AttendeeID}) - [:CONNECTED_TO]- (n1:Attendee) RETURN n1.AttendeeID as id'
    results = tx.run(query, AttendeeID=attendee)

    relations = []
    for result in results:
        relations.append(result['id'])

    return relations


def create_attendee_node(tx, attendee_id):
    tx.run('MERGE (n:Attendee {AttendeeID: $attendee_id})', attendee_id=attendee_id)


def create_connection(tx, id1, id2):
    query = 'MATCH (n:Attendee {AttendeeID: $id1}), (n1:Attendee{AttendeeID: $id2})' \
            ' MERGE (n) - [:CONNECTED_TO] -> (n1)'

    tx.run(query, id1=id1, id2=id2)


# ----------- MENU FUNCTIONS ---------------

def view_connected_attendees():
    try:
        attendee_id = int(input('Enter Attendee ID: '))

        with neo4j_driver.session() as session:
            relations = session.execute_read(get_relations, attendee_id)

        attendee = get_attendee_name(attendee_id)
        if attendee is not None:
            print(f'Attendee Name: {attendee}')
            print('--------')
            if len(relations) > 0:
                print('These attendees are connected:')
                for relation in relations:
                    relation_name = get_attendee_name(relation)
                    print(f'{relation}\t|\t{relation_name}')
            else:
                print('No connections')

    except ValueError:
        print('*** ERROR *** Invalid Attendee ID')
    except Exception as e:
        print(f'Database error: {e}')


def add_connection():
    while True:
        id_1 = input('Enter Attendee 1 ID: ').strip()
        id_2 = input('Enter Attendee 2 ID: ').strip()

        if not (id_1.isdigit() and id_2.isdigit()):
            print('*** ERROR *** Attendee IDs must be numbers ')
            continue

        attendee_1_id = int(id_1)
        attendee_2_id = int(id_2)

        if not (attendee_exists(attendee_1_id) and attendee_exists(attendee_2_id)):
            print('*** ERROR *** One or both attendees do not exist')
            continue

        if attendee_1_id == attendee_2_id:
            print('*** ERROR *** An attendee cannot connect to him/herself')
            continue

        break

    try:
        with neo4j_driver.session() as session:
            relations = session.execute_read(get_relations, attendee_1_id)
            if attendee_2_id in relations:
                print('*** ERROR *** : These attendees are already connected')
            else:
                with neo4j_driver.session() as session:
                    session.execute_write(create_connection, attendee_1_id, attendee_2_id)

                print(f'Attendee {attendee_1_id} is now connected to {attendee_2_id}')

    except Exception as e:
        print(f'Database Error: {e}')
