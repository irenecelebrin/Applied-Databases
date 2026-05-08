import pymysql
from connections import conn


# -------- Helper functions -------------------

def get_valid_company_id():
    while True:
        user_input = input('Enter company ID: ').strip()

        if not user_input.isdigit():
            continue

        company_id = int(user_input)

        if company_id <= 0:
            continue

        return company_id


def company_exists(company_id):
    query = 'SELECT * FROM company' \
            ' WHERE companyID = %s LIMIT 1'

    cursor = conn.cursor()
    cursor.execute(query, (company_id,))
    result = cursor.fetchone()

    return result


def get_attendee_name(attendee_id):
    try:
        query = 'SELECT AttendeeName from Attendee' \
                ' WHERE AttendeeID = %s LIMIT 1'

        cursor = conn.cursor()
        cursor.execute(query, attendee_id)
        items = cursor.fetchall()

        attendee_name = items[0]['AttendeeName']

        return attendee_name

    except IndexError:
        print('*** ERROR *** : Attendee does not exist')
    except Exception as e:
        print(f'*** ERROR *** : Database error: {e}')


def attendee_exists(attendee_id):
    try:
        query = 'SELECT * from Attendee' \
                ' WHERE AttendeeID = %s'

        cursor = conn.cursor()
        cursor.execute(query, (attendee_id,))
        item = cursor.fetchone()

        return item is not None

    except Exception as e:
        print(f'Database Error: {e}')


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
        cursor.execute(query, (search_string,))
        items = cursor.fetchall()

        rows = []
        for item in items:
            rows.append(item['speakerName'] + '\t|\t' + item['sessionTitle'] + '\t|\t' + item['roomName'])

        print(f'Session details for: {search_for}')
        if rows:
            for row in rows:
                print(row)
        else:
            print('--------------')
            print('No speakers found of that name')

    except Exception as e:
        print(f'Database error: {e}')


def view_attendees():
    while True:
        try:
            search_for = get_valid_company_id()
            search_string = search_for
            company_query = 'SELECT companyName' \
                            ' from company' \
                            ' WHERE companyID = %s'

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
            cursor.execute(company_query, (search_string,))
            company = cursor.fetchall()
            cursor.execute(attendee_query, (search_string,))
            items = cursor.fetchall()

            company_name = company[0]['companyName']
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

            print(f'{company_name} Attendees')
            if len(attendees) > 0:
                for attendee in attendees:
                    print(attendee)
                break
            else:
                print(f'No attendees found for {company_name}')
                continue

        except IndexError:
            print(f"Company with ID {search_for} doesn't exist")
            continue
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

        if not company_exists(company_id):
            print(f' ***ERROR*** Company ID {company_id} does not exist')
            return

        query = 'INSERT INTO attendee' \
                ' (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)' \
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
        print(f'*** ERROR *** {e}')


def view_rooms():
    query = 'SELECT * FROM room'
    cursor = conn.cursor()
    cursor.execute(query)
    rooms = cursor.fetchall()

    print('Room ID\t|\tRoomName\t|\tCapacity')
    for room in rooms:
        print(f"{room['roomID']}\t|\t{room['roomName']}\t|\t{room['capacity']}")
