from io import BytesIO
from fastapi import FastAPI, HTTPException, Depends
from fastapi import Request
from barcode import *
from barcode.writer import ImageWriter
from barcode.errors import BarcodeError
from mongoengine import *
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
import os
from reportlab.pdfgen import canvas
import json
from apis.model import *
from apis.schema import *
from datetime import datetime
import socket
app = FastAPI()

# Connect to MongoDB
connect(db="Barcode", host="51.20.138.108", port=27017)
current_time = datetime.now()
 ## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)   


app.mount("/static", StaticFiles(directory="./apis/static"), name="static")

# Define a dependency to get the request object
def get_request(request: Request):
    return request

# @app.post("/generate_barcode_and_pdf/")
# async def generate_barcode_and_pdf(me:barcode, request: Request = Depends(get_request)):
#     Sample_number = "Barcode23045{:002d}".format(Barcode.objects.count()+1)
#     Department = me.Department
#     name = me.name
#     date = me.date
#     Age = me.Age
#     Gender = me.Gender
#     BillNo = me.BillNo
#     umr = me.umr
#     heading = f"Name: {name}\nAge: {Age} G: {Gender}      Bill No: {BillNo}\n"
#     heading +=f"Date: {date}\nUMR: {umr} ({Department})"

#     # Split the heading into lines to fit within the available space
#     heading_lines = []
#     max_line_length = 75  # Adjust as needed
#     for line in heading.split('\n'):
#         if len(line) <= max_line_length:
#             heading_lines.append(line)
#         else:
#             # If a line is longer than max_line_length, split it into multiple lines
#             words = line.split(' ')
#             current_line = ""
#             for word in words:
#                 if len(current_line + word) <= max_line_length:
#                     current_line += word + ' '
#                 else:
#                     heading_lines.append(current_line.strip())
#                     current_line = word + ' '
#             if current_line:
#                 heading_lines.append(current_line.strip())

   
#     # Combine data and heading into a single string for the barcode
#     barcode_data = f"{Sample_number}"
#     try:

#         # Generate barcode image
#         code_data = f"{barcode_data}"

#         # Create a PDF buffer
#         pdf_buffer = BytesIO()

#         # Create a PDF document with custom page size
#         custom_page_width = 80  # 80mm
#         custom_page_height = 25  # 35mm
#         c = canvas.Canvas(pdf_buffer, pagesize=(custom_page_width, custom_page_height))

#         # Draw the barcode image on the PDF
#         img_path = "temp_barcode.png"
#         code = Code128(code_data, writer=ImageWriter())  # Create barcode with ImageWriter
#         code_img = code.render(writer_options={"module_height": 10})  # Adjust barcode options as needed
#         code_img.save(img_path, dpi=(300, 300))  # Save the barcode image

#         c.drawImage(img_path, 12, custom_page_height - 27, width=60, height=15)  # Adjust position and size

#         # Add the wrapped heading lines to the PDF
#         c.setFont("Helvetica", 3)  # Adjust the font size as needed
#         line_height =3  # Adjust the line height as needed
#         for i, line in enumerate(heading_lines):
#             c.drawString(2, custom_page_height - 3 - i * line_height, line)

#         # Save the PDF to the buffer
#         c.showPage()
#         c.save()

#         # Save the buffer content as a PDF file
#         pdf_buffer.seek(0)
#         pdf_filename = f"barcode_{Sample_number}.pdf"
#         # pdf_filename1 = f"{uuid.uuid4()}"
#         pdf_filepath = os.path.join("./apis/static", pdf_filename)
#         with open(pdf_filepath, "wb") as pdf_file:
#             pdf_file.write(pdf_buffer.read())

#         # Construct the URL to the saved PDF
#         base_url = request.base_url
#         print(base_url)
#         pdf_return_path = f"{base_url.scheme}://{base_url.netloc}/static/{pdf_filename}"

#         create_barcode_details = Barcode1(
#             Department=me.Department, name=me.name, date=me.date, umr=me.umr,
#             Sample_number=Sample_number, Gender=me.Gender, Age=me.Age, BillNo=me.BillNo,
#             testname=me.testname, pdf_file_name=pdf_return_path
#         ).save()



#         # Save barcode data to MongoDB or any other desired storage

#         return {"data": Department, "name": name, "pdf_path": pdf_return_path}

