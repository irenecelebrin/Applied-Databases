# Final project for Applied Databases

# import libraries to connect to db
import pymysql
from neo4j import GraphDatabase

## connect to MySQL database.

# connect to database
conn = pymysql.connect(user = 'root', 
                        cursorclass = pymysql.cursors.DictCursor,
                        password = 'root',
                        host = 'localhost',
                        db = 'appdbproj',
                        port = 3306)

'''
test connection 
query ='select attendeeName from attendee'

with conn: 
    cursor = conn.cursor()
    cursor.execute(query)
    attendee_names = cursor.fetchall()

for name in attendee_names:
    print(name['attendeeName'])

'''

# connect to Neo4j 

uri = 'neo4j://localhost:7687'
neo4j_driver = GraphDatabase.driver(uri, auth=('neo4j', 'neo4jneo4j'))

def main():


    # map choice to CRUD operations 
    # now placeholders
    while True:
        display_menu()
        choice = input('Choice: ').strip()
        if choice == '1':
            view_speakers()
        elif choice == '2':
            view_attendees()
        elif choice == '3':
            add_new_attendee()
        elif choice == '4':
            view_connected_attendees()
        elif choice == '5':
            print('5')
        elif choice == '6':
            print(6)
        elif choice == 'x':
            break
        else:
            print('Select a valid option')


#display the menu in the terminal 
def display_menu():

    print('--------')
    print('Conference Management')
    print('')
    print('MENU')
    print('========')
    print('1 - View Speakers and Sessions')
    print('2 - View Attendees by Company')
    print('3 - Add New Attendee')
    print('4 - View Connected Attendees')
    print('5 - Add Attendee Connection')
    print('6 - View Rooms')
    print('x - Exit Application')


# -------- Helper functions -------------------
           

# prompt user to provide a company ID until the ID is a valid number
def get_valid_company_id(): 

    while True: 
        user_input = input('Enter company ID: ').strip()

        if not user_input.isdigit():
            continue

        company_id = int(user_input)

        if company_id <= 0:
            continue

        return company_id

# verify that company exists and return company name. Input: int, output: list
# TODO repurpose to return company name instead of company 
def company_exists(company_id):

    query = 'SELECT * FROM company' \
            ' WHERE companyID = %s LIMIT 1'

    cursor = conn.cursor() 
    cursor.execute(query,(company_id,))
    result = cursor.fetchone()

    return result 

# return attendee name from ID. Inputs: int, returns: string
def get_attendee_name(attendee_id):

    try:
        query = 'SELECT AttendeeName from Attendee' \
                ' WHERE AttendeeID = %s LIMIT 1'

        cursor = conn.cursor()
        cursor.execute(query,attendee_id)
        items = cursor.fetchall()

        attendee_name = items[0]['AttendeeName']

        return attendee_name
    
    except IndexError as e:
        print('*** ERROR *** : Attendee does not exist')
    except Exception as e:
        print('*** ERROR *** : Database error: {e}')

# verify if attendee ID exists in SLQ db. Input: int, Output: bool
def attendee_exists(attendee_id):

    try:
        query = 'SELECT * from Attendee' \
                ' WHERE AttendeeID = %s'

        cursor = conn.cursor()
        cursor.execute(query,(attendee_id,))
        item = cursor.fetchone()

        return item is not None

    except Exception as e: 
        print(f'Database Error :{e}')

# Return relations from Neo4J database 
def get_relations(tx, module):

    query = 'MATCH(n:Attendee{AttendeeID:$AttendeeID}) - [:CONNECTED_TO]-> (n1:Attendee) RETURN n1.AttendeeID as id' 
    results = tx.run(query, AttendeeID = module)

    relations = []
    for result in results:
        relations.append(result['id'])

    return relations

# ----------- MENU FUNCTIONS --------------- 

def view_speakers():

    try: 

        search_for = input('Enter speaker name: ')
        search_string = '%' + search_for + '%'
        query = 'SELECT session.speakerName, session.sessionTitle, room.roomName' \
                ' from session' \
                ' INNER JOIN room' \
                ' on session.roomID = room.roomID' \
                ' WHERE session.speakerName LIKE %s'



        cursor = conn.cursor()
        cursor.execute(query,(search_string,))
        items = cursor.fetchall()
  
        rows = []
        for item in items:
            rows.append(item['speakerName'] + '\t|\t' + item['sessionTitle'] + '\t|\t' + item['roomName'])
    
        print(f'Session details for: {search_for}')
        if rows != []:
            for row in rows:
                print(row) 
        else: 
            print('--------------')
            print('No speakers found of that name')

    except Exception as e: 
        print('Databse error: {e}')
   

