import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

import razorpay
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.utils.dateparse import parse_datetime

# Create your views here.
from hair_app.models import *


def home(request):
    return render(request,"index.html")
def login(request):
    return render(request,"loginindex.html")



def logincode(request):
    username = request.POST.get('mail')
    pwd = request.POST.get('Password')

    # Check if username and password match
    ob = login_table.objects.filter(username=username, password=pwd)

    if ob.exists():
        ob1 = login_table.objects.get(username=username, password=pwd)
        request.session['lid'] = ob1.id

        if ob1.type == 'admin':
            return redirect('/adminhome')

        elif ob1.type == 'user':
            ob = user_table.objects.get(LOGINID__id=ob1.id)
            request.session['uname'] = ob.name
            request.session['image'] = ob.photo.url
            return redirect('/userhome')

        elif ob1.type == 'employee':
            ob = employee_table.objects.get(loginid__id=ob1.id)
            request.session['uname'] = ob.name
            request.session['image'] = ob.photo.url
            return redirect('/employee')

        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('/login')

    else:
        # Add an error message when credentials don't match
        messages.error(request, "Invalid username or password.")
        return redirect('/login')


def adminhome(request):
    return render(request,"admin/adminhome1.html")

def adminadd_employee(request):
    from django.shortcuts import render, redirect
    from django.contrib import messages

    def adminadd_employee(request):
        if request.method == 'POST':
            messages.success(request, 'Employee successfully added!')
            return redirect('admin/Admin_add_employee.html')  # Redirect to another page after submission

        return render(request, "admin/Admin_add_employee.html")

    return render(request,"admin/Admin_add_employee.html")

def employee(request):
    kk=employee_table.objects.get(loginid__id=request.session['lid'])
    return render(request, 'employee/emphome.html',{"name":kk.name,"img":kk.photo})


def registration(request):
    return render(request,"Registration/reg.html")

def registration_post(request):
    name=request.POST["first_name"]
    dob=request.POST["dob"]
    phone=request.POST["phone_number"]
    gender=request.POST["gen"]
    email=request.POST["email"]
    photo=request.FILES["file"]
    passw=request.POST["password"]

    fs=FileSystemStorage()
    fsave=fs.save(photo.name,photo)

    if login_table.objects.filter(username=email).exists():
        already = True
        return render(request, "Registration/reg.html", {'already': already})

    lg=login_table()
    lg.username=email
    lg.password=passw
    lg.type="user"
    lg.save()

    ob=user_table()
    ob.LOGINID=lg
    ob.name=name
    ob.phone=phone
    ob.gender=gender
    ob.dob=dob
    ob.email=email
    ob.photo=fsave
    ob.save()

    return HttpResponse('''
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    Swal.fire({
                        icon: 'success',
                        title: 'Successfully Registered!',
                        confirmButtonText: 'OK',
                        reverseButtons: true
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location = '/login';
                        }
                    });
                });
            </script>
        ''')


def manage_services(request):
    ob=services_table.objects.all()
    for i in ob:
        t=int(i.Duration)
        tt=""
        h=t//60
        if h>0:
            tt=str(h)+" Hour "
        m=t%60
        if m>0:
            tt+=str(m)+" Minutes"
        i.t=tt
    return render(request,'admin/manage services.html',{'values':ob})







def userhome(request):
    ll=user_table.objects.get(LOGINID__id=request.session['lid'])
    request.session['p']=ll.photo.url
    return render(request, "users/userhome.html",{"name":ll.name,"img":ll.photo})


def view_services(request):
    service = services_table.objects.all()
    return render(request, 'users/services.html',{'service':service})

def view_type(request,type):
    types = services_table.objects.filter(type=type)
    return render(request, 'users/services.html',{'types':types})


def employeehome(request):
    return render(request, "employee/emphome.html")




def manage_emp(request):
    ob=employee_table.objects.all()
    return render(request,'admin/manage employee.html',{'values':ob})

def add_emp(request):
    return render(request,'admin/add emp.html')

def add_empp(request):
    print(request.POST,"jhhhhhhhhhhhhh")
    name = request.POST['textfield']
    phone = request.POST['textfield2']
    experience = request.POST['textfield3']
    Employee_type = request.POST['Employee_type']
    language=request.POST['textfield6']
    uname = request.POST['textfield4']
    pwrd = request.POST['textfield5']
    photo = request.FILES['file']
    fs = FileSystemStorage()
    fn = fs.save(photo.name, photo)

    login = login_table.objects.filter(username=uname)
    if login.exists():
        return HttpResponse('''
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        Swal.fire({
                            icon: 'error',  
                            title: 'Username Already exist',
                            confirmButtonText: 'OK',
                            reverseButtons: true
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location = '/add_emp';
                            }
                        });
                    });
                </script>
            ''')

    m = login_table()
    m.username=uname
    m.password=pwrd
    m.type="employee"
    m.save()

    emp_obj = employee_table()
    emp_obj.loginid = m
    emp_obj.name = name
    emp_obj.phone = phone
    emp_obj.experience = experience
    emp_obj.language=language
    emp_obj.Employee_type=Employee_type
    emp_obj.photo = fn
    emp_obj.save()
    return HttpResponse('''
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    Swal.fire({
                        icon: 'success',
                        title: 'Successfully Added!',
                        confirmButtonText: 'OK',
                        reverseButtons: true
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location = '/manage_emp';
                        }
                    });
                });
            </script>
        ''')