#     except BarcodeError as e:
#         raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_barcode_and_pdf_for_multiple")
async def generate_barcode_and_pdf(me: barcode1, request: Request = Depends(get_request)):
    response_data = []

    for department,tests in zip(me.Department,me.testname):
        if all([department=="Biochemistry" and tests=="GLUCOSE FASTING (FBS), SODIUM FLUORIDE PLASMA"]):

            Sample_number = "Barcode23045{:002d}".format(Barcode1.objects.count() + 1)
            Department = department  # Set the department explicitly
            name = me.name
            date = me.date
            Age = me.Age
            Gender = me.Gender
            BillNo = me.BillNo
            umr = me.umr
        
            heading = f"Name: {name}\nAge: {Age} G: {Gender}      Bill No: {BillNo}\n"
            heading += f"Date: {date}\nUMR: {umr} ({Department}-FBS)"

            # Split the heading into lines to fit within the available space
            heading_lines = []
            max_line_length = 75  # Adjust as needed
            for line in heading.split('\n'):
                if len(line) <= max_line_length:
                    heading_lines.append(line)
                else:
                    # If a line is longer than max_line_length, split it into multiple lines
                    words = line.split(' ')
                    current_line = ""
                    for word in words:
                        if len(current_line + word) <= max_line_length:
                            current_line += word + ' '
                        else:
                            heading_lines.append(current_line.strip())
                            current_line = word + ' '
                    if current_line:
                        heading_lines.append(current_line.strip())

            # Combine data and heading into a single string for the barcode
            barcode_data = f"{Sample_number}"  # Set barcode_data based on department

            try:
                # Generate barcode image
                code_data = f"{barcode_data}"

                # Create a PDF buffer
                pdf_buffer = BytesIO()

                # Create a PDF document with custom page size
                custom_page_width = 80  # 80mm
                custom_page_height = 25  # 35mm
                c = canvas.Canvas(pdf_buffer, pagesize=(custom_page_width, custom_page_height))

                # Draw the barcode image on the PDF
                img_path = "temp_barcode.png"
                code = Code128(code_data, writer=ImageWriter())  # Create barcode with ImageWriter
                code_img = code.render(writer_options={"module_height": 10})  # Adjust barcode options as needed
                code_img.save(img_path, dpi=(300, 300))  # Save the barcode image

                c.drawImage(img_path, 12, custom_page_height - 27, width=60, height=15)  # Adjust position and size

                # Add the wrapped heading lines to the PDF
                c.setFont("Helvetica", 3)  # Adjust the font size as needed
                line_height = 3  # Adjust the line height as needed
                for i, line in enumerate(heading_lines):
                    c.drawString(2, custom_page_height - 3 - i * line_height, line)

                # Save the PDF to the buffer
                c.showPage()
                c.save()
                pdf_buffer.seek(0)
                pdf_filename = f"barcode_{Department}_{umr}.pdf"  # Modify the filename
                pdf_filepath = os.path.join("./apis/static", pdf_filename)
                with open(pdf_filepath, "wb") as pdf_file:
                    pdf_file.write(pdf_buffer.read())

                # Verify that the PDF file was successfully created
                if os.path.exists(pdf_filepath):
                    # Construct the URL to the saved PDF
                    base_url = request.base_url
                    pdf_return_path = f"{base_url.scheme}://{base_url.netloc}/static/{pdf_filename}"

                    # Clean up the temporary barcode image (optional)
                    if os.path.exists(img_path):
                        os.remove(img_path)
                    
                    create_barcode_details = Barcode1(
                        Department=[Department], name=name, date=date, umr=umr, Sample_number=Sample_number,
                        Gender=Gender, Age=Age, BillNo=BillNo, testname=[tests], pdf_file_name=pdf_return_path
                    ).save()

                    response_data.append({"data": Department, "name": name, "pdf_path": pdf_return_path})

                else:
                    raise HTTPException(status_code=500, detail="PDF file creation failed")
    
            except BarcodeError as e:
                raise HTTPException(status_code=400, detail=str(e))
            
        else:
            Sample_number = "Barcode23045{:002d}".format(Barcode1.objects.count() + 1)
            Department = department  # Set the department explicitly
            name = me.name
            date = me.date
            Age = me.Age
            Gender = me.Gender
            BillNo = me.BillNo
            umr = me.umr
        
            heading = f"Name: {name}\nAge: {Age} G: {Gender}      Bill No: {BillNo}\n"
            heading += f"Date: {date}\nUMR: {umr} ({Department})"

            # Split the heading into lines to fit within the available space
            heading_lines = []
            max_line_length = 75  # Adjust as needed
            for line in heading.split('\n'):
                if len(line) <= max_line_length:
                    heading_lines.append(line)
                else:
                    # If a line is longer than max_line_length, split it into multiple lines
                    words = line.split(' ')
                    current_line = ""
                    for word in words:
                        if len(current_line + word) <= max_line_length:
                            current_line += word + ' '
                        else:
                            heading_lines.append(current_line.strip())
                            current_line = word + ' '
                    if current_line:
                        heading_lines.append(current_line.strip())

            # Combine data and heading into a single string for the barcode
            barcode_data = f"{Sample_number}"  # Set barcode_data based on department

            try:
                # Generate barcode image
                code_data = f"{barcode_data}"

                # Create a PDF buffer
                pdf_buffer = BytesIO()

                # Create a PDF document with custom page size
                custom_page_width = 80  # 80mm
                custom_page_height = 25  # 35mm
                c = canvas.Canvas(pdf_buffer, pagesize=(custom_page_width, custom_page_height))

                # Draw the barcode image on the PDF
                img_path = "temp_barcode.png"
                code = Code128(code_data, writer=ImageWriter())  # Create barcode with ImageWriter
                code_img = code.render(writer_options={"module_height": 10})  # Adjust barcode options as needed
                code_img.save(img_path, dpi=(300, 300))  # Save the barcode image

                c.drawImage(img_path, 12, custom_page_height - 27, width=60, height=15)  # Adjust position and size

                # Add the wrapped heading lines to the PDF
                c.setFont("Helvetica", 3)  # Adjust the font size as needed
                line_height = 3  # Adjust the line height as needed
                for i, line in enumerate(heading_lines):
                    c.drawString(2, custom_page_height - 3 - i * line_height, line)

                # Save the PDF to the buffer
                c.showPage()
                c.save()
                pdf_buffer.seek(0)
                pdf_filename = f"barcode_{Department}_{umr}.pdf"  # Modify the filename
                pdf_filepath = os.path.join("./apis/static", pdf_filename)
                with open(pdf_filepath, "wb") as pdf_file:
                    pdf_file.write(pdf_buffer.read())

                # Verify that the PDF file was successfully created
                if os.path.exists(pdf_filepath):
                    # Construct the URL to the saved PDF
                    base_url = request.base_url
                    pdf_return_path = f"{base_url.scheme}://{base_url.netloc}/static/{pdf_filename}"

                    # Clean up the temporary barcode image (optional)
                    if os.path.exists(img_path):
                        os.remove(img_path)

                    create_barcode_details = Barcode1(
                        Department=[Department], name=name, date=date, umr=umr, Sample_number=Sample_number,
                        Gender=Gender, Age=Age, BillNo=BillNo, testname=[tests], pdf_file_name=pdf_return_path
                    ).save()

                    response_data.append({"data": Department, "name": name, "pdf_path": pdf_return_path})

                else:
                    raise HTTPException(status_code=500, detail="PDF file creation failed")

            except BarcodeError as e:
                raise HTTPException(status_code=400, detail=str(e))
            # except Exception as e:
            #     raise HTTPException(status_code=500, detail=str(e))
                # except Exception as e:
                #     raise HTTPException(status_code=500, detail=str(e))

    return response_data
            



















