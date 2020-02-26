from db import *
import index 

class YoungerProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
        mycursor.execute(sql)
        user_id = mycursor.fetchone()
        self.user_id = user_id[0]
        self.younger_name = user_id[1]
        sql = f'SELECT PK_younger_id FROM youngers WHERE FK_user_id={self.user_id}'
        mycursor.execute(sql)
        younger_id = mycursor.fetchone()
        self.younger_id=younger_id[0]
        sql = f'SELECT FK_younger_id from elders where FK_younger_id = {self.younger_id}'
        mycursor.execute(sql)
        self.youngerCount = mycursor.fetchall()

    def log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} is not registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_younger()
        else:
            print("Wrong email and password")
            import index

    def dashboard_younger(self):
        elderCount = len(self.youngerCount)
        print(f'Currentlty you are taking care of {elderCount} Elders\nYou can request for {4-elderCount} more elders to take care of.\n1.View list of Available elders to take care of.\n2.Give review and rating for a elder\n3.LogOut')
        choice = int(input())
        if choice==1:
            self.request_elder()
        elif choice==2:
            self.review()
        elif choice==3:
            self.log_out()

    # user should be able to see list of available elder and sent them request. NOTE:- 1 user can't sent request to same elder twice
    def request_elder(self):
        if len(self.youngerCount) <= 4:
            sql = f'SELECT * FROM elders where available = True'
            mycursor.execute(sql)
            print(mycursor.fetchall())
            print("Select elder_id from the table whom you want to take care")
            choice = int(input())
            sql = f'INSERT INTO request (FK_younger_id,FK_elder_id,request_status) VALUES (%s, %s, %s)'
            val = (self.younger_id,choice,True)
            mycursor.execute(sql,val)
            mydb.commit()
            print("request has been added successfully")
            
    # younger can give review and rating to elders
    def review(self):
        sql = f'SELECT PK_elder_id FROM elders where FK_younger_id = "{self.younger_id}" '
        mycursor.execute(sql)
        val = mycursor.fetchone()
        
        if val:
            sql = f'SELECT * FROM elders WHERE FK_younger_id = {self.younger_id}'
            mycursor.execute(sql)
            print("The elders list you are taking care is below")
            print(mycursor.fetchall())
            print("Enter the user_id whom you want to give review and rating")
            choice = int(input())
            rating = int(input('Rating :'))
            review = str(input('Review :'))
            val = f'UPDATE elders SET rating = {rating} where FK_user_id = {choice}'
            mycursor.execute(val)
            mydb.commit()
            review_table = f'INSERT INTO reviews (FK_user_id,review,rating,review_by) VALUES (%s, %s, %s, %s)'
            sql = f'Select name FROM users where PK_user_id = {self.user_id} '
            mycursor.execute(sql)
            reviewer_name = mycursor.fetchone()
            val = (choice,review,rating,reviewer_name[0])
            mycursor.execute(review_table,val)
            mydb.commit()
            print("Thanks for your feeeback")
            print("\n\n Want to rate other elders you are taking care of!\n1.Yes\n2.No")
            choice = int(input())
            if choice == 1:
                self.review()
            else:
                self.dashboard_younger()
        else:
            print("As you are not taking care of any one you cannot give rating")

    def log_out(self):
        print("Are you sure you want to Logout.\n1.yes\n2.no")
        choice = int(input())
        if choice == 1:
            print("You have been Logged out")
            index.welcome()
        elif choice == 2:
            self.dashboard_younger()
        else:
            print("Enter the correct choice")
            self.log_out()
