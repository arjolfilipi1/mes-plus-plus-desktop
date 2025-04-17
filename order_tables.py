from peewee import *
import datetime
from create_tables import *


class Order(BaseModel):
    # reference: Unique order number / reference / code
    reference     = CharField(primary_key=True)
    # description: Long form description (required)
    description = CharField(   max_length = 550 )
    # notes: Extra note field (optional)
    notes = CharField( null=True,  max_length = 550 )
    # creation_date: Automatic date of order creation
    creation_date = DateField(default = datetime.datetime.now().date())
    # created_by: User who created this order (automatically captured)
    created_by    = ForeignKeyField(User, null= True,to_field="username",on_delete='SET NULL')
    # issue_date: Date the order was issued
    issue_date = DateField(null = True)
    # complete_date: Date the order was completed
    complete_date = DateField(null = True)
    # responsible: User (or group) responsible for managing the order
    created_by    = ForeignKeyField(User, null= True,to_field="username",on_delete='SET NULL')
    
class PurchaseOrder( Order):
        # supplier: Reference to the company supplying the goods in the order
    supplier = CharField(   max_length = 550 )
        # supplier_reference: Optional field for supplier order reference code
    supplier_reference = CharField(   max_length = 550 )
        # received_by: User that received the goods
    received_by    = ForeignKeyField(User, null= True,to_field="username",on_delete='SET NULL')
        # target_date: Expected delivery target date for PurchaseOrder completion (optional)
    target_date = DateField(null = True)
    
class SalesOrder( Order):
    # order reference
    reference  = CharField(   unique=True,null= False, max_length = 550 )
    # add customer

class OrderLineItem(BaseModel):
    quantity  = FloatField(default = 1.0)
    reference = CharField( max_length=100, null = True)
    target_date = DateField(null = True)
    description = CharField(max_length=250, null = True)
    
class PurchaseOrderLineItem(OrderLineItem):
    order = ForeignKeyField(PurchaseOrder,on_delete='CASCADE')
    part = ForeignKeyField(Part_nr,on_delete='CASCADE')
    #quantity reversed
    received = FloatField(default = 0.0)
    destination = ForeignKeyField(StockLocation, null= True, on_delete= 'SET NULL')

class SaleOrderLineItem(OrderLineItem):
    shipped = FloatField(default = 0.0)
    part = ForeignKeyField(Part_nr,on_delete='CASCADE')

db.create_tables([PurchaseOrder,SalesOrder,PurchaseOrderLineItem,SaleOrderLineItem])