# class barcode_scan(BaseModel):
#     scaned_sampledata:str
# @app.post("/get_barcode_data")
# def get_barcode_data(me:barcode_scan):
    
#     a1=Barcode.objects(Sample_number=me.scaned_sampledata).to_json()
#     getting_data_from_database=json.loads(a1)
#     if getting_data_from_database:
#         list_compari=[{'Name':data_in_loop["name"],"Service_name":data_in_loop["testname"],"Barcode":data_in_loop["Sample_number"],"Date":data_in_loop["date"]} for data_in_loop in getting_data_from_database]
#         appending_data={"Error":"False","barcod_data":list_compari}
#         return appending_data

# ## create Category table
# @app.post("/create_category_table")
# def category_table(me:category_schema):
#     converting_first_letter_Capital= me.Category_name[:1].upper() + me.Category_name[1:]
#     storeing_category_data=Category(sno=Category.objects.count()+1,Category_name=converting_first_letter_Capital).save()
#     if storeing_category_data:
#         success_message={"Error":"False","Message":"Successfully Exicuted"}
#         return success_message   
#     else :
#         error_message={"Error":"True","Message":"Data Not Found"}
#         return JSONResponse(content=error_message, status_code=400)
# # getting data from data base                                                                                   
# @app.post("/getting_category_data")
# def retriveing_data():
#     getting_category_data=Category.objects()
#     if getting_category_data:
#         In_dic_format=[{"Category_name":loop_of_data["Category_name"]} for loop_of_data in getting_category_data]
#         appending_data={"Error":"False","Category_name":In_dic_format}
#         return appending_data
    
