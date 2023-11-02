from pydantic import BaseModel

class barcode(BaseModel):
    Department: str
    name: str
    date: str
    umr: str
    Gender: str
    Age: str
    BillNo: str
    testname: str
class barcode1(BaseModel):
    Department: list[str]
    name: str
    date: str
    umr: str
    Gender: str
    Age: str
    BillNo: str
    testname: list[str]
class category_schema(BaseModel):
    Category_name:str

class tags_schema(BaseModel):
    tag_name:str


class unique_reg(BaseModel):
    category:str
    First_name:str
    Middle_name:str
    Sur_name:str
    Gender:str
    Date_of_birth:str
    Age:str
    Blood_group:str
    Contact_number:str
    Email:str
    Alternative_number:str
    emergency_number:str
    Gardeian_name:str
    Nationality:str
    State:str
    city:str
    Area:str
    Address:str
    pincode:str
    ID_Proof:str
    ID_Proof_no:str
    Remarks:str
class get_unique_data_based_on_date(BaseModel):
    from_date:str
    to_date:str
class search_umr(BaseModel):
    search_data:str

class service_master_schema(BaseModel):
    service_name:str
    service_category:str
    service_sub_category:str
    Bill_head:str
    Department:str
    price:float
    service_group_code:str
    Vaccutainer:str
    sample_type:str
    category:str
    Turn_around_time:str
    branch:str

class bill_generate_schema(BaseModel):
    service_name:list
    patient_name:str
    age:int
    umr:str
    mobile:str
    doctor_name:str
    discount:list[float]
    price:list[float]
    total_discount:float
    cash:float
    card:float
    upi:float
    created_by:str

class package_master_schema(BaseModel):
    package_type:str
    package_name:str
    package_cost:float
    package_original_cost:float
    gender:str
    Age:int
    spoonser_type:str
    packagee_vailed_date:str
    package_terms_and_condtions:str
    branch:str

class package_approved_scheam(BaseModel):
    approved_by:str
    status:str
    package_id:str

class Package_list_schema(BaseModel):
    package_id:str
    service_code:str
    service_name:str
    service_department:str
    service_cost:float
    created_by:str
    branch:str

class get_package_list_with_approved(BaseModel):
    package_id:str

class sre_pdf_schema(BaseModel):
    vechile_num:str
    eway:str
    po_number:str
    po_date:str
    Bill_company_mame:str
    address:str
    bill_gst:str
    Description:list[str]
    Hsn_code:list[str]
    Quantity:list[float]
    Uom:list[str]
    Rate:list[float]
    CGST:float
    SGST:float
    # IGST:float
    











