# MySQL operations and helper functions 

# import pymysql and connections
import pymysql
from connections import conn, neo4j_driver


# -------- Helper functions -------------------

# ask user to enter a company id until it's valid (it's a integer and positive) 
def get_valid_company_id():
    while True:
        user_input = input('Enter company ID: ').strip()

        if not user_input.isdigit():
            continue

        company_id = int(user_input)

        if company_id <= 0:
            continue

        return company_id

# find company by id and return its name, or None if it doesn't exist
def get_company_name(company_id):
    query = 'SELECT companyName FROM company' \
            ' WHERE companyID = %s LIMIT 1'

    cursor = conn.cursor()
    cursor.execute(query, (company_id,))
    result = cursor.fetchone()

    return result['companyName'] if result else None


# get the attendee name from the attendee id
def get_attendee_name(attendee_id):
    # query the database to get 1 attendee name 
    try:
        query = 'SELECT AttendeeName from Attendee' \
                ' WHERE AttendeeID = %s LIMIT 1'

        cursor = conn.cursor()
        cursor.execute(query, (attendee_id,))
        items = cursor.fetchall()

        attendee_name = items[0]['AttendeeName']

        # return the attendee name
        return attendee_name

    # handle exceptions
    except IndexError:
        print('*** ERROR *** : Attendee does not exist')
    except Exception as e:
        print(f'*** ERROR *** : Database error: {e}')


# check if an attendee exists in the database
def attendee_exists(attendee_id):
    try:
        query = 'SELECT * from Attendee' \
                ' WHERE AttendeeID = %s'

        cursor = conn.cursor()
        cursor.execute(query, (attendee_id,))
        item = cursor.fetchone()

        # return True if the attendee exists, False otherwise
        return item is not None

    # handle exceptions
    except Exception as e:
        print(f'Database Error: {e}')


# ----------- MENU FUNCTIONS ---------------

# view speakers and their sessions (option 1 in the menu)
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
        cursor.execute(query, (search_string,))
        items = cursor.fetchall()

        rows = []
        # add the speaker name, session title and room name to the rows list
        for item in items:
            rows.append(item['speakerName'] + '\t|\t' + item['sessionTitle'] + '\t|\t' + item['roomName'])

        # print the session details
        print(f'Session details for: {search_for}')
        # if there are rows, print them else print fallback message
        if rows:
            for row in rows:
                print(row)
        else:
            print('--------------')
            print('No speakers found of that name')

    # handle exceptions
    except Exception as e:
        print(f'Database error: {e}')


# view attendees by company (option 2 in the menu)
def view_attendees():
    while True:
        try:
            # get a valid company id from the user
            search_for = get_valid_company_id()

            company_name = get_company_name(search_for)
            if not company_name:
                print(f"Company with ID {search_for} doesn't exist")
                continue

            attendee_query = 'SELECT attendee.attendeeName, attendee.attendeeDOB, session.sessionTitle, session.speakerName, session.sessionDate, room.roomName' \
                             ' from attendee' \
                             ' INNER JOIN registration' \
                             ' on attendee.attendeeID = registration.attendeeID' \
                             ' INNER JOIN session' \
                             ' on registration.sessionID = session.sessionID' \
                             ' INNER JOIN room' \
                             ' ON session.roomID = room.roomID' \
                             ' WHERE attendee.attendeeCompanyID = %s' \
                             ' ORDER BY attendee.attendeeName'

            cursor = conn.cursor()
            cursor.execute(attendee_query, (search_for,))
            items = cursor.fetchall()
            # store attendees in a list 
            attendees = []
            for item in items:
                attendees.append(
                    item['attendeeName'] + '\t|\t' +
                    str(item['attendeeDOB']) + '\t|\t' +
                    item['sessionTitle'] + '\t|\t' +
                    item['speakerName'] + '\t|\t' +
                    str(item['sessionDate']) + '\t|\t' +
                    item['roomName']
                )

            # print company name
            print(f'{company_name} Attendees')
            # print attendees if there are any
            if len(attendees) > 0:
                for attendee in attendees:
                    print(attendee)
                break
            # If no attendees are found, the user can try again with a different company ID
            else:
                print(f'No attendees found for {company_name}')
                continue

        except Exception as e:
            print(f'Database error: {e}')


# add a new attendee (option 3 in the menu)
def add_new_attendee():
    try:
        # get required attendee information from the user
        print('Add New Attendee:')
        print('--------')
        attendee_id = input('Attendee ID: ')
        name = input('Name: ')
        dob = input('DOB: ')
        gender = input('Gender: ')
        company_id = int(input('Company ID: '))

        # check if the company exists and if not print an error message and ask the user to try again with a different company ID
        if not get_company_name(company_id):
            print(f' *** ERROR*** Company ID: {company_id} does not exist')
            return

        # add the new attendee into the database
        query = 'INSERT INTO attendee' \
                ' (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)' \
                ' VALUES (%s, %s, %s, %s, %s)'

        cursor = conn.cursor()
        cursor.execute(query, (int(attendee_id), name, dob, gender, company_id))
        conn.commit()

        # add the new attendee to the Neo4j database
        with neo4j_driver.session() as session:
            from neo4j_operations import create_attendee_node
            session.execute_write(create_attendee_node, int(attendee_id))

        # print success message
        print('Attendee successfully added')

    # handle exceptions and print error messages 
    # if the attendee ID already exists
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            print(f'*** ERROR *** Attendee ID: {attendee_id} already exists')
    # if the gender is not Male/Female
    except pymysql.err.DataError as e:
        if e.args[0] == 1265:
            print(f'*** ERROR *** Gender must be Male/Female')
    # catchall
    except Exception as e:
        print(f'*** ERROR *** {e}')


# view rooms (option 6 in the menu)
def view_rooms():

    try: 
        # query the database to get all rooms
        query = 'SELECT * FROM room'
        cursor = conn.cursor()
        cursor.execute(query)
        rooms = cursor.fetchall()

        # print the room details
        print('Room ID\t|\tRoomName\t|\tCapacity')
        for room in rooms:
            print(f"{room['roomID']}\t|\t{room['roomName']}\t|\t{room['capacity']}")

    except Exception as e:
        print(f'Database error: {e}')