#     #creating title tags
# @app.post("/create_tags_data")
# def create_tag_title(me:tags_schema):
#     converting_first_letter_Capital= me.tag_name[:1].upper() + me.tag_name[1:]
#     storeing_tag_data=Title_tags(sno=Title_tags.objects.count()+1,Title_name=converting_first_letter_Capital).save()
#     if storeing_tag_data:
#         success_message={"Error":"False","Message":"Successfully Exicuted"}
#         return success_message   
#     else :
#         error_message={"Error":"True","Message":"Data Not Found"}
#         return JSONResponse(content=error_message, status_code=400)
    
# # Get the title tag from the databas
# @app.post("/get_title_tag")
# def get_title_tags():
    
#     query_for_geting_data=Title_tags.objects()
#     if query_for_geting_data:
#         In_dic_format=[{"Title_name":loop_of_data["Title_name"]} for loop_of_data in query_for_geting_data]
#         appending_data={"Error":"False","Title_name":In_dic_format}
#         return appending_data
#     else :
#         error_message={"Error":"True","Message":"Data Not Found"}
#         return JSONResponse(content=error_message, status_code=400)

# #create unique regi
# @app.post("/create_unique_regi")
# def reg_function(me:unique_reg):
#     current_time = datetime.now()
#     unique_number = "42302023{:002d}".format(Unique_Reg.objects.count()+1)
#     try:
#         if all([me.First_name!="",me.Gender!="",me.Date_of_birth!="",me.Age!="",me.Contact_number!="",me.Nationality!="",me.city!="",me.Area!="",me.Address!=""]):
#             createing_unique_reg_query=Unique_Reg(sno=Unique_Reg.objects.count()+1,unique_num=unique_number,category=me.category,First_name=me.First_name,Middle_name=me.Middle_name,Sur_name=me.Sur_name,Gender=me.Gender,Date_of_birth=me.Date_of_birth,Age=me.Age,Blood_group=me.Blood_group,Contact_number=me.Contact_number,Email=me.Email,Alternative_number=me.Alternative_number,emergency_number=me.emergency_number,Gardeian_name=me.Gardeian_name,Nationality=me.Nationality,State=me.State,city=me.city,Area=me.Area,Address=me.Address,Pin_Code=me.pincode,ID_Proof=me.ID_Proof,ID_Proof_no=me.ID_Proof_no,Remarks=me.Remarks,created_on=current_time).save()
#             if createing_unique_reg_query:
#                 success_message={"Error":"False","Message":"Successfully Exicuted"}
#                 return success_message   
#             else :
#                 error_message={"Error":"True","Message":"Data Not Found"}
#                 return JSONResponse(content=error_message, status_code=400)
#         else:
#             error_message={"Error":"True","Message":"please Enter mandatory fields"}
#             return JSONResponse(content=error_message, status_code=400)
#     except NotUniqueError:
#         error_message={"Message":"Duplicate Error"}
#         return JSONResponse(content=error_message, status_code=400)
# # geting data from data base

# @app.post("/getting_unique_data")
# def unique_data_fun(me:get_unique_data_based_on_date):
#     date_from=datetime.strptime(me.from_date,"%Y-%m-%d")
#     to_date=datetime.strptime(me.to_date,"%Y-%m-%d")
#     new_date_end= to_date + timedelta(days=1)
#     start_time1= datetime.combine(date_from, time(0, 00))
#     end_time1= datetime.combine(date_from, time(23,59))
#     if me.from_date!=me.to_date:
#         geting_unique_data_base=Unique_Reg.objects(created_on__gte=date_from,created_on__lt=new_date_end)
#     else:
#         geting_unique_data_base=Unique_Reg.objects(created_on__gte=start_time1,created_on__lte=end_time1)
#     if geting_unique_data_base:
#         In_dic_format=[{"sno":looping_data["sno"],"Name":looping_data["First_name"],"Middle_name":looping_data["Middle_name"],"Surname":looping_data["Sur_name"],"Age":looping_data["Age"]}for looping_data in geting_unique_data_base]
#         appending_data={"Error":"False","Umr_regi":In_dic_format}
#         return appending_data
#     else :
#         error_message={"Error":"True","Message":"Data Not Found"}
#         return JSONResponse(content=error_message, status_code=400)
    
