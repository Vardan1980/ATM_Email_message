import pymysql
import yagmail
db = {"host": "localhost",
      "user": "root",
      "password": "",
      "database": "ATM"}
connection = pymysql.connect(**db)
cursor = connection.cursor()
attempts = 0
yag = yagmail.SMTP('davit.manukyan.d@tumo.org','phppython404')
while (True):
    if attempts==3:
        break
    else:
        operation = input('Press r for registration, l for login, e for exit, d for remove user -> ')
        if operation == 'r':
            user_name = input('Enter your name -> ')
            email = input('Enter email -> ')
            password = input('Enter password -> ')
            r_password = input('Repeat password -> ')
            if password != r_password:
                print('Password doesnt match')
                continue
            else:
                create = "INSERT INTO users (Name, Password, Email, Balance) VALUES (%s,%s,%s,%s)"
                cursor.execute(create, (user_name, password, email, 0))
                connection.commit()
                text = 'You are registered ATM'
                print('Registration completed !')
                #yag.send(to=f'{email}', subject='ATM message', contents=text)
                print(f'Message sent {email} email')
                print('-'*40)
        elif operation == 'l':
            while (True):
                if attempts == 3:
                    break
                email = input('Enter your email -> ')
                password = input('Enter your password -> ')
                read = "SELECT * FROM users WHERE Password = %s AND Email = %s"
                cursor.execute(read, (password, email))
                data = cursor.fetchone()
                if data == None:
                  print('Wrong password or email ! Try again!')
                  attempts += 1
                  continue
                else:
                  print(f'Welcome {data[1]}')
                  print('-'*40)
                  print('Check balance - b ')
                  print('Cash in - (+)')
                  print('Cash out - (-)')
                  print('Transaction - t ')
                  print('Exit - e ')
                  print('-' * 40)
                  while (True):
                      command=input('Enter your command -> ')
                      if command == 'b':
                          print(f'Dear {data[1]} your balance -> {data[4]} AMD')
                      elif command == '+':
                          sum = int(input('Enter cash in sum -> '))
                          text = f'Your current balance -> {data[4] + sum} AMD'
                          update="UPDATE users SET balance = %s WHERE id = %s"
                          cursor.execute(update,(data[4]+sum,data[0]))
                          connection.commit()
                          print(f'Your current balance -> {data[4]+sum} AMD')
                          read = "SELECT * FROM users WHERE id=%s"
                          cursor.execute(read,(data[0]))
                          connection.commit()
                          data=cursor.fetchone()
                          #yag.send(to=f'{data[3]}', subject='ATM balance change', contents=text)
                          print(f'Message sent {data[3]} email')
                          print('-' * 40)
                      elif command == '-':
                          sum=int(input('Enter cash out sum -> '))
                          text = f'Your current balance -> {data[4] - sum} AMD'
                          if sum > data[4]:
                              print(f'Error. Your balance -> {data[4]} AMD')
                          else:
                              update = "UPDATE users SET balance = %s WHERE id = %s"
                              cursor.execute(update, (data[4] - sum, data[0]))
                              connection.commit()
                              print(f'Your current balance -> {data[4] - sum} AMD')
                              read = "SELECT * FROM users WHERE id=%s"
                              cursor.execute(read, (data[0]))
                              connection.commit()
                              data = cursor.fetchone()
                              #yag.send(to=f'{data[3]}', subject='ATM balance change', contents=text)
                              print(f'Message sent {data[3]} email')
                              print('-' * 40)
                      elif command == 't':
                          transaction_id = input('Enter users id for transaction -> ')
                          sum = int(input('Enter transaction sum -> '))
                          read = "SELECT * FROM users WHERE id = %s"
                          cursor.execute(read,(transaction_id))
                          connection.commit()
                          an_data = cursor.fetchone()
                          text = f'Your current balance -> {data[4] - sum} AMD'
                          text1 = f'Your current balance -> {an_data[4] + sum} AMD'
                          if (an_data != None) and (an_data[0] != data[0]) and (sum <= data[4]):
                             update = "UPDATE users SET balance = %s WHERE id = %s"
                             cursor.execute(update,(data[4]-sum,data[0]))
                             connection.commit()
                             update = "UPDATE users SET balance = %s WHERE id = %s"
                             cursor.execute(update, (an_data[4] + sum, an_data[0]))
                             connection.commit()
                             print(f'Your current balance -> {data[4]-sum} AMD')
                             read = "SELECT * FROM users WHERE id=%s"
                             cursor.execute(read, (data[0]))
                             connection.commit()
                             data = cursor.fetchone()
                             print('-' * 40)
                             #yag.send(to=f'{data[3]}', subject='ATM balance change', contents=text)
                             print(f'Message sent {data[3]} email')
                             print('-' * 40)
                             #yag.send(to=f'{an_data[3]}', subject='ATM balance change', contents=text1)
                             print(f'Message sent {an_data[3]} email')
                             print('-' * 40)
                      elif command == 'e':
                          break
                      else:
                          print('Bad command!!!')
                          attempts+=1
        elif operation == 'e':
            break
        elif operation == 'd':
            id_delete=int(input('Enter removed id -> '))
            password = input('Enter id password -> ')
            read = "SELECT * FROM users WHERE id=%s AND Password=%s"
            cursor.execute(read,(id_delete,password))
            connection.commit()
            data = cursor.fetchone()
            if data == None:
                print('This id or password not correct')
            else:
                delete = "DELETE FROM users WHERE id = %s"
                cursor.execute(delete,id_delete)
                connection.commit()
        else:
            print("Bad command! Try again!")
            continue
connection.close()
yag.close()
