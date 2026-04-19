# topic 10 exercise 1 and 2. 

import pymysql

# connect to database
conn = pymysql.connect(user = 'root', 
                        cursorclass = pymysql.cursors.DictCursor,
                        password = '',
                        host = 'localhost',
                        db = 'hospital',
                        port = 3306)

'''test connection
query =' select * from doctor_table '

with conn: 
    cursor = conn.cursor()
    cursor.execute(query)
    doctors = cursor.fetchall()
'''

def main():

    display_menu()

    while True: 
        choice = input('Select action:')
        if choice == '1':
            add_new_patient()
            display_menu()
        elif choice == '2':
            find_patient()
            display_menu()
        elif choice == '3':
            break
        else: 
            print('Select a valid option!')
            display_menu()


def display_menu(): 
    print('----')
    print('Menu:')
    print('1. Add new patient')
    print('2. Find a patient')
    print('3. Exit')
    print('----')

def add_new_patient():
    try: 
        ppsn = input('Insert patient PPSN: ')
        first_name =  input('Insert patient first name: ')
        surname =  input('Insert patient surname: ')
        address =  input('Insert patient address: ')
        doctorID =  int(input('Insert doctor ID: '))

        ins = 'INSERT INTO patient_table' \
        ' (ppsn, first_name, surname, address, doctorID) ' \
        'VALUES (%s, %s, %s, %s, %s)'

        with conn:
        
            cursor = conn.cursor()
            cursor.execute(ins, (ppsn, first_name,surname,address,doctorID))
            conn.commit()
            print('--- \r\nInsert successful.')
    except ValueError as e:
            print('Invalid value entered for doctorID')
    except pymysql.err.IntegrityError as e: 
            print('Existing PPSN entered, or non-existent doctorID')
    except pymysql.err.InterfaceError as e: 
            print('Interface error', e)
    except pymysql.err.Error as e:
            print('Error', e)

def find_patient():
     
    try: 
        search_for = input('Search for: ')
        find_string = '%' + search_for + '%'

        query = 'Select * from patient_table ' \
        'WHERE surname LIKE %s'

        with conn: 
            cursor = conn.cursor()
            cursor.execute(query, (find_string))
            patient_details = cursor.fetchall()
            print(search_for)
            for patient in patient_details:
                print(patient)

    except: 
         (print('error'))



if __name__ == '__main__':
    main()