#     #search data by useing umr_coloum and contact_number
       
# @app.post("/search_unique_data")
# def search_unique_fun(me:search_umr):
#     geeting_data_from_data_base=Unique_Reg.objects(Q(unique_num=me.search_data) | Q(Contact_number=me.search_data))
#     if geeting_data_from_data_base:
#         In_dic_format=[{"sno":looping_data["sno"],"Name":looping_data["First_name"],"Middle_name":looping_data["Middle_name"],"Surname":looping_data["Sur_name"],"Age":looping_data["Age"]}for looping_data in geeting_data_from_data_base]
#         appending_data={"Error":"False","Umr_regi":In_dic_format}
#         return appending_data
#     else :
#         error_message={"Error":"True","Message":"Data Not Found"}
#         return JSONResponse(content=error_message, status_code=400)
    
#     #create service master

# @app.post("/create_service_master")
# def service_mas_fun(me:service_master_schema):
#     service_code1= "SER{:003d}".format(service_master.objects.count()+1)
#     store_service_data=service_master(sno=service_master.objects.count()+1,service_code=service_code1,service_name=me.service_name,service_category=me.service_category,Department=me.Department,Bill_head=me.Bill_head,price=me.price,service_group_code=me.service_group_code,Vaccutainer=me.Vaccutainer,sample_type=me.sample_type,category=me.category,branch=me.branch,Turn_around_time=me.Turn_around_time).save()
#     if store_service_data:
#         success_message={"Error":"False","Message":"Successfully Exicuted"}
#         return success_message   
#     else :
#         error_message={"Error":"True","Message":"Data Not Found"}
#         return JSONResponse(content=error_message, status_code=400)
# # get service master data

# @app.post("/get_service_master")
# def get_service_mas_fun():
#     getting_service_data=service_master.objects()
#     if getting_service_data:
#         In_dic_format=[{"service_code":looping_data["service_code"],"Service_name":looping_data["service_name"],"Cost":looping_data["price"]}for looping_data in getting_service_data]
#         appending_data={"Error":"False","service_data":In_dic_format}
#         return appending_data
#     else :
#         error_message={"Error":"True","Message":"Data Not Found"}
#         return JSONResponse(content=error_message, status_code=400)
    
