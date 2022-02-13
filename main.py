import mysql.connector
from datetime import datetime
mydb = mysql.connector.connect(host="localhost", user="root", passwd="abcd1234", database="jatin")
mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE customer ( id int PRIMARY KEY NOT NULL AUTO_INCREMENT,name varchar(50) NOT NULL,"
                 #"phone varchar(50),email varchar(50), created datetime)")
#mycursor.execute("CREATE TABLE rental_detail ( id int PRIMARY KEY NOT NULL AUTO_INCREMENT,c_name varchar(50) NOT NULL, created_at datetime ,return_date varchar(50),veh_type varchar(50) NOT NULL)")


class Customer:

    def __init__(self):
        self.customers_list =[]

    def add_detail(self):
        self.name = input("Enter the customer name:-")
        self.phone = int(input("Enter the phone number:-"))
        self.email = input("Enter the customer mail:-")
        self.customer_detail = []
        self.customer_detail.append(self.name)
        self.customer_detail.append(self.phone)
        self.customer_detail.append(self.email)
        print(self.customer_detail)
        mycursor.execute("INSERT INTO customer (name,phone,email,created) values (%s,%s,%s,%s) ", (self.name,self.phone,self.email,datetime.now()));
        mydb.commit()

        print("1. for add more customer")
        print("any key to exit")
        val = input("Enter input:-")
        if val == '1':
            self.add_more()
        else:
            return 


    def add_more(self):
            self.add_detail()

    def show_detail(self):
        mycursor.execute("select * from customer")

        for i in mycursor:
            print(i)




class Vehicles(Customer):

    def __init__(self,default_vehicles):
        self.default_vehicles=default_vehicles

    def add_vehicles(self):

        self.vehicle_type = input("Enter the vehicle type:-")
        self.vehicle_inventory = int(input("Enter value:-"))

        self.default_vehicles[self.vehicle_type] = self.vehicle_inventory

    def modify_inventory(self):

        print(self.default_vehicles)
        self.name = input("Enter the vehicle type you went to modify:-")
        if self.name in self.default_vehicles:
            self.value = int(input("Enter the inventory value:-"))
            self.default_vehicles[self.name] = self.value
        else:
            print("Enter correct vehicle type")

    def rent_vehicles(self):
        name_list=[]
        mycursor.execute("select name from customer")
        result = mycursor.fetchall()
        print("Total customer name are:", len(result))
        for i in result:
            #print("Name: ", i[0])
            name_list.append(i[0])
        print(name_list)
        while True:
            cname = input("Enter the name from the list:-")
            if cname in name_list:
                return_date = int(input("Enter the return date"))
                self.show_vehicles()
                while True:
                    vehicle_type = input("Enter the vehicle type from the list")
                    if vehicle_type in self.default_vehicles:
                        x = self.default_vehicles[vehicle_type]
                        if x > 0:
                            mycursor.execute("INSERT INTO rental_detail (c_name,created_at,return_date,veh_type) values"
                                         " (%s,%s,%s,%s) ", (cname, datetime.now(), return_date, vehicle_type));
                            mydb.commit()
                            x -= 1
                            self.default_vehicles[vehicle_type]=x
                            print(f"{cname} rent a {vehicle_type}")
                            break
                        else:
                            print(f"{vehicle_type} cannot be rented as it is already booked")

                        break
                    else:
                        print(f"{vehicle_type} is not present in vehicles inventory.")

                break
            else:
                print("Please enter right name!")


    def rental_book_list(self):
        mycursor.execute("select * from rental_detail")
        result = mycursor.fetchall()

        for i in result:
            print("id:",i[0])
            print("name:",i[1])
            print("rent_datetime:", i[2])
            print("return_date:",i[3])
            print("vehicle_type:",i[4])

    def show_vehicles(self):
        print(self.default_vehicles)


def start():
    while True:
        ei = input('''
1. Add customer
2. Add rental booking
3. See customer list
4. See rental booking list
5. See inventory of vehicles available
Press any other key to exit
''')
        vehicle = Vehicles(vehicles_avail)

        if ei == '1':
            vehicle.add_detail()
        elif ei == '2':
            vehicle.rent_vehicles()
        elif ei == '3':
            vehicle.show_detail()
        elif ei == '4':
            vehicle.rental_book_list()
        elif ei == '5':
            vehicle.show_vehicles()
        else:
            break


vehicles_avail = {
    "bike": 2,
    "cycle": 3,
    "car": 1,
    "boat": 2,
}

if __name__ == "__main__":
    start()

