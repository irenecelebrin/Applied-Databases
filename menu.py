# menu file to display the application menu and handle the user's choices.

# import MySQL and Neo4j operations
from mysql_operations import view_speakers, view_attendees, add_new_attendee, view_rooms
from neo4j_operations import view_connected_attendees, add_connection

# display the application menu
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

# ---------------------- Main ---------------------

def main():
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
            add_connection()
        elif choice == '6':
            view_rooms()
        elif choice == 'x':
            break
        else:
            print('Select a valid option')