#Billing_idea
@app.post("/create_bill_history")
def create_bill_fun(me:bill_generate_schema):
    print(f"Total Discount: {me.total_discount}")
    print(f"Individual Discounts: {me.discount}")
    discounted_prices=[]
    current_time = datetime.now()
    Invoice_number_auto= "INV{:002d}".format(Billing_depat.objects.count()+1)
    if me.total_discount != 0 and me.discount == [0]:
    
        sum_of_prices=sum(me.price)
        discount_amount=sum_of_prices*(me.total_discount/100)
        ##doing subraction total test amount to discount amount
        Net_amount_is=sum_of_prices-discount_amount
        geeting_money_different_modes=(me.cash+me.card+me.upi)-Net_amount_is
        ##taking money from different modes like cash,card,upi
        if geeting_money_different_modes >=0:

            create_bill=Billing_depat(sno=Billing_depat.objects.count()+1,Invoice_number=Invoice_number_auto,Patient_name=me.patient_name,age=me.age,umr=me.umr,Doctor_name=me.doctor_name,mobile_number=me.mobile,service_name=me.service_name,created_on=current_time,created_by=me.created_by,price=me.price,discount=me.discount,after_discount=discount_amount)
            return {"Invoice":Invoice_number_auto,"Umr":me.umr,"Name":me.patient_name,"Age":me.age,"Mobile":me.mobile,"Services_name":me.service_name,"ToalAmount":sum_of_prices,"Discount_amount":discount_amount,"Net_amount":Net_amount_is,"Discount_type":"total"}
        else:
            error_message={"Error":"True","Message":f"Please pay balance amount {geeting_money_different_modes}"}
            return JSONResponse(content=error_message, status_code=400)

    elif me.total_discount == 0 and all(discount != 0 for discount in me.discount):
        sum_of_prices_is=sum(me.price)
        ##calculate percentage Indivisuval test for list items,
        for price, discount_percentage in zip(me.price, me.discount):
            ##discount Formula
            discount_amount = price * (discount_percentage / 100)
            print("discount",discount_amount)
            ##appending data
            discounted_prices.append(discount_amount)
            ##after discount calcualte total bill value
            after_discount_amount = [a - b for a, b in zip(me.price, discounted_prices)]
            after_indivisuval_discount_adding_total_bill=sum(after_discount_amount)
            print("sum of all",after_indivisuval_discount_adding_total_bill)
    #subract data total amount to different modes
            geeting_money_different_modes1=(me.cash+me.card+me.upi)-after_indivisuval_discount_adding_total_bill
            print(geeting_money_different_modes1)
    ##if paying amount is greather than the after_indivisuval_discount_adding_total_bill data
        if (geeting_money_different_modes1 >=0):
            create_bill=Billing_depat(sno=Billing_depat.objects.count()+1,Invoice_number=Invoice_number_auto,Patient_name=me.patient_name,age=me.age,umr=me.umr,Doctor_name=me.doctor_name,mobile_number=me.mobile,created_on=current_time,created_by=me.created_by,service_name=me.service_name,price=me.price,discount=me.discount,after_discount=after_discount_amount)
            return {"Invoice":Invoice_number_auto,"Umr":me.umr,"Name":me.patient_name,"Age":me.age,"Mobile":me.mobile,"Services_name":me.service_name,"Toatl_amount":sum_of_prices_is,"Discount_amount":sum(discounted_prices),"Net_amount":after_indivisuval_discount_adding_total_bill,"Cash":me.cash,"Card":me.card,"Upi":me.upi,"Discount_type":"Indivisuval"}
        else:
            error_message={"Error":"True","Message":f"Please pay balance amount {geeting_money_different_modes1}"}
            return JSONResponse(content=error_message, status_code=400)
    elif me.total_discount != 0 and all(discount != 0 for discount in me.discount):
            discount_prices=[]
            for price, discount_percentage in zip(me.price, me.discount):
            ##discount Formula
                discount_amount = price * (discount_percentage / 100)
            ##appending data
            discount_prices.append(discount_amount)
            ##after discount calcualte total bill value
            after_discount_amount = [a - b for a, b in zip(me.price, discount_prices)]
            after_indivisuval_discount_adding_total_bill=sum(after_discount_amount)
            total_all_test_discounts=after_indivisuval_discount_adding_total_bill*(me.total_discount/100)
            from_delete_bill_to_second_discount_amount=after_indivisuval_discount_adding_total_bill-total_all_test_discounts
            ##showing current amount after paying modes######
            showing_different_modes=(me.cash+me.card+me.upi)-from_delete_bill_to_second_discount_amount
            ####### importtant ##########
            if showing_different_modes >=0 :
                create_bill=Billing_depat(sno=Billing_depat.objects.count()+1,Invoice_number=Invoice_number_auto,Patient_name=me.patient_name,age=me.age,umr=me.umr,Doctor_name=me.doctor_name,mobile_number=me.mobile,created_on=current_time,created_by=me.created_by,service_name=me.service_name,price=me.price,discount=me.discount,after_discount=after_discount_amount)
                return {"Invoice":Invoice_number_auto,"Umr":me.umr,"Name":me.patient_name,"Age":me.age,"Mobile":me.mobile,"Services_name":me.service_name,"dou":"dou"}
            else:
                error_message={"Error":"True","Message":f"Please pay balance amount {showing_different_modes}"}
            return JSONResponse(content=error_message, status_code=400)

@app.post("/create_package_name")
def package_master_create_fun(me:package_master_schema):
    
    format = '%Y-%m-%d'
    # package_start_date = datetime.datetime.strptime(date_time, format)
    package_vaild_date= datetime.strptime(me.packagee_vailed_date, format)
   
    package_number_auto= "PACK{:00004d}".format(Package_master.objects.count()+1)
    create_pacakge_data=Package_master(sno=Package_master.objects.count()+1,package_id=package_number_auto,package_type=me.package_type,package_name=me.package_name,package_cost=me.package_cost,package_original_cost=me.package_original_cost,gender=me.gender,Age=me.Age,spoonser_type=me.spoonser_type,created_on=current_time,packagee_vailed_date=package_vaild_date,status="Pending",package_terms_and_condtions=me.package_terms_and_condtions,created_ip_address=ip_address,created_host_address=hostname,approved_by="",approved_on=current_time).save()
    return "done"
