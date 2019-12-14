#!/usr/bin/env python
# coding: utf-8

# In[191]:


class RentalShops:
    def __init__(self,shop_name,no_of_bikes):
        self.shop_name = shop_name
        self.no_of_bikes = no_of_bikes
      
    def generate_bill(customer):
        total_bill = (customer.total_hours * 5) + (customer.total_days * 20) + (customer.total_weeks * 60)
        if customer.total_no_of_bikes > 5:
            return "Cannot Generate bill, you have exceeded the no of bike limits"
        if customer.total_no_of_bikes > 3 and customer.total_no_of_bikes <= 5:
            print("Congratulation, you will get 30% off on your total bill as you are falling in group rental option")
            return "The total bill after group rental is {}".format((70/100)*total_bill)
        else:
            return "The total bill is {}".format(total_bill)
    
    def display_available_bikes(self):
        return self.no_of_bikes
    
    def hourly_basis_request(self,no_of_hours):
        self.amount_per_hours = no_of_hours * 5
        return "The cost for {} hours is {}".format(no_of_hours,self.amount_per_hours)
    
    def daily_basis_request(self,no_of_days):
        self.amount_per_days = no_of_days * 20
        return "The cost for {} days is {}".format(no_of_days,self.amount_per_days)

    def weekly_basis_request(self,no_of_weeks):
        self.amount_per_weeks = no_of_weeks * 60
        return "The cost for {} weeks is {}".format(no_of_weeks,self.amount_per_weeks)
    


# In[192]:


class Customers:
    def __init__(self,name,email):
        self.name = name
        self.email = email
        self.total_hours = 0
        self.total_days = 0
        self.total_weeks = 0
        self.total_no_of_bikes = 0
        
    def check_available_bikes(self,shop):
            return "The available number of bikes are {}".format(shop.no_of_bikes)
    
    def bikes_on_hourly_basis(self,shop,no_of_hours):
        self.total_hours += no_of_hours
        self.total_no_of_bikes += 1
        shop.no_of_bikes -= 1
        if shop.no_of_bikes > 0:
            return shop.hourly_basis_request(no_of_hours)
        else:
            return "sorry! No bikes available right now, Glad to see you soon"
        
    def bikes_on_daily_basis(self,shop,no_of_days):
        self.total_days += no_of_days
        self.total_no_of_bikes += 1
        shop.no_of_bikes -= 1
        if shop.no_of_bikes > 0:
            return shop.daily_basis_request(no_of_days)
        else:
            return "sorry! No bikes available right now, Glad to see you soon"
    
    def bikes_on_weekly_basis(self,shop,no_of_weeks):
        self.total_no_of_bikes += 1
        if self.total_no_of_bikes > 5:
            return "Sorry! You cannot take more than 5 bikes"
        self.total_weeks += no_of_weeks
        shop.no_of_bikes -= 1
        if shop.no_of_bikes > 0:
            if self.total_no_of_bikes >= 3 and self.total_no_of_bikes <= 5:
                print("Congratulaions, you can select for group rental which gives 30% off on your total price")
            return shop.weekly_basis_request(no_of_weeks)
        else:
            return "sorry! No bikes available right now, Glad to see you soon"
    
    def return_bike(self):
        return RentalShops.generate_bill(self)
    
    def group_rental(self):
        if self.total_no_of_bikes > 3 and self.total_no_of_bikes <= 5:
            return "The total bill after group rental is {}".format((30/100)*RentalShops.generate_bill(self))
        else:
            return "You need to select 3 to 5 bikes for group rental"
        


# In[190]:


cust1 = Customers("Vishwa","vishwa@abc.com")
shop1 = RentalShops("Yamaha",10)
cust1.check_available_bikes(shop1)
print(cust1.bikes_on_hourly_basis(shop1,5))
print(cust1.bikes_on_hourly_basis(shop1,5))
print(cust1.bikes_on_hourly_basis(shop1,5))
print(cust1.bikes_on_daily_basis(shop1,5))
print(cust1.bikes_on_weekly_basis(shop1,2))
print(cust1.bikes_on_weekly_basis(shop1,2))
cust1.return_bike()

