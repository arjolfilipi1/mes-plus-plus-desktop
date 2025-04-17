from peewee import *
import datetime

from create_tables import db,BaseModel,User,Departament


class Employee(BaseModel):
    Worker_id    = CharField( primary_key=True )
    Name         = CharField(  max_length = 550 )
    Birthday     = DateField(  )
    email        = CharField( null=True, max_length = 550 )
    phone        = CharField( null=True, max_length = 550 )
    address      = CharField( null=True, max_length = 1000 )
    def __str__(self):
        return self.Worker_id
class Shift(BaseModel):
    name     = CharField(primary_key=True)
    start    = TimeField()
    end      = TimeField()
'''
class Shift(BaseModel):
    name     = CharField(primary_key=True)
    quota    = IntegerField( default= None,null = True)
'''   
   
class Details(BaseModel):
    Employee    = ForeignKeyField(Employee, to_field="Worker_id",on_delete='CASCADE')
    Departament = ForeignKeyField(Departament, to_field="name", on_delete='CASCADE')
    Hire_date   = DateField(  default= datetime.datetime.now().date())
    Shift       = ForeignKeyField(Shift, null= True, to_field="name", on_delete='SET NULL')
    Photo        = CharField( null=True, max_length = 550 )
    User        = ForeignKeyField(User, null= True, to_field="username", on_delete='SET NULL')
    
class Attendance(BaseModel):
    Employee    = ForeignKeyField(Employee, to_field="Worker_id",on_delete='CASCADE')
    date        = DateField(  default= datetime.datetime.now().date())
    start_time  = TimeField()
    end_time    = TimeField(  null = True )
    hours       = FloatField( null = True )
    overtime    = FloatField( null = True )
    
db.create_tables([Employee,Shift,Details,Attendance])