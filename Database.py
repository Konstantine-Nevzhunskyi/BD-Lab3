import MySQLdb as mdb
import sys
import csv

from models import Address, TaxiOrder, Car, Client


# 109 / 15


class DB(object):

    def __init__(self):
            self.client = MongoClient()
            self.db = self.client.lab2

    def connect(self):
        if self.connection is not None:
            return
        try:
            self.connection = mdb.connect('localhost', 'root', 'root', 'taxi_db')

        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            self.connection = None

    def close(self):
        if self.connection is not None:
            self.connection.close()
        self.connection = None

    def enableTrigger(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("CREATE TRIGGER backup AFTER DELETE ON taxi_order for each row  "
                    "CALL logOrder(OLD.id, OLD.start_id, OLD.finish_id, OLD.car_id, OLD.client_id, OLD.data);")
        self.close()

    def disableTrigger(self):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("DROP trigger backup;")
        self.close()

    def setEventTime(self, time):
        self.connect()
        if self.connection is None:
            return []

        cur = self.connection.cursor(mdb.cursors.DictCursor)
        cur.execute("ALTER EVENT clearEvent ON SCHEDULE EVERY %s MINUTE" % time)
        self.close()

    def getOrderList(self):
        return TaxiOrder.objects.all()

    def getOrder(self, id):
        return TaxiOrder.objects.get(id=id)

    def getCarList(self):
        return Car.objects.all()

    def getClientList(self):
        return Client.objects.all()

    def getAddressList(self):
        return Address.objects.all()

    def saveOrder(self, startId, finishId, carId, clientId, data):
        car = Car.objects.get(id=int(carId))
        client = Client.objects.get(id=int(clientId))
        start = Address.objects.get(id=int(startId))
        finish = Address.objects.get(id=int(finishId))
        TaxiOrder.objects.create(car=car, client=client, start=start, finish=finish, data=data)

    def updateOrder(self, orderId, startId, finishId, carId, clientId, data):
        order = TaxiOrder.objects.get(id=int(orderId))
        car = Car.objects.get(id=int(carId))
        client = Client.objects.get(id=int(clientId))
        start = Address.objects.get(id=int(startId))
        finish = Address.objects.get(id=int(finishId))
        order.car = car
        order.client = client
        order.start = start
        order.finish = finish
        order.data = data
        order.save()

    def removeOrder(self, id):
        TaxiOrder.objects.get(id=id).delete()
