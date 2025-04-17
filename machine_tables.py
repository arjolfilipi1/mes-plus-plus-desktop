from peewee import *
import datetime

from create_tables import BaseModel,User,Departament,Part_nr,StockLocation,db
from hr_tables import Employee

class Machine_type(BaseModel):
    name = CharField( primary_key=True )
    description = CharField(  null = True, max_length = 550 )
class Machine(BaseModel):
    Machine_id   = CharField( primary_key=True )
    Name         = CharField(  max_length = 550 )
    Machine_type = ForeignKeyField( Machine_type, to_field="name",on_delete='CASCADE' )
    Model        = CharField( null = True, max_length = 550 )
    Year         = CharField(  max_length = 4 )
    Departament  = ForeignKeyField( Departament , null=True , to_field="name",on_delete='SET NULL' )
    Operator     = ForeignKeyField( Employee    , null=True , to_field="Name",on_delete='SET NULL' )
    Active       = BooleanField(default = True)
    '''
    To add:
    Maintenance type
    Maintenance frequency
    '''
    
class Applicator(BaseModel):
    Name           = CharField( max_length = 550 )
    Code           = CharField( max_length = 550,primary_key= True )
    Manufacturer   = CharField( max_length = 550,null=True, )
    Serial         = CharField( max_length = 550,null=True, )
    In_use         = BooleanField(default= True)
    In_maintenance = BooleanField(default= True)
    Long_storage   = BooleanField(default= True)
    Machine        = ForeignKeyField( Machine,null=True, to_field="Machine_id",on_delete='SET NULL' )

'''
Applicator die type, like Wire crimper, wire anvil etc
'''

class ApplicatorDieType(BaseModel):
    Name           = CharField( max_length = 550 )
    Code           = CharField( max_length = 550,primary_key= True )
    Reversible     = BooleanField( default = False )

class SparePart(BaseModel):
    Code           = CharField( max_length = 550,primary_key= True )
    Name           = CharField( max_length = 550 )
    Description    = CharField( max_length = 550 )
    Part_nr        = ForeignKeyField( Part_nr, null=True,on_delete='SET NULL')
    Safety_stock   = FloatField(null=True)
    Storage        = ForeignKeyField(StockLocation,to_field='name' ,null=True,on_delete='SET NULL', backref='children')
    Shelf          = CharField( max_length = 550 )
    #lead time in days
    Lead_time      = FloatField(null=True)
    Calculated_l_t = FloatField(null=True)
    Machine        = ForeignKeyField(Machine_type, null=True,on_delete='SET NULL')
    Applicator     = ForeignKeyField(Applicator, null=True,on_delete='SET NULL')

'''
To keep track of the active die, 
'''

class ActiveDie(BaseModel):
    Applicator   = ForeignKeyField( Applicator, to_field="Code",on_delete='CASCADE' )
    Type         = ForeignKeyField( ApplicatorDieType, to_field="Code",on_delete='CASCADE' )
    Count        = IntegerField( default = 0 )
    Max_count    = IntegerField( default = 0 )
    SparePart    = ForeignKeyField( SparePart, to_field="Code",on_delete='CASCADE' )
    Changed_date = DateTimeField(default=datetime.datetime.now())
    Reverse      = BooleanField(default = False)
    class Meta:
        indexes = (
            (('Applicator', 'Type'), True),
        )
        
# db.create_tables([Machine_type,Machine,Applicator,ApplicatorDieType,SparePart,ActiveDie])
db.create_tables([Machine,ActiveDie])