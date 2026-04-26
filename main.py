# Final project for Applied Databases

# import 
import pymysql

## connect to MySQL database.

# connect to database
conn = pymysql.connect(user = 'root', 
                        cursorclass = pymysql.cursors.DictCursor,
                        password = '',
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
            print('3')
        elif choice == '4':
            print('4')
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
           

# verify that company ID is a valid number (integer, above 0)
def get_valid_company_id(): 

    while True: 
        user_input = input('Enter company ID: ').strip()

        if not user_input.isdigit():
            continue

        company_id = int(user_input)

        if company_id <= 0:
            continue

        return company_id
    

#TODO check if Date of session needs to be included in the output
def view_attendees():

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

    
        cursor = conn.cursor()
        cursor.execute(company_query, (search_string,))
        company = cursor.fetchall()
        cursor.execute(attendee_query,(search_string,))
        items = cursor.fetchall()


        attendees = []
        for item in items:
            attendees.append(item['attendeeName'] + '\t|\t' + str(item['attendeeDOB']) + '\t|\t' + item['sessionTitle'] + '\t|\t' + item['speakerName'] + '\t|\t' + item['roomName'])
    
    
        #print results
        print(f"{company[0]['companyName']} Attendees")   
        for attendee in attendees:
            print(attendee)

    # If company ID is a valid number but does not exist in the database
    except IndexError as e:
        print('Company ID not found')

    # catch-all 
    except Exception as e:
        print(f'Database error: {type(e)}')




## main 
if __name__ == '__main__':
    main()

