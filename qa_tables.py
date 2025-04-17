from peewee import *
import datetime
from create_tables import Part_nr,db,BaseModel,StockLocation
#model for the tests that can be performed



class TestModel(BaseModel):
    name        = CharField( primary_key = True, max_length = 250 )
    description = CharField(  null = True, max_length = 250 )
    # is test performed on use or when item passes a location
    # eg. terminals are tested on use
    on_use      = BooleanField(default =  False)
    # 'Does this test require a value when adding a test result?'
    requires_value      = BooleanField(default =  False)
    requires_attachment = BooleanField(default =  False)
    # test requirenmets default
    value           = FloatField(  null = True )
    lower_tolerance = FloatField(  null = True )
    upper_tolerance = FloatField(  null = True )
    required        = BooleanField( default =  False )
    #choices, for comma separated test choices, can be overwriten
    choices         = CharField( max_length = 5000,  null = True)
    
class Test(TestModel):
    part = ForeignKeyField( Part_nr, to_field="Part_nr_txt",on_delete= 'CASCADE' )
    test = ForeignKeyField( TestModel, to_field="name",on_delete= 'CASCADE' )
    name = None
    description = None
    class Meta:
        indexes = (
            (('part', 'test'), True),
        )
    # if no data provided for these fields than the default is applied
    def save(self, *args, **kwargs):
        self.name = self.test.name + " " + self.part.Part_nr_txt if not self.name else self.name
        self.value = self.test.value if not self.value else self.value
        self.requires_value = self.test.requires_value if not self.requires_value else self.requires_value
        self.requires_attachment = self.test.requires_attachment if not self.requires_attachment else self.requires_attachment
        self.lower_tolerance = self.test.lower_tolerance if not self.lower_tolerance else self.lower_tolerance
        self.upper_tolerance = self.test.upper_tolerance if not self.upper_tolerance else self.upper_tolerance
        self.required = self.test.required if not self.required else self.required
        self.choices = self.test.choices if not self.choices else self.choices
        return super(Test, self).save(*args, **kwargs)
class BomItem(BaseModel):
    # part: Link to the parent part (the part that will be produced)
    part = ForeignKeyField( Part_nr, to_field="Part_nr_txt" ,on_delete= 'CASCADE')
    # sub_part: Link to the child part (the part that will be consumed)
    sub_part = ForeignKeyField( Part_nr, to_field="Part_nr_txt",on_delete= 'CASCADE' )
    # quantity: Number of 'sub_parts' consumed to produce one 'part'
    value = FloatField( default = 0 )
    # optional: Boolean field describing if this BomItem is optional
    optional = BooleanField(default =  False)
    # consumable: Boolean field describing if this BomItem is considered a 'consumable'
    consumable = BooleanField(default =  False)
    # reference: BOM reference field (e.g. part designators)
    reference = IntegerField(default = 1)
    # overage: Estimated losses for a Build. Can be expressed as absolute value (e.g. '0.07')
    overage = FloatField(default = 0,null = True, )
    # note: Note field for this BOM item
    note = CharField(  null = True, max_length = 250 )
    # inherited: This BomItem can be inherited by the BOMs of variant parts
    consumable = BooleanField(default =  False)
    # allow_variants: Stock for part variants can be substituted for this BomItem
    consumable = BooleanField(default =  False)

# db.create_tables([Test])
'''
try:
    nt = Test.create(part = '444000016176',test = 'test',name='DROP test;--')
    nt.save()
except Exception as e:
    print(e)
    '''
    
# db.create_tables([TestModel,Test,BomItem])