def add_serv(request):
    return render(request,'admin/add services.html')

def add_services(request):
    name = request.POST['name']
    phone = request.POST['details']
    type = request.POST['type']
    experience = request.POST['cost']
    category=request.POST['category']
    du=request.POST['du']
    photo = request.FILES['file']
    fs = FileSystemStorage()
    fn = fs.save(photo.name, photo)
    emp_obj = services_table()
    emp_obj.name = name
    emp_obj.description = phone
    emp_obj.Duration = du
    emp_obj.cost = experience
    emp_obj.category=category
    emp_obj.type=type
    emp_obj.photo = fn
    emp_obj.save()
    return HttpResponse('''
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    Swal.fire({
                        icon: 'success',
                        title: 'Service added successfully',
                        confirmButtonText: 'OK',
                        reverseButtons: true
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location = '/manage_services#stats';
                        }
                    });
                });
            </script>
        ''')




def edit_emp(request,id):
    request.session['id'] = id
    obj = employee_table.objects.get(id=id)
    return render(request,'admin/emp-edit.html',{'i':obj})

def edit_empp(request):
    try:
        name = request.POST['textfield']
        phone = request.POST['textfield2']
        Employee_type = request.POST['Employee_type']
        photo = request.FILES['file']
        fs=FileSystemStorage()
        fn=fs.save(photo.name,photo)
        experience = request.POST['textfield3']
        language=request.POST['textfield4']
        a = employee_table.objects.get(id=request.session['id'])
        a.name = name
        a.phone = phone
        a.photo = fn
        a.experience = experience
        a.Employee_type = Employee_type
        a.language = language
        a.save()
        return HttpResponse('''
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        Swal.fire({
                            icon: 'success',
                            title: 'Successfully Updated!',
                            confirmButtonText: 'OK',
                            reverseButtons: true
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location = '/edit_emp';
                            }
                        });
                    });
                </script>
            ''')
    except:
        name = request.POST['textfield']
        phone = request.POST['textfield2']
        Employee_type = request.POST['Employee_type']
        experience = request.POST['textfield3']
        language = request.POST['textfield4']
        a = employee_table.objects.get(id=request.session['id'])
        a.name = name
        a.phone = phone
        a.experience = experience
        a.Employee_type = Employee_type
        a.language = language
        a.save()

        return HttpResponse('''
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        Swal.fire({
                            icon: 'success',
                            title: 'Successfully Edited',
                            confirmButtonText: 'OK',
                            reverseButtons: true
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location = '/manage_emp#stats';
                            }
                        });
                    });
                </script>
            ''')


def delete(request, id):
    obj=employee_table.objects.get(id=id)
    obj.delete()
    return HttpResponse('''
    
                      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                      <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                      <script>
                          document.addEventListener("DOMContentLoaded", function() {
                              Swal.fire({
                                  icon: 'success',
                                  title: ' Successfully Deleted!',
                                  text: '.',
                                  confirmButtonText: 'OK',
                                  cancelButtonText: 'CLOSE',
                                  showCancelButton: true,
                                  reverseButtons: true
                              }).then((result) => {
                                  if (result.isConfirmed) {
                                      window.location = '/manage_emp';
                                  } else {
                                      // Handle close button action if needed
                                  }
                              });
                          });
                      </script>''')


def deleteservices(request, id):
    obj = services_table.objects.get(id=id)
    obj.delete()
    return HttpResponse('''
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
            <script>
                document.addEventListener("DOMContentLoaded", function() {
                    Swal.fire({
                        icon: 'success',
                        title: 'Successfully Deleted',
                        confirmButtonText: 'OK',
                        reverseButtons: true
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location = '/manage_services#stats';
                        }
                    });
                });
            </script>
        ''')

    # return HttpResponse('''
    #
    #                   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
    #                   <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
    #                   <script>
    #                       document.addEventListener("DOMContentLoaded", function() {
    #                           Swal.fire({
    #                               icon: 'success',
    #                               title: ' Successfully Updated!',
    #                               text: ,
    #                               confirmButtonText: 'ok',
    #                               cancelButtonText: 'Close',
    #                               showCancelButton: true,
    #                               reverseButtons: true
    #                           }).then((result) => {
    #                               if (result.isConfirmed) {
    #                                   window.location = '/manage_services';
    #                               } else {
    #                                   // Handle close button action if needed
    #                               }
    #                           });
    #                       });
    #                   </script>''')


