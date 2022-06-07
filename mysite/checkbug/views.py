from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import escape
from datetime import datetime
from django.shortcuts import redirect
from sqlalchemy import null
from .models import userdata,customer,problem
from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
import random

def validatelogin(request):
    
 
 if 'user_id' not in request.session:  
    f = request.POST.get("company", "")
    s = request.POST.get("date", "")
    querry = (userdata.objects
    .values('id','Username','Password','IsEmploye')
    )
    
    for item in querry:
        id=item['id']
        username=item['Username']
        password=item['Password']
        employee=item['IsEmploye']
        if (username==f) and (password==s):
            request.session['user_id'] = id
            request.session['is_employee'] = employee
            if employee==0:
                return redirect('./client')
            else:return redirect('./programmer')
    return render(request, "login.html") 
 else:return redirect('/about/programmer')  
def customers(request):
  if 'user_id' in request.session:  
   if request.session['is_employee']==0:
    querry = (customer.objects
    .values('UID')
    .filter(UID=request.session['user_id'])
    )
    for item in querry:
        id=item['UID']
    request.session['user_id']
 
    query=(problem.objects
    .values('Topic','Description','Status','id')
    .filter(Customer_id=id)
    )
    return render(request, "client.html",{'query': query}) 
   else: return redirect('/about/programmer') 
  else:return redirect('/about/')
def logout(request):

    del request.session['user_id']
    del request.session['is_employee']
    return redirect('/about/')
    
def programmer(request):
  if 'user_id' in request.session:  
   if request.session['is_employee']==1:
    querry = (problem.objects.values('Customer__FirstName','Customer__LastName','Topic','Description','Status','Customer__UID__E_Mail','id').exclude(Status='Solved'))
    return render(request,"programmer.html",{'querry': querry})
   else: return redirect('/about/client') 
  else:return redirect('/about/')
def solution(request):
 if 'user_id' in request.session:
  if request.session['is_employee']==1:
    f = request.POST.get("date", )
    problem.objects.filter(id=f).update(Status=('In progress'))
    return redirect('/about/programmer')
  else: return redirect('/about/client')
 else:return redirect('/about/') 
def Solved(request):
 if 'user_id' in request.session:
  if request.session['is_employee']==1:
    f = request.POST.get("date", )
    problem.objects.filter(id=f).update(Status=('Solved'))
    return redirect('/about/programmer')
  else: return redirect('/about/client')
 else:return redirect('/about/')
def delete(request):
   f = request.POST.get("date", )
   problem.objects.filter(id=f).delete()
   return redirect('/about/client')
   
def edit(request):
  if request.method=='POST':
    f= request.POST.get("topic","")
    s= request.POST.get("description","")
    d= request.POST.get("id", )
    context= {  
        'topic': f,
        'description': s,
        'id': d
        }
    return render(request,'edit.html',context)
  else: return redirect('/about/client')
def fedit(request):


    problem.objects.filter(id=request.POST.get("id",)).update(Topic=(request.POST.get("topic","")),Description=(request.POST.get("description","")))
    return redirect('/about/client')
def insertdata(request):
  querry = (customer.objects
    .values('UID')
    .filter(UID=request.session['user_id'])
    )
  for item in querry:
    id=item['UID']
  request.session['user_id']
  f = request.POST.get("company", "")
  s = request.POST.get("date", "")
  if len(f)>0:
      problem.objects.create(Topic=f, Description=s, Status="Unchecked",Customer_id=id)
  return redirect('/about/client')