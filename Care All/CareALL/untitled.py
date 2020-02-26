from db import *

test = 8
sql = f'SELECT PK_elder_id FROM elders where FK_younger_id = "{test}" '
mycursor.execute(sql)
val = mycursor.fetchall()

print(val)