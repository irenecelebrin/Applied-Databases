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

    display_menu()

    # map choice to CRUD operations 
    # now placeholders
    while True:
        choice = input('Choice: ')
        if choice == '1':
            view_speakers()
            display_menu()
        elif choice == '2':
            print('2')
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


# function to display the menu in the terminal 
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

    
    except:
        print('error')

    with conn: 
        cursor = conn.cursor()
        cursor.execute(query,(search_string))
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
           




## main 
if __name__ == '__main__':
    main()

