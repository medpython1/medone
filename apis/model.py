from mongoengine import *

class sre_pdf_create_bill(Document):
    sno=ImageField()
    invoice_num=StringField()
    vechile_num=StringField()
    eway=StringField()
    po_number=StringField()
    po_date=StringField()
    Bill_company_mame=StringField()
    address=StringField()
    bill_gst=StringField()
    Description=ListField(StringField())
    Hsn_code=ListField(StringField())
    Quantity=ListField(FloatField())
    Uom=ListField(StringField())
    Rate=ListField(FloatField())
    Amount=ListField(StringField())
    CGST=FloatField()
    SGST=FloatField()
    # IGST=FloatField()
    Total_amount=FloatField()
    
    

class Barcode(Document):
    Department =StringField()
    name =StringField()
    date =StringField()
    umr =StringField()
    Sample_number =StringField()
    Gender =StringField()
    Age =StringField()
    BillNo =StringField()
    testname =StringField()
    pdf_file_name =StringField()
    
class Barcode1(Document):
    Department =ListField(StringField())
    name =StringField()
    date =StringField()
    umr =StringField()
    Sample_number =StringField()
    Gender =StringField()
    Age =StringField()
    BillNo =StringField()
    testname =ListField(StringField())
    pdf_file_name =StringField()

class Category(Document):
    sno=IntField()
    Category_name=StringField()

class Title_tags(Document):
    sno=IntField()
    Title_name=StringField()

class Unique_Reg(Document):
    sno=IntField(required=True)
    unique_num=StringField(unique=True)
    category=StringField()
    First_name=StringField(required=True)
    Middle_name=StringField()
    Sur_name=StringField()
    Gender=StringField(required=True)
    Date_of_birth=StringField(required=True)
    Age=StringField(required=True)
    Blood_group=StringField()
    Contact_number=StringField(unique=True)
    Email=StringField()
    Alternative_number=StringField()
    emergency_number=StringField()
    Gardeian_name=StringField()
    Nationality=StringField(required=True)
    State=StringField()
    city=StringField(required=True)
    Area=StringField(required=True)
    Address =StringField(required=True)
    Pin_Code=StringField()
    ID_Proof=StringField()
    ID_Proof_no=StringField()
    Remarks=StringField()
    created_on=DateTimeField()

class service_master(Document):
    sno=IntField()
    service_code=StringField(unique=True)
    service_name=StringField()
    service_category=StringField()
    service_sub_category=StringField()
    Department=StringField()
    Bill_head=StringField()
    price=FloatField()
    service_group_code=StringField()
    Vaccutainer=StringField()
    sample_type=StringField()
    category=StringField()
    branch=StringField()
    Turn_around_time=StringField()

class Billing_depat(Document):
    sno=IntField()
    Invoice_number=StringField(unique=True)
    Patient_name=StringField()
    age=IntField()
    umr=StringField()
    Doctor_name=StringField()
    mobile_number=StringField()
    created_on=DateTimeField()
    service_name=ListField()
    discount=ListField(FloatField())
    price=ListField(FloatField())
    after_discount=ListField(FloatField())
    total_discount=FloatField()
    payment_mode=ListField(StringField())
    sum_of_total=FloatField()
    cash=FloatField()
    card=FloatField()
    upi=FloatField()
    created_by=StringField()

class Package_master(Document):
    sno=IntField()
    package_id=StringField()
    package_type=StringField()
    package_name=StringField()
    package_cost=FloatField()
    package_original_cost=FloatField()
    gender=StringField()
    Age=IntField()
    spoonser_type=StringField()
    created_on=DateTimeField()
    packagee_vailed_date=DateTimeField()
    status=StringField()
    approved_by=StringField()
    approved_on=DateTimeField()
    package_terms_and_condtions=StringField()
    created_ip_address=StringField()
    created_host_address=StringField()
    branch=StringField()



class Package_list(Document):
    sno=IntField()
    package_id=StringField()
    package_name=StringField()
    package_categrory=StringField()
    service_code=StringField(unique=True)
    service_name=StringField(unique=True)
    service_department=StringField()
    service_cost=FloatField()
    created_by=StringField()
    created_on=DateTimeField()
    modified_by=StringField()
    modified_on=DateTimeField()
    status=StringField()
    created_ip_address=StringField()
    created_host_address=StringField()
    branch=StringField()











