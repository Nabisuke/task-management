from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import *
from datetime import date
from django.db.models import Q,Count
from django.contrib import messages

# Create your views here.

def manager_dashboard(request):
    

    #getting task count
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()

    # count = {
    #     "total_task":
    #     "completed_task":
    #     "in_progress_task":
    #     "pending_task":
    # }
    type = request.GET.get('type', 'all')

    

    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')))

    #retreiving task data
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')  
    elif type == 'all':
        tasks = base_query.all()                         

    context = {
        "tasks": tasks,
        "counts": counts
    }
    return render(request, "dashboard/manager-dashboard.html", context)

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    names = ["Mahmud", "Ahamed", "John", "Mr. X"]
    count = 0
    for name in names:
        count += 1
    context = {
        "names": names,
        "age": 23,
        "count": count
    }
    return render(request, 'test.html', context)

def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm() #For GET
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":
        # form = TaskModelForm(request.POST)   
        task_form = TaskModelForm(request.POST) #For GET
        task_detail_form = TaskDetailModelForm(request.POST)    
        if task_form.is_valid() and task_detail_form.is_valid():

            # for model form data
            task = task_form.save()
            task_detail= task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task created successfully")
            return redirect('create-task')

        # for Django Form Data
        #     data = form.cleaned_data
        #     title = data.get('title')
        #     description = data.get('description')
        #     due_date = data.get('due_date')
        #     assigned_to = data.get('assigned_to') #list [1,3]

        #     task = Task.objects.create(title=title,description=description,due_date=due_date)
        #     for emp_id in assigned_to:
        #         employee = Employee.objects.get(id=emp_id)
        #         task.assigned_to.add(employee)

            # return HttpResponse("Task Created Successfully")

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


def update_task(request,id):
    # employees = Employee.objects.all()
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) #For GET

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        # form = TaskModelForm(request.POST)   
        task_form = TaskModelForm(request.POST, instance=task) #For GET
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)    
        if task_form.is_valid() and task_detail_form.is_valid():

            # for model form data
            task = task_form.save()
            task_detail= task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated successfully")
            return redirect('update-task', id)

        # for Django Form Data
        #     data = form.cleaned_data
        #     title = data.get('title')
        #     description = data.get('description')
        #     due_date = data.get('due_date')
        #     assigned_to = data.get('assigned_to') #list [1,3]

        #     task = Task.objects.create(title=title,description=description,due_date=due_date)
        #     for emp_id in assigned_to:
        #         employee = Employee.objects.get(id=emp_id)
        #         task.assigned_to.add(employee)

            # return HttpResponse("Task Created Successfully")

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)

def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager-dashboard')




def view_task(request):
    # All tasks
    tasks = Task.objects.all()

    # Single task with id=1
    try:
        task_1 = Task.objects.get(id=1)
    except Task.DoesNotExist:
        task_1 = None

    # Tasks with status "PENDING"
    task_2 = Task.objects.filter(status="PENDING")

    # First task
    first_task = Task.objects.first()

    # Tasks whose due date is today
    today_task = Task.objects.filter(due_date=date.today())

    # TaskDetail with priority not LOW
    priority_task = TaskDetail.objects.exclude(priority='L')

    #query for show the task that contains word 'c'
    tasks_with_c = Task.objects.filter(title__icontains="c")

    # New query for PENDING or IN_PROGRESS
    tasks_pending_or_inprogress = Task.objects.filter(
        Q(status='PENDING') | Q(status='IN_PROGRESS')
    )
    # QuerySet method that returns True or False
    exists_or_not = Task.objects.filter(status='PENDING').exists()

    #select_related (ForeignKey, OneToOneField)
    task_details = TaskDetail.objects.select_related('task').all()

    #prefetch_related
    task_assigned_to = Task.objects.prefetch_related('assigned_to').all()

    #aggregations
    total_counts = Task.objects.aggregate(
    total=Count('id'),
    pending=Count('id', filter=Q(status='PENDING')),
    inprogress=Count('id', filter=Q(status='IN_PROGRESS'))
    )

    #annotation
    no_of_employee = Task.objects.annotate(num_employees=Count('assigned_to'))


    context = {
        "tasks": tasks,
        "task_1": task_1,
        "task_2": task_2,
        "first_task": first_task,
        "today_task": today_task,
        "priority_task": priority_task,
        "tasks_with_c": tasks_with_c,
        "tasks_pending_or_inprogress": tasks_pending_or_inprogress,
        "exists_or_not": exists_or_not,
        "task_details": task_details,
        "task_assigned_to": task_assigned_to,
        "total_counts": total_counts,
        "no_of_employee": no_of_employee

    }

    return render(request, "show_task.html", context)


