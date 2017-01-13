from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from Database import DB
import csv

from models import Address, TaxiOrder, Car, Client


def initialize_database(request):
    Address.objects.initialize()
    Car.objects.initialize()
    Client.objects.initialize()
    database = DB()
    TaxiOrder.model.objects.all().delete()
    from django.db import connection
    cur = connection.cursor()
    cur.execute("ALTER TABLE taxi_order AUTO_INCREMENT = 1")
    with open('order.csv', 'rb') as csvfile:
        passengers = csv.reader(csvfile, quotechar=',')
        for pas in passengers:
            car = Car.objects.get(id=int(pas[2]))
            client = Client.objects.get(id=int(pas[3]))
            start = Address.objects.get(id=int(pas[0]))
            finish = Address.objects.get(id=int(pas[1]))
            database.saveOrder(start, finish, car, client, pas[4])

    return redirect('/')


def main(request):
    database = DB()
    list = database.getOrderList()
    car = database.getCarList()
    for elem in list:
        print elem
    return render(request, 'main_page.html', {'list': list, 'car': car})


def remove(request, id):
    database = DB()
    database.removeOrder(id)
    return redirect('/')


def edit(request, id):
    database = DB()
    if request.method == 'GET':
        address = database.getAddressList()
        car = database.getCarList()
        client = database.getClientList()
        order = database.getOrder(id)
        return render(request, 'edit_page.html', {'address': address, 'car': car, 'client': client, 'order': order})
    else:
        database.updateOrder(id, request.POST['start_id'], request.POST['finish_id'], request.POST['car_id'],
                             request.POST['client_id'], request.POST['entry-day-time'])
        return redirect('/')


def add(request):
    database = DB()
    if request.method == 'GET':
        address = database.getAddressList()
        car = database.getCarList()
        client = database.getClientList()
        return render(request, 'add_page.html', {'address': address, 'car': car, 'client': client})
    elif request.method == 'POST':
        database.saveOrder(request.POST['start_id'], request.POST['finish_id'], request.POST['car_id'],
                           request.POST['client_id'], request.POST['entry-day-time'])
        return redirect('/')


def triggerOn(request):
    database = DB()
    database.enableTrigger()
    return redirect('/')


def triggerOff(request):
    database = DB()
    database.disableTrigger()
    return redirect('/')


def setTime(request):
    database = DB()
    if 'eventTime' in request.GET:
        database.setEventTime(request.GET['eventTime'])
        return redirect(reverse('index') + '?message=Time changed to ' + str(request.GET['eventTime']))
    return redirect(reverse('index'))