@app.post("/pacakge_approve_api")
def package_approved_fun(me:package_approved_scheam):
    current_time = datetime.now()
    update_package_status=Package_master.objects(package_id=me.package_id).update_one(set__approved_by=me.approved_by,set__status=me.status,set__approved_on=current_time)
    success_message="Succfully Updated"
    if success_message:
                    return {"Error":"False","Message":success_message}
    else:
        # return {"Error":"True","Message":"Data not found"}
        a={"Error":"True","Message":"Data not found"}
        return JSONResponse(content=a, status_code=400)
@app.post("/getting_package_data")
def getting_pack_data_all_modes():
    getting_data_from_data_base=Package_master.objects()
    if getting_data_from_data_base:
        from_dic=[{"package_id":dic_type_data["package_id"],"package_type":dic_type_data["package_type"],"package_name":dic_type_data["package_name"],"package_cost":dic_type_data["package_cost"],"status":dic_type_data["status"]} for dic_type_data in getting_data_from_data_base]
        appending_data={"Error":"False","service_data":from_dic}
        return appending_data
    else :
        error_message={"Error":"True","Message":"Data Not Found"}
        return JSONResponse(content=error_message, status_code=400)
@app.post("/get_data_only_approved_package")
def get_data_Approved_package_fun():
    getting_data_from_data_base=Package_master.objects(status="Approved")
    if getting_data_from_data_base:
        from_dic=[{"package_id":dic_type_data["package_id"],"package_type":dic_type_data["package_type"],"package_name":dic_type_data["package_name"],"package_cost":dic_type_data["package_cost"],"status":dic_type_data["status"]} for dic_type_data in getting_data_from_data_base]
        appending_data={"Error":"False","service_data":from_dic}
        return appending_data
    else :
        error_message={"Error":"True","Message":"Data Not Found"}
        return JSONResponse(content=error_message, status_code=400)
    
@app.post("/add_package_list_package")
def add_list_in_package_function(me:Package_list_schema):
    get_data_from_package_master=Package_master.objects(package_id=me.package_id)
    print(get_data_from_package_master)
    try:
        if get_data_from_package_master:
            for geting_data in get_data_from_package_master:
                package_name=geting_data["package_name"]
                package_categrory=geting_data["package_type"]
                create_package_list=Package_list(sno=Package_list.objects.count()+1,package_id=me.package_id,package_name=package_name,package_categrory=package_categrory,service_code=me.service_code,service_name=me.service_name,service_department=me.service_department,service_cost=me.service_cost,created_by=me.created_by,created_on=current_time,modified_by="",status="Active",created_ip_address=ip_address,created_host_address=hostname,branch=me.branch).save()
            success_message="Successfully Submitted"
            if success_message:
                        return {"Error":"False","Message":success_message}
            else:
                # return {"Error":"True","Message":"Data not found"}
                a={"Error":"True","Message":"Data not found"}
                return JSONResponse(content=a, status_code=400)
        else:
                # return {"Error":"True","Message":"Data not found"}
                a={"Error":"True","Message":"Data not found"}
                return JSONResponse(content=a, status_code=400)
    except NotUniqueError:
        a={"Error":"True","Message":"This service code is already existed"}
        return JSONResponse(content=a, status_code=400)
@app.post("/get_package_list_with_approved_data")
def get_package_data_with_approve(me:get_package_list_with_approved):
    get_data_from_package_master=Package_master.objects(package_id=me.package_id,status="Approved")
    if get_data_from_package_master:
        get_package_list=Package_list.objects(package_id=me.package_id)
        dic_format_data=[{"package_id":data_exa["package_id"],"package_name":data_exa["package_name"],"service_name":data_exa["service_name"],"Department":data_exa["service_department"]}for data_exa in get_package_list]
        appending_data={"Error":"False","package_list":dic_format_data}
        return appending_data
    else:
        a={"Error":"True","Message":"Data not found"}
        return JSONResponse(content=a, status_code=400)          




   