#TODO check if Date of session needs to be included in the output
def view_attendees():

    while True: 
            
        try:

            search_for = get_valid_company_id()
            search_string = search_for
            company_query = 'SELECT companyName' \
                            ' from company' \
                            ' WHERE companyID = %s'
            
            attendee_query = 'SELECT attendee.attendeeName, attendee.attendeeDOB, session.sessionTitle, session.speakerName, room.roomName' \
                    ' from attendee' \
                    ' INNER JOIN registration' \
                    ' on attendee.attendeeID = registration.attendeeID' \
                    ' INNER JOIN session' \
                    ' on registration.sessionID = session.sessionID' \
                    ' INNER JOIN room' \
                    ' ON session.roomID = room.roomID' \
                    ' WHERE attendee.attendeeCompanyID = %s' \
                    ' ORDER BY attendee.attendeeName'

            # connect to db
            cursor = conn.cursor()
            cursor.execute(company_query, (search_string,))
            company = cursor.fetchall()
            cursor.execute(attendee_query,(search_string,))
            items = cursor.fetchall()

            # store values 
            company_name = company[0]['companyName']
            attendees = []
            for item in items:
                attendees.append(item['attendeeName'] + '\t|\t' + str(item['attendeeDOB']) + '\t|\t' + item['sessionTitle'] + '\t|\t' + item['speakerName'] + '\t|\t' + item['roomName'])
        
        
            #print results
            print(f"{company_name} Attendees")  
            if len(attendees) > 0:  
                for attendee in attendees:
                    print(attendee)
                break
            # exception: company has no attendee 
            else:
                print(f'No attendees found for {company_name}')
                continue

        # exception: company ID is a valid number but does not exist in the database
        except IndexError as e:
            print(f"Company with ID {search_for} doesn't exist")
            continue

        # exception: catch-all 
        except Exception as e:
            print(f'Database error: {type(e)}')

def add_new_attendee():

    try:

        print('Add New Attendee:')
        print('--------')
        id = input('Attendee ID: ')
        name = input('Name: ')
        dob = input('DOB: ')
        gender = input('Gender: ')
        company_id = int(input('Company ID: '))

        '''error handling: company ID does not exist in DB'''
        if not company_exists(company_id):
            print(f' ***ERROR*** Company ID {company_id} does not exist')
            return 

        query = 'INSERT INTO attendee' \
                ' (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)'\
                ' VALUES (%s, %s, %s, %s, %s)'
        
        cursor = conn.cursor()
        cursor.execute(query, (int(id), name, dob, gender, company_id))
        conn.commit()
        print('Attendee succcessfully added')
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            print(f'*** ERROR *** Attendee ID: {id} already exists')
    except pymysql.err.DataError as e:
        if e.args[0] == 1265:
            print(f'*** ERROR *** Gender must be Male/Female')
    except Exception as e:
        print (f'*** ERROR *** {e}')   


def view_connected_attendees():
    
    try: 
            
        attendee_id = int(input('Enter Attendee ID: '))

        '''get relations from neo4j'''
        with neo4j_driver.session() as session:

            '''execute  managed transaction with execute_read https://neo4j.com/docs/python-manual/current/transactions/'''
            relations = session.execute_read(get_relations, attendee_id)

        #get attendee name
        attendee = get_attendee_name(attendee_id)
        # Get connected attendees only when the attendee ID is valid and exists in the SQL database 
        if attendee is not None:
            print(f'Attendee Name: {attendee}')
            print('--------')
            if len(relations) > 0:
                print('These attendees are connected:')

                #match attendeeID with attendeeName
                for relation in relations:
                    relation_name = get_attendee_name(relation)
                    print(f'{relation}\t|\t{relation_name}')
            else: 
                print('No connections')

    # catch error for invalid ID (not int)
    except ValueError as e:
        print('*** ERROR *** : Invalid Attendee ID')
    # catch-all 
    except Exception as e:
        print (f'Database error: {e}')

def add_connection():

    while True: 
        try: 
            attendee_1_id = int(input('Enter Attendee 1 ID: '))
        except ValueError as e: 
            print(' *** ERROR ***: {e}')
            continue
        
        if attendee_exists(attendee_1_id):
            break
        else: 
            print(f'*** ERROR ***: Attendee {attendee_1_id} does not exist')

    while True: 
        try: 
            attendee_2_id = int(input('Enter Attendee 2 ID: '))
        except ValueError as e: 
            print(' *** ERROR ***: {e}')
            continue
        
        if attendee_exists(attendee_2_id):
            break
        else: 
            print(f'*** ERROR ***: Attendee {attendee_2_id} does not exist')        
    
    if attendee_1_id == attendee_2_id:
        print(f' *** ERROR *** : An attendee cannot be connected to him/herlsef')

    
    











    '''
    with neo4j_driver.session() as session: 

        try: 
            session.execute_write(add conection, )
'''
## main 
if __name__ == '__main__':
    add_connection()