def checkemail(request):

    username  = request.GET['email']
    print(username)
    data = {
        'is_taken': login_table.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message']="A user with this email already exists."

        # return HttpResponse("A user with this username already exists.")
    return JsonResponse(data)

def viewpro(request):
    ob=employee_table.objects.get(loginid__id=request.session['lid'])
    return render(request,"employee/viewpro.html",{"i":ob})


def service(request):
    ob=services_table.objects.all()
    return render(request,"users/services.html",{"i":ob})

def bill(request,id):
    cart_master = BookingMaster.objects.filter(id=id).first()
    cart_items = BookingSub.objects.filter(BOOKING_MASTER=cart_master) if cart_master else []
    total = cart_master.amount if cart_master else 0
    total_duration_minutes = 0
    for item in cart_items:
        total_duration_minutes += int(item.price)  # Assuming Duration is stored in minutes


    # Fetch employee list for selection in the form
    emp = employee_table.objects.all()
    return render(request,"users/bill.html",{"items":cart_items,"tt":total_duration_minutes,"id":cart_master.id,"d":cart_master.date})

def search_service(request,type):
    print(type,"===========================")
    ob=services_table.objects.filter(category=type)
    return render(request,"users/services.html",{"jj":ob})


def book_service(request, service_id):
    service = get_object_or_404(services_table, id=service_id)
    return render(request, 'users/book_service.html', {'service': service})

def add_to_cart(request,id):
    user = user_table.objects.get(LOGINID_id=request.session['lid'])
    service = services_table.objects.get(id=id)
    master = BookingMaster.objects.filter(USER_id=user,status='cart').first()
    if not master:
        master = BookingMaster(
            USER=user,
            date=datetime.now(),
            amount=0,
            status='cart'
        )
        master.save()
    booking_sub = BookingSub.objects.filter(BOOKING_MASTER=master, SERVICE=service).first()
    if not booking_sub:
        booking_sub = BookingSub(
            BOOKING_MASTER=master,
            SERVICE=service,
            price=service.cost,
            status='pending'
        )
        booking_sub.save()
        master.amount += service.cost
        master.save()
        return HttpResponse('''
               <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
               <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
               <script>
                   document.addEventListener("DOMContentLoaded", function() {
                       Swal.fire({
                           icon: 'success',
                           title: 'Service Added To Cart',
                           confirmButtonText: 'OK',
                           cancelButtonText: 'CLOSE',
                           showCancelButton: true,
                           reverseButtons: true
                       }).then((result) => {
                           if (result.isConfirmed) {
                               window.location = '/service';
                           }
                       });
                   });
               </script>
           ''')
    else:
        return HttpResponse('''
                       <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                       <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                       <script>
                           document.addEventListener("DOMContentLoaded", function() {
                               Swal.fire({
                                   icon: 'success',
                                   title: 'Already in cart...',
                                   confirmButtonText: 'OK',
                                   cancelButtonText: 'CLOSE',
                                   showCancelButton: true,
                                   reverseButtons: true
                               }).then((result) => {
                                   if (result.isConfirmed) {
                                       window.location = '/service';
                                   }
                               });
                           });
                       </script>
                   ''')

    return redirect('/service')


def view_cart(request):
    cart_master = BookingMaster.objects.filter(USER__LOGINID_id=request.session['lid'], status='cart').first()
    cart_items = BookingSub.objects.filter(BOOKING_MASTER=cart_master) if cart_master else []
    total = cart_master.amount if cart_master else 0
    total_duration_minutes = 0
    for item in cart_items:
        total_duration_minutes += int(item.SERVICE.Duration)  # Assuming Duration is stored in minutes
    total_hours = total_duration_minutes // 60
    remaining_minutes = total_duration_minutes % 60

    # Fetch employee list for selection in the form
    emp = employee_table.objects.all()

    return render(request, 'users/cart.html', {
        'cart_items': cart_items,
        'emp': emp,
        'total': total,
        'total_hours': total_hours,
        'remaining_minutes': remaining_minutes,
        'cart_master':cart_master,
        "d":datetime.now().strftime("%Y-%m-%d")
    })


def view_cart1(request,id):
    user = user_table.objects.get(LOGINID_id=request.session['lid'])
    service = services_table.objects.get(id=id)
    master = BookingMaster.objects.filter(USER_id=user, status='dbook')
    for i in master:
        i.delete()

    master = BookingMaster.objects.filter(USER_id=user, status='dbook').first()
    if not master:
        master = BookingMaster(
            USER=user,
            date=datetime.now(),
            amount=0,
            status='dbook'
        )
        master.save()
    booking_sub = BookingSub.objects.filter(BOOKING_MASTER=master, SERVICE=service).first()
    if not booking_sub:
        booking_sub = BookingSub(
            BOOKING_MASTER=master,
            SERVICE=service,
            price=service.cost,
            status='pending'
        )
        booking_sub.save()
        master.amount += service.cost
        master.save()



    cart_master = BookingMaster.objects.filter(USER__LOGINID_id=request.session['lid'], status='dbook').first()
    cart_items = BookingSub.objects.filter(BOOKING_MASTER=cart_master) if cart_master else []
    total = cart_master.amount if cart_master else 0
    total_duration_minutes = 0
    for item in cart_items:
        total_duration_minutes += int(item.SERVICE.Duration)  # Assuming Duration is stored in minutes
    total_hours = total_duration_minutes // 60
    remaining_minutes = total_duration_minutes % 60

    # Fetch employee list for selection in the form
    emp = employee_table.objects.all()

    return render(request, 'users/cart1.html', {
        'cart_items': cart_items,
        'emp': emp,
        'total': total,
        'total_hours': total_hours,
        'remaining_minutes': remaining_minutes,
        'cart_master':cart_master,
        "d":datetime.now().strftime("%Y-%m-%d")
    })


from datetime import datetime, timedelta, time


def generate_timeslots(start_time=time(8, 0), end_time=time(20, 0), interval=30):
    slots = []
    current_time = datetime.combine(datetime.today(), start_time)
    end_time = datetime.combine(datetime.today(), end_time)

    while current_time < end_time:
        next_time = current_time + timedelta(minutes=interval)
        slots.append((current_time.time(), next_time.time()))
        current_time = next_time

    return slots


def get_timeslots_for_date(request):
    print(request.GET)
    sid=request.GET['employee_id']
    date=request.GET['date']
    tt=int(request.GET['th'])*60+int(request.GET['tm'])

    # Parse date to filter by
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()

    # Get booked slots for the employee on that date
    booked_slots = BookingMaster.objects.filter(
        EMPLOYEE_id=sid,
        date=selected_date
    ).values('From_time', 'To_time')

    # Generate all slots
    all_slots = generate_timeslots(interval=tt)

    # Filter available slots
    available_slots = []
    for start, end in all_slots:
        # Check if any booked slot overlaps with this time range
        if not any(start < b['To_time'] and end > b['From_time'] for b in booked_slots):
            available_slots.append(f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}")
    print(available_slots)
    return JsonResponse({'timeslots': available_slots})

    return JsonResponse({"task":"ok"})
def delete_cart(request,id):
    cart_item = BookingSub.objects.get(id=id)
    cart_item.delete()
    return redirect('/view_cart')

def convert_to_24_hour(time_str):
    # Convert "HH:MM AM/PM" to 24-hour "HH:MM:SS" format
    return datetime.strptime(time_str, "%I:%M %p").time()
def purchase_product(request):
    ob=BookingMaster.objects.get(USER__LOGINID=request.session["lid"],status="cart")
    request.session["bookid"]=ob.id
    date=request.POST['date']
    emp=request.POST['employee']
    ts=request.POST['ts'].split(" - ")

    ob.date=date
    ob.From_time=convert_to_24_hour(ts[0])
    ob.To_time=convert_to_24_hour(ts[1])
    ob.EMPLOYEE=employee_table.objects.get(id=emp)
    ob.save()

    return render(request,'users/confirm.html',{"booking":ob})
def purchase_product1(request):
    ob=BookingMaster.objects.get(USER__LOGINID=request.session["lid"],status="dbook")
    request.session["bookid"]=ob.id
    date=request.POST['date']
    emp=request.POST['employee']
    ts=request.POST['ts'].split(" - ")

    ob.date=date
    ob.From_time=convert_to_24_hour(ts[0])
    ob.To_time=convert_to_24_hour(ts[1])
    ob.EMPLOYEE=employee_table.objects.get(id=emp)
    ob.save()

    return render(request,'users/confirm1.html',{"booking":ob})
def confirm_page(request):
    btn=request.POST["btn"]
    print(btn)

    ob = BookingMaster.objects.get(USER__LOGINID=request.session["lid"], status="cart")
    # request.session["bookid"] = ob.id
    # if len(ob) > 0:
    #     obb = BookingSub.object.filter(BOOKING_MASTER=ob[0].id).update(status="purchased")
    #     BookingMaster.objects.get(id=ob[0].id).update(status="purchased")
    # else:
    #     pass
    print(btn)
    print(ob.amount)
    if btn=="Pay Full":
        print("fulll")
        return user_pay_proceed(request,ob.id,ob.amount)
    else:
        print("100")
        return user_pay_proceed(request, ob.id, 100)


def confirm_page1(request):
    btn=request.POST["btn"]
    print(btn)

    ob = BookingMaster.objects.get(USER__LOGINID=request.session["lid"], status="dbook")
    # request.session["bookid"] = ob.id
    # if len(ob) > 0:
    #     obb = BookingSub.object.filter(BOOKING_MASTER=ob[0].id).update(status="purchased")
    #     BookingMaster.objects.get(id=ob[0].id).update(status="purchased")
    # else:
    #     pass
    print(btn)
    print(ob.amount)
    if btn=="Pay Full":
        print("fulll")
        return user_pay_proceed(request,ob.id,ob.amount)
    else:
        print("100")
        return user_pay_proceed(request, ob.id, 100)




def user_pay_proceed(request, id, amt):
    request.session['rid'] = id
    request.session['pay_amount'] = str(amt).split(".")[0]
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create(
        {'amount':  str(amt).split(".")[0] + "00", 'currency': "INR", 'payment_capture': '1'})
    res = user_table.objects.get(LOGINID=request.session['lid'])

    # ob = BookingMaster.objects.get(id=request.session['rid'])
    # ob.status = 'paid'
    # ob.save()
    return render(request, 'users/UserPayProceed.html',
                  {'p': payment, 'val': res, "lid": request.session['lid'], "id": request.session['rid']})

def on_payment_success(request):
    request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']
    # var = auth.authenticate(username='admin', password='admin')
    # if var is not None:
    #     auth.login(request, var)
    # amt = request.session['pay_amount']
    print("payment========================")
    ob=Payment_table()
    ob.date=datetime.now().today().date()
    ob.time=datetime.now().today().time()

    ob1 = BookingMaster.objects.get(id=request.session['rid'])
    ob1.status = 'paid'
    ob1.save()

    ob.ORDER = ob1
    ob.status ='paid'
    ob.save()

    return HttpResponse('''
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        Swal.fire({
                            icon: 'success',
                            title: 'Order Confirmed... !',
                            confirmButtonText: 'OK',
                            reverseButtons: true
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location = '/userhome';
                            }
                        });
                    });
                </script>
            ''')


    # return HttpResponse('''<script>alert("Success! Thank you for your Contribution");window.location="/userhome"</script>''')

def jquryemployee_view(request,emid):
    obu = employee_table.objects.get(id=emid)



    return JsonResponse({"photo": obu.photo.url,"name": obu.name, "expe": obu.experience, "lang": obu.language})


def BookNow(request):
    if request.method == 'POST':
        booking_sub_id = request.POST.get('booking_sub_id')
        if not booking_sub_id:
            return redirect('view_cart')

        try:
            # Fetch the corresponding BookingSub (cart item)
            booking_sub = BookingSub.objects.get(id=booking_sub_id)

            # Get the selected employee from the form
            employee_id = request.POST.get('employee')
            employee = employee_table.objects.get(id=employee_id)

            # Get the appointment date and time from the form
            from_time_str = request.POST.get('from_time')  # datetime-local input
            from_time = parse_datetime(from_time_str)
            if not from_time:
                return redirect('view_cart')  # Handle invalid date input gracefully

            # Calculate the to_time by adding the service duration
            service_duration_minutes = int(booking_sub.SERVICE.Duration)
            to_time = from_time + timedelta(minutes=service_duration_minutes)

            # Create a new Cart entry with status 'waiting'
            booking = Cart(
                BOOKING_SUB=booking_sub,
                EMPLOYEE=employee,
                from_time=from_time,
                to_time=to_time,
                status='waiting'  # Booking status
            )
            booking.save()

            # Update the status of BookingSub to 'waiting'
            booking_sub.status = 'waiting'
            booking_sub.save()

            # Update the status of BookingMaster related to this BookingSub
            booking_master = booking_sub.BOOKING_MASTER
            if booking_master:
                booking_master.status = 'waiting'
                booking_master.save()

            # Redirect to the cart page after successful booking
            return redirect('view_cart')

        except BookingSub.DoesNotExist:
            # Handle the case where booking_sub_id is invalid
            return redirect('view_cart')

    # In case of GET or other non-POST requests, redirect to view cart
    return redirect('view_cart')

from django.shortcuts import render, redirect, get_object_or_404
from .models import user_table # Adjust to your user model


def block_user(request, id):
    user = login_table.objects.get(id=id)

    # Toggle block status
    user.type = 'blocked'
    user.save()

    # Redirect back to the manage users page
    return redirect('/manage_users')  # Replace with the actual URL name of the page


def unblock_user(request, id):
    user = login_table.objects.get(id=id)

    # Toggle block status
    user.type = 'user'
    user.save()

    # Redirect back to the manage users page
    return redirect('/manage_users')  # Replace with the actual URL name of the page


def manage_users(request):
    ob=user_table.objects.all()
    print(ob)
    return render(request,"admin/manage-users.html",{"val":ob})

def admin_view_complaint(request):
    a=Complaint.objects.all()
    return render(request,'admin/view complaints.html',{'val':a})

def admin_view_booking(request):
    a=Complaint.objects.all()
    return render(request,'admin/booking.html',{'val':a})


def admin_send_reply(request,id):
    a=Complaint.objects.get(id=id)
    return render(request,'admin/reply.html',{'data':a})

def admin_send_reply_post(request):
    id=request.POST['id']
    reply=request.POST['reply']
    a=Complaint.objects.get(id=id)
    a.Reply=reply
    a.save()
    return HttpResponse('''

                       <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                       <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                       <script>
                           document.addEventListener("DOMContentLoaded", function() {
                               Swal.fire({
                                   icon: 'success',
                                   title: ' Replied!',
                                   text: 'We will get back to you within 24hs ',
                                   confirmButtonText: 'OK',
                                   cancelButtonText: 'CLOSE',
                                   showCancelButton: true,
                                   reverseButtons: true
                               }).then((result) => {
                                   if (result.isConfirmed) {
                                       window.location = '/admin_view_complaint';
                                   } else {
                                       // Handle close button action if needed
                                   }
                               });
                           });
                       </script>''')





def edit_emp_pro(request):

    obj = employee_table.objects.get(loginid__id=request.session['lid'])
    return render(request,'employee/emp-edit.html',{'i':obj})



def usrviewpro(request):

    obj = user_table.objects.get(LOGINID__id=request.session['lid'])
    return render(request,'users/usrviewpro.html',{'i':obj})

def men_services(request):
    if request.method == 'GET':
        # Assuming you're fetching services related to Men from the database
        services = services_table.objects.filter(type='men')  # Replace `Service` with your model
        for i in services:

                t = int(i.Duration)
                tt = ""
                h = t // 60
                if h > 0:
                    tt = str(h) + " Hour "
                m = t % 60
                if m > 0:
                    tt += str(m) + " Minutes"
                i.t = tt
        print(services[0].t,"ttttttttttttttttttt")
        context = {
            'services': services
        }
        return render(request, 'users/men.html', context)


def women_services(request):
    if request.method == 'GET':
        # Fetch services where the type is 'women'
        services = services_table.objects.filter(type='women')
        for i in services:

            t = int(i.Duration)
            tt = ""
            h = t // 60
            if h > 0:
                tt = str(h) + " Hour "
            m = t % 60
            if m > 0:
                tt += str(m) + " Minutes"
            i.t = tt
        context = {
            'services': services
        }
        return render(request, 'users/women.html', context)

def kids_services(request):
     if request.method == 'GET':
        # Assuming you're fetching services related to Men from the database
        services = services_table.objects.filter(type='kids')  # Replace `Service` with your model
        for i in services:

            t = int(i.Duration)
            tt = ""
            h = t // 60
            if h > 0:
                tt = str(h) + " Hour "
            m = t % 60
            if m > 0:
                tt += str(m) + " Minutes"
            i.t = tt
        context = {
            'services': services
        }
        return render(request, 'users/kids.html', context)






from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import employee_table, login_table


def edit_empp1(request):
    try:
        # Retrieve data from the request
        name = request.POST['textfield']
        phone = request.POST['textfield2']
        experience = request.POST['textfield3']
        language = request.POST['textfield4']
        email = request.POST['email']

        # Get the employee record
        employee = employee_table.objects.get(loginid__id=request.session['lid'])

        # Update fields
        employee.name = name
        employee.phone = phone
        employee.experience = experience
        employee.language = language

        # Check if there's a photo file
        if 'file' in request.FILES:
            photo = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            employee.photo = filename

        # Update email from login_table
        login_record = login_table.objects.get(id=request.session['lid'])
        login_record.username = email  # Assuming you want to change username to email
        login_record.save()

        # Save employee record
        employee.email = email
        employee.save()

        return generate_success_response()

    except Exception as e:
        # Log the error or handle it as needed

        # Fallback to update without photo
        try:
            name = request.POST['textfield']
            phone = request.POST['textfield2']
            experience = request.POST['textfield3']
            language = request.POST['textfield4']
            email = request.POST['email']
            employee = employee_table.objects.get(loginid__id=request.session['lid'])

            employee.name = name
            employee.phone = phone
            employee.experience = experience
            employee.language = language
            employee.email = email
            employee.save()

            return generate_success_response()

        except Exception as e:
            return HttpResponse("An error occurred while updating your profile.", status=500)


def generate_success_response():
    return HttpResponse('''
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                Swal.fire({
                    icon: 'success',
                    title: 'Successfully Updated!',
                    confirmButtonText: 'OK',
                    cancelButtonText: 'CLOSE',
                    showCancelButton: true,
                    reverseButtons: true
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location = '/viewpro';
                    }
                });
            });
        </script>
    ''')


def edit_user_profile(request):
    profile = user_table.objects.get(LOGINID__id=request.session['lid'])
    return render(request, 'users/user-edit.html',{'profile':profile})

def edit_profile_post(request):
    profile_name = request.POST['profile_name']
    phone = request.POST['phone']
    dob = request.POST['dob']
    email = request.POST['email']
    kk=login_table.objects.get(id=request.session['lid'])
    kk.username=email
    kk.save()
    profile = user_table.objects.get(LOGINID__id=request.session['lid'])
    if 'file' in request.FILES:
        file = request.FILES['file']
        fs = FileSystemStorage()
        fp = fs.save(file.name,file)
        profile.photo = fp
        profile.save()

    profile.name = profile_name
    profile.phone = phone
    profile.email = email
    profile.dob = dob
    profile.save()
    login = login_table.objects.get(id=request.session['lid'])
    login.username = email
    login.save()
    return HttpResponse('''

                   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                   <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                   <script>
                       document.addEventListener("DOMContentLoaded", function() {
                           Swal.fire({
                               icon: 'success',
                               title: ' Successfully Updated!',
                               text: '',
                               confirmButtonText: 'OK',
                               cancelButtonText: 'CLOSE',
                               showCancelButton: true,
                               reverseButtons: true
                           }).then((result) => {
                               if (result.isConfirmed) {
                                   window.location = '/usrviewpro';
                               } else {
                                   // Handle close button action if needed
                               }
                           });
                       });
                   </script>''')

    # return redirect('/')

def forgot_password_post(request):
    un=request.POST['mail']
    try:
        ob=login_table.objects.get(username=un)

        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('abhinandv848@gmail.com', 'jebp kifh doiz nowq')
            print("login=======")
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Your new password is : " + str(ob.password))
        print(msg)
        msg['Subject'] = 'TechBay'
        msg['To'] = un
        msg['From'] = 'abhinandv848@gmail.com'

        print("ok====")

        try:
            gmail.send_message(msg)
            return HttpResponse('''<script>alert("check your mail");window.location="/login"</script>''')


        except Exception as e:
            return HttpResponse('''<script>alert("Network error");window.location="/forgot_password"</script>''')



    except:

        return HttpResponse('''<script>alert("Invalid Username");window.location="/forgot_password"</script>''')



def forgot_password(request):

    return render(request,"fp.html")



def view_my_bookng(request):
    ob=BookingMaster.objects.filter(USER__LOGINID__id=request.session['lid'],status='paid').order_by("-date")
    for i in ob:
        obb=BookingSub.objects.filter(BOOKING_MASTER__id=i.id)
        i.sub=[]
        for j in obb:
            i.sub.append({"sn":j.SERVICE.name,"img":j.SERVICE.photo.url})
    return render(request,"users/my_booking.html",{"val":ob})
def submit_feedback(request):
    fbk=request.POST['review']
    rating=request.POST['rating']
    eid=request.POST['book_id']
    ob=Feedbacks()
    ob.date=datetime.today()
    ob.EMPLOYEE=employee_table.objects.get(id=eid)
    ob.USER=user_table.objects.get(LOGINID__id=request.session['lid'])
    ob.rating=rating
    ob.feedback=fbk
    ob.save()
    return redirect("/view_my_bookng")

def submit_complaint(request):
    fbk=request.POST['review']

    eid=request.POST['book_id']
    ob=Complaint()
    ob.date=datetime.today().date()
    ob.BOOKING=BookingMaster.objects.get(id=eid)

    ob.Complaint=fbk
    ob.Reply='pending'
    ob.save()
    return HttpResponse('''

                       <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                       <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                       <script>
                           document.addEventListener("DOMContentLoaded", function() {
                               Swal.fire({
                                   icon: 'success',
                                   title: ' Successfully Submitted!',
                                   text: 'We will get back to you within 24hs ',
                                   confirmButtonText: 'OK',
                                   cancelButtonText: 'CLOSE',
                                   showCancelButton: true,
                                   reverseButtons: true
                               }).then((result) => {
                                   if (result.isConfirmed) {
                                       window.location = '/view_my_bookng';
                                   } else {
                                       // Handle close button action if needed
                                   }
                               });
                           });
                       </script>''')


from django.shortcuts import render
from .models import BookingMaster, BookingSub

def admin_view_booking(request):
    # Check if session 'lid' exists and print it for debugging
    session_id = request.session.get('lid')
    if not session_id:
        print("Session ID is missing or not set.")
        return render(request, "admin/booking.html", {"val": []})

    print(f"Session ID: {session_id}")

    # Retrieve bookings where status is 'paid' for the current session user
    bookings = BookingMaster.objects.filter( status='paid').order_by("-date")
    print(f"Found {bookings.count()} bookings with status 'paid' for user ID {session_id}")

    # Initialize booking data
    booking_data = []

    # Loop through bookings to gather required details
    for booking in bookings:
        # Retrieve sub-bookings and gather service details
        services = BookingSub.objects.filter(BOOKING_MASTER=booking)
        print(f"Found {services.count()} services for Booking ID {booking.id}")

        # Organize services with names and images
        service_list = [
            {
                "sn": service.SERVICE.name,
                "img": service.SERVICE.photo.url if service.SERVICE.photo else None
            } for service in services
        ]

        # Append booking details to list
        booking_data.append({
            "booking_id": booking.id,
            "user_photo": booking.USER.photo.url if booking.USER.photo else None,
            "user_name": booking.USER.name,
            "employee_photo": booking.EMPLOYEE.photo.url if booking.EMPLOYEE and booking.EMPLOYEE.photo else None,
            "employee_name": booking.EMPLOYEE.name if booking.EMPLOYEE else "N/A",
            "services": service_list,
            "from_time": booking.From_time,
            "to_time": booking.To_time,
            "date": booking.date,
            "status": booking.status,
        })

    print("Booking Data Prepared:", booking_data)  # Debugging statement

    # Pass booking data to the template
    return render(request, "admin/booking.html", {"val": booking_data})


def searchbookingadmin(request):
    date = request.POST['date']
    employee_name = request.POST['employee_name']

    # Filter bookings based on search criteria
    bookings = BookingMaster.objects.all()
    if date:
        bookings = bookings.filter(date=date)
    if employee_name:
        bookings = bookings.filter(EMPLOYEE__name__icontains=employee_name)

    booking_data = []

    # Loop through bookings to gather required details
    for booking in bookings:
        # Retrieve sub-bookings and gather service details
        services = BookingSub.objects.filter(BOOKING_MASTER=booking)
        print(f"Found {services.count()} services for Booking ID {booking.id}")

        # Organize services with names and images
        service_list = [
            {
                "sn": service.SERVICE.name,
                "img": service.SERVICE.photo.url if service.SERVICE.photo else None
            } for service in services
        ]

        # Append booking details to list
        booking_data.append({
            "booking_id": booking.id,
            "user_photo": booking.USER.photo.url if booking.USER.photo else None,
            "user_name": booking.USER.name,
            "employee_photo": booking.EMPLOYEE.photo.url if booking.EMPLOYEE and booking.EMPLOYEE.photo else None,
            "employee_name": booking.EMPLOYEE.name if booking.EMPLOYEE else "N/A",
            "services": service_list,
            "from_time": booking.From_time,
            "to_time": booking.To_time,
            "date": booking.date,
            "status": booking.status,
        })

    print("Booking Data Prepared:", booking_data)  # Debugging statement

    # Pass booking data to the template
    return render(request, "admin/booking.html", {"val": booking_data,"d":date,"en":employee_name})


def admin_view_payments(request):
    ob=Payment_table.objects.filter(status='paid').order_by("-date")
    return render(request,"admin/view_payment.html",{"pay":ob})

def employee_view_shedule(request):
    ob = BookingMaster.objects.filter(EMPLOYEE__loginid__id=request.session['lid'], status='paid').order_by("-date")
    for i in ob:
        obb = BookingSub.objects.filter(BOOKING_MASTER__id=i.id)
        i.sub = []
        for j in obb:
            i.sub.append({"sn": j.SERVICE.name, "img": j.SERVICE.photo.url})

    return render(request, 'employee/view_booking.html', {"val": ob})


def employee_view_shedule_post(request):
    d=request.POST['d']
    ob = BookingMaster.objects.filter(EMPLOYEE__loginid__id=request.session['lid'], status='paid',date=d)
    for i in ob:
        obb = BookingSub.objects.filter(BOOKING_MASTER__id=i.id)
        i.sub = []
        for j in obb:
            i.sub.append({"sn": j.SERVICE.name, "img": j.SERVICE.photo.url})

    return render(request, 'employee/view_booking.html', {"val": ob,"d":d})
def user_view_reply(request):
    complaints=Complaint.objects.filter(BOOKING__USER__LOGINID__id=request.session['lid'])
    return render(request,"users/view_reply.html",{"complaints":complaints})



