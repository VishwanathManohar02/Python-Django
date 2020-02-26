from db import *

class ElderProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
        mycursor.execute(sql)
        user_id = mycursor.fetchone()
        self.user_id = user_id[0]
        self.elder_name = user_id[1]
        sql = f'SELECT PK_elder_id FROM elders WHERE FK_user_id="{self.user_id}"'
        mycursor.execute(sql)
        elder_id = mycursor.fetchone()
        self.elder_id=elder_id[0]

    def log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} not registered. Please try to register first')
                  # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_elder()
        else:
            print("Wrong email and password")

    def dashboard_elder(self):
        sql = f'SELECT available FROM elders where PK_elder_id = {self.elder_id}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            print("You are currently Available to take care of.\n1.Make Available\\Unavailable\n2.Allocate Fund\n3.Request\n4.Take Care Name\n5.Give review and rating for a younger\n6.LogOut")
            choice = int(input())
            if choice==1:
                self.change_status()
                self.dashboard_elder()
            elif choice==2:
                self.allocate_fund()
            elif choice==3:
                self.show_request()
            elif choice==4:
                self.take_care_name()
            elif choice==5:
                self.review()
            elif choice==6:
                self.log_out()

        else:
            print("You are currently Unavailable to take care of.\n1.Make Available\n2.Log Out")
            choice = int(input())
            if choice==1:
                self.change_status()
                self.dashboard_elder()
            elif choice==2:
                self.log_out()

    # elder should be able to allocate fund
    def allocate_fund(self):
        print("Enter the amount to allocate as fund for yourself")
        fund_amt = int(input('Fund Amount :'))
        sql = f'UPDATE elders set fund = "{fund_amt}" where PK_elder_id = "{self.elder_id}" '
        mycursor.execute(sql)
        mydb.commit()
        print("funds allocated successfully to your account")

    # elder can change their status from available to unavailable and vice-versa
    def change_status(self):
        print("1.Available\n2.Unavialable")
        choice = int(input())
        if choice == 1:
            sql = f'UPDATE elders SET available = True where PK_elder_id = "{self.elder_id}" '
            mycursor.execute(sql)
            mydb.commit()
        else:
            sql = f'UPDATE elders SET available = False where PK_elder_id = "{self.elder_id}" '
            mycursor.execute(sql)
            mydb.commit()
        print('Status Changed Successfully')
    
    # elder can see requests and accept whome they trust only 1 request can be accepted by elder      
    def show_request(self):
        sql = f'SELECT * FROM request where FK_elder_id = "{self.elder_id}" '
        mycursor.execute(sql)
        val = mycursor.fetchall()
        sql = f'SELECT FK_younger_id from elders where PK_elder_id = "{self.elder_id}" '
        mycursor.execute(sql)
        younger_id = mycursor.fetchone()
        
        if len(val)>=1:
            if None not in younger_id:
                print(val)
                print("Select the younger_id from the above table as your care taker")
                choice = int(input())
                sql = f'UPDATE elders SET FK_younger_id = %s WHERE PK_elder_id = %s'
                val = (choice,self.elder_id)
                mycursor.execute(sql,val)
                mydb.commit()
                print('Congratulations! you got a new care taker')
            else:
                print("You cannot accept the request of more than one care taker")
        else:
            print("There are no requests for you right now! come back again")

    # elder can see name of younger who is taking care of them
    def take_care_name(self):
        sql = f'SELECT FK_younger_id from elders where PK_elder_id = "{self.elder_id}" '
        mycursor.execute(sql)
        val = mycursor.fetchone()
        
        if None not in val:
            sql = 'SELECT * FROM elders'
            mycursor.execute(sql)
            print(mycursor.fetchall())
        else:
            print("No care takers for you right now")

    # elder can give review and rating to youngers
    def review(self):
        sql = f'SELECT FK_younger_id from elders where PK_elder_id = "{self.elder_id}" '
        mycursor.execute(sql)
        val = mycursor.fetchone()
        
        if None not in val:
            sql = f'SELECT * FROM youngers WHERE PK_younger_id = (SELECT FK_younger_id FROM elders where PK_elder_id="{self.elder_id}") '
            mycursor.execute(sql)
            print(mycursor.fetchall())
            print("Enter the rating for your care taker")
            rating = int(input('Rating :'))
            review = str(input('Review :'))
            val = f'UPDATE youngers SET rating = "{rating}" WHERE PK_younger_id = (SELECT FK_younger_id FROM elders where PK_elder_id="{self.elder_id}") '
            mycursor.execute(val)
            mydb.commit()
            sql = f'SELECT name FROM users where PK_user_id = "{self.user_id}" '
            mycursor.execute(sql)
            name = mycursor.fetchone()
            sql = f'SELECT FK_user_id FROM youngers WHERE PK_younger_id = (SELECT FK_younger_id FROM elders where PK_elder_id="{self.elder_id}")'
            mycursor.execute(sql)
            user_id = mycursor.fetchone()
            sql = f'INSERT INTO reviews (FK_user_id,review,rating,review_by) VALUES (%s, %s, %s, %s)'
            val = (user_id[0],review,rating,name[0])
            mycursor.execute(sql,val)
            mydb.commit()
            print("Thanks for your feeeback")
            
        else:
            print("As there are no care takers for you right now, You cannot give rating")
            
    def log_out(self):
        print("Are you sure you want to Logout.\n1.yes\n2.no")
        choice = int(input())
        if choice == 1:
            print("You have been Logged out")
            index.welcome()
        elif choice == 2:
            self.dashboard_elder()
        else:
            print("Enter the correct choice")
            self.log_out()
