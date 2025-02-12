from flask import Flask, render_template, request, make_response, redirect, url_for
from datetime import datetime
import sqlite3
import hashlib
import re
import time

#Version 0.0, Date 02/12/24 ->Created empty database. Started home page and animal search page. Created basic filter system using JavaScript to use later. Created basic log-in page that is not functional

#Version 0.1, Date 03/12/24 ->Continued animal search page and made basic card for each animal to have their name and picture on. Added Side bar 

#Version 0.2 Date 04/12/24 -> Created book tickets page and javascript backend and added sidebar for every page for mobile

#Version 0.3 Date 09/12/24 -> Created Filter Hotels page and javascript backend and added semantic ui dropdowns. added input validation for book tickets page

#Version 0.4 Date 10/12/24 -> Created cookies in flask and javascript and fully implemented them across the website. 

#Version 0.5 Date 11/12/24 -> Started Book hotel option and added sign up feature

#Version 1 Date 16/12/24 -> Finished Book hotel option to finish basic website functionality and added styling

#Version 1.1 Date 17/12/24 -> Added change password option

#Version 1.2 Date 18/12/24 -> added change hotel booking option and delete account option



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

#This function checks if the user's inputs match up with an account in the database,
#and then hashes their password and checks it against the hashed password that is 
#already in the database to see if they match. If the passwords match, a cookie
#is created to log the user in and the user is returned to the home page.
#If the password doesn't match or there is no account, the user is returned to the
#log in page with an error message
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        unhashed_pw = request.form['password']
        if email and unhashed_pw:
            encoded = unhashed_pw.encode(encoding = 'UTF-8', errors = 'strict')#encodes the password string
            hashed_pw = hashlib.sha256(encoded).hexdigest()#hashes the password string

            try:
                con = sqlite3.connect("testing.db")
                cur = con.cursor()
                res = cur.execute("SELECT * FROM customers")
                all = res.fetchall()
                res = cur.execute(f"SELECT customer_id, first_name, p_word FROM customers WHERE email='{email}'")
                result = res.fetchone()
                p_word = result[2]
                name = result[1]
                id = result[0]

                if hashed_pw == p_word:
                    resp = make_response(redirect(url_for("home")))
                    #creates user_id  and first name cookies for the user to use the website
                    resp.set_cookie('user_id', value=f"{id}", max_age=30*24*60*60, httponly=False, secure=True, samesite="strict" )
                    resp.set_cookie('name', value=f"{name}", max_age=30*24*60*60, httponly=False, secure=True, samesite="strict" )
                    time.sleep(0.5)
                    return resp
                else:
                    time.sleep(0.5)
                    return render_template("login.html", pass_fail = True)#returns a specific error message
            except:
                print("email not found")
                return render_template("login.html", user_fail = True)#returns a specific error message
        else:
            return render_template("login.html", enter_fail = True)#returns a specific error message

    return render_template("login.html")


#This function deletes all possible cookies and then
#returns the user back to the home page
@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("home")))
    resp.set_cookie('user_id', value="", expires=0)
    resp.set_cookie('name', value="", expires=0)
    resp.set_cookie('end', value="", expires=0)
    resp.set_cookie('room_price', value="", expires=0)
    resp.set_cookie('total', value="", expires=0)
    resp.set_cookie('old_check_in', value="", expires=0)
    resp.set_cookie('room_number', value="", expires=0)
    return resp

#this function receives either the pre-set input from the "learn more"
#buttons in the animal page, or recieves an input from the search bar.
#It then sends the user to the animal's specific page if the animal exists
@app.route("/animals", methods=["GET", "POST"])
def animals():
    if request.method == "POST":
        try:
            animal = request.form["animal"].lower()#this section users lower() and capitalize() to try and let all user inputs work whilst stil working with the preset inputs

            
            split = animal.split()
            if len(split) > 1:
                animal = split[0].capitalize() +" "+ split[1].capitalize()
            else:
                animal = animal.capitalize()
            print(animal)
            
            con = sqlite3.connect("testing.db")
            cur = con.cursor()
            res = cur.execute(f"SELECT class, latin_name, description, iucn_status, image_url FROM animals WHERE name='{animal}'")#receives info from database
            result = res.fetchone()
            animal_class = result[0]
            description = result[2]
            latin = result[1]
            iucn = result[3]
            url = result[4]

            #returns user with specific info for that animal
            return render_template("animal_page.html", name = animal, animal_class = animal_class, latin = latin, iucn = iucn,  description = description, picture = f"/static/images/{url}.jpg")
        except:
            return render_template("animals.html", search_fail = True)#returns a specific error message
    
    return render_template("animals.html")

#this function allows a user to choose a hotel room to book and then sends them to a booking table for that hotel room
@app.route("/hotel_search", methods=["GET","POST"])
def hotel():
    if request.method == "POST":
        room_number = request.form.get("room")#receives room number
        hotel_price = request.form.get("hotel_price")#recieves price per night
        return render_template("book_hotel.html", hotel_price=int(hotel_price), room = room_number)#returns hotel information to the front end
    return render_template("hotel_search.html")

#this function receives the date of the tickets, as well as how many
#adult and child tickets there are. It then creates each ticket individually 
#in the database as well as updating the user's money_spent value
#the user is then returned to the home page
@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method=="POST":
        today_date = datetime.now()

        ticket_date = request.form["date"]#recieves user inputs
        child_tickets = request.form["child_tickets"]
        adult_tickets = request.form["adult_tickets"]


        if not ticket_date:#checks if a date was chosen
            if (child_tickets == "0") and (adult_tickets == "0"):#checks if there are no tickets selected

                return render_template("book.html", datefail = True, choosefail = True)#returns a specific error message
            
            else:
                return render_template("book.html", datefail = True, choosefail = False)#returns a specific error message
        elif (child_tickets == "0") and (adult_tickets == "0"):#checks if no tickets were selected
            
            return render_template("book.html", datefail = False, choosefail = True)#returns a specific error message
        
        elif today_date > datetime.strptime(ticket_date,'%Y-%m-%d' ):#checks if the date chosen is in the past

            return render_template("book.html", invalid_date = True)#returns a specific error message
        else:

            customer_id = request.cookies.get('user_id')#finds user id for updating the database
            total = 0

            for i in range(int(adult_tickets)):#this goes through each adult ticket and makes a database entry
                total = total + 12
                con = sqlite3.connect("testing.db")
                cur = con.cursor()
                res = cur.execute("SELECT ticket_id FROM bought_tickets")#checks if there are any tickets in the database
                list = res.fetchall()
                if not list:#if no tickets are in the database, it is inserted with ticket_id = 0
                    res = cur.execute("INSERT INTO bought_tickets VALUES(?,?,?,?)", (0,'Adult',ticket_date,customer_id))
                    con.commit()
                else:#if there are tickets in the database, the next id is calculated and used
                    last_id = list[-1][0]
                    new_id = last_id + 1
                    res = cur.execute("INSERT INTO bought_tickets VALUES(?,?,?,?)", (new_id,'Adult',ticket_date,customer_id))
                    con.commit()
            
            for i in range(int(child_tickets)):#this goes through each child ticket and makes a database entry
                total = total + 8
                con = sqlite3.connect("testing.db")
                cur = con.cursor()
                res = cur.execute("SELECT ticket_id FROM bought_tickets")
                list = res.fetchall()
                if not list:#if no tickets exist ticket_id = 0
                    res = cur.execute("INSERT INTO bought_tickets VALUES(?,?,?,?)", (0,'Child',ticket_date,customer_id))
                    con.commit()
                else:#if no tickets exist a new ticket_id is calculated
                    last_id = list[-1][0]
                    new_id = last_id + 1
                    res = cur.execute("INSERT INTO bought_tickets VALUES(?,?,?,?)", (new_id,'Child',ticket_date,customer_id))
                    con.commit()

            con = sqlite3.connect("testing.db")
            cur = con.cursor()
            res = cur.execute(f"SELECT money_spent FROM customers WHERE customer_id = {customer_id}")#gets users old money_spent value
            list = res.fetchone()
            money = list[0]
            total = total + money

            res = cur.execute(f"UPDATE customers SET money_spent = {total} WHERE customer_id = {customer_id}")#updates user's money_spent
            con.commit()
            
            return render_template("index.html")

    return render_template("book.html", datefail = False, choosefail = False)#returns a specific error message

@app.route("/animal_page")
def animal_page():
    return render_template("animal_page.html")

#this function checks if all inputs are filled in and then 
#makes sure that the check in date is before check out and then
#makes sure that either date is not in the past.
#After this all reservations for that room are checked to see if 
#the room is available on these dates. If it is a new reservation is made
#and the user's money_spent is updated
@app.route("/book_hotel", methods=["GET", "POST"])
def book_hotel():
    if request.method == "POST":
        today_date = datetime.now()
        check_in = request.form.get("check_in")
        check_out = request.form.get("check_out")
        price = request.form.get("room_price")
        number = request.form.get("room")
        total = request.cookies.get("total")
        customer_id = request.cookies.get("user_id")



        if (not check_in) or (check_in == "") or (not check_out) or (check_out == ""):
            return render_template("book_hotel.html", hotel_price=int(price), room = number, empty_fail = True)#returns a specific error message
        
        date_check_in = datetime.strptime(check_in,'%Y-%m-%d' )
        date_check_out = datetime.strptime(check_out,'%Y-%m-%d' )

        if date_check_in >= date_check_out:
            return render_template("book_hotel.html", hotel_price=int(price), room = number, date_fail = True)#returns a specific error message
        elif (today_date > date_check_in) or (today_date > date_check_out):
            return render_template("book_hotel.html", hotel_price=int(price), room = number, today_fail = True)#returns a specific error message
        else:
            con = sqlite3.connect("testing.db")
            cur = con.cursor()
            res = cur.execute(f"SELECT check_in_date, check_out_date FROM reservations WHERE room_number = '{number}'")#finds reservations for the room
            list = res.fetchall()
            print(list)
            for i in list:
                reserved = datetime.strptime(i[0],'%Y-%m-%d' )#checks if check in dates are not within the range
                if (date_check_in <= reserved < date_check_out):
                    return render_template("book_hotel.html", hotel_price=int(price), room = number, reserve_fail = True)#returns a specific error message
            print("passed One")
            for i in list:
                reserved = datetime.strptime(i[1],'%Y-%m-%d' )#checks if check out dates are no within the range
                if (date_check_in < reserved < date_check_out):
                    return render_template("book_hotel.html", hotel_price=int(price), room = str(number), reserve_fail = True)#returns a specific error message
            print("passed two")

            res = cur.execute("SELECT reservation_id FROM reservations")
            list = res.fetchall()
            print(list)
            if not list:#if no reservations exist reservation_id =0
                res = cur.execute("INSERT INTO reservations VALUES(?,?,?,?,?,?)", (0,check_in, check_out, total, customer_id, number))
                con.commit()
                print("all done")
            else:#if some reservations exist the id is calculated
                last_id = list[-1][0]
                print(last_id)
                new_id = last_id + 1
                res = cur.execute("INSERT INTO reservations VALUES(?,?,?,?,?,?)", (new_id,check_in, check_out, total, customer_id, number))
                con.commit()
            
            con = sqlite3.connect("testing.db")
            cur = con.cursor()
            res = cur.execute(f"SELECT money_spent FROM customers WHERE customer_id={customer_id}")
            result = res.fetchone()
            money_spent = result[0] + (int(total))#money_spent is updated

            res = cur.execute(f"UPDATE customers SET money_spent = {money_spent} WHERE customer_id = {customer_id}")
            con.commit()


            resp = make_response(redirect(url_for("option_menu")))
            resp.set_cookie('total', value="", expires=0)
            return resp
        
    return render_template("book_hotel.html", hotel_price=int("50"), room = "101")

@app.route("/option_menu")
def option_menu():
    return render_template("option_menu.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/edu_visit")
def edu_visit():
    return render_template("edu_visit.html")

@app.route("/back")#this deletes all cookies related to that reservation if the user changes their mind
def back():
    resp = make_response(render_template("change_hotel.html"))
    resp.set_cookie('end', value="", expires=0)
    resp.set_cookie('room_price', value="", expires=0)
    resp.set_cookie('total', value="", expires=0)
    resp.set_cookie('old_check_in', value="", expires=0)
    resp.set_cookie('room_number', value="", expires=0)
    return resp

@app.route("/tic_back")#this deletes all cookies related to that reservation if the user changes their mind
def tic_back():
    user_id = request.cookies.get("user_id")
    con = sqlite3.connect("testing.db")#connects to database
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM bought_tickets WHERE customer_id={user_id}")

    resp = make_response(render_template("change_tickets.html", tickets = res))
    resp.set_cookie('tic_id', value="", expires=0)
    resp.set_cookie('tic_date', value="", expires=0)
    resp.set_cookie('tic_user', value="", expires=0)
    return resp
 
#this function could either receive user input for which reservation to find
#or user input on how to change the reservation. Therefore the "end" cookie is used 
#and checked to see which to do. 
#The first part checks if the reservation exists and belongs to the user, and then creates
#cookies relating to that reservation.
#The second part checks if the updated resrvation is available and if it is it updates
#the reservation and the user's money_spent
@app.route("/change_hotel", methods=["GET", "POST"])
def change_hotel():
    if request.method == "POST":
        
        ticket_id = request.form.get("ticket_id")
        if ticket_id:
            print(ticket_id)
            return redirect("/")
        old_check_in = request.form.get("old_check_in")#receives user inputs
        room_number = request.form.get("room_number")
        check_in = request.form.get("check_in")
        check_out = request.form.get("check_out")

        end = request.cookies.get("end")#receives cookies
        user_id =request.cookies.get("user_id")


        if (end != "TRUE") and (old_check_in != "") and (room_number != ""):#checks which part of the inputs are recieved and if end = "TRUE"
            print("start")
            date_old_check_in = datetime.strptime(old_check_in,'%Y-%m-%d' )
            con = sqlite3.connect("testing.db")
            cur = con.cursor()
            res = cur.execute(f"SELECT customer_id FROM reservations WHERE room_number={int(room_number)} and check_in_date = '{old_check_in}'")
            result = res.fetchone()
            print(result[0])
            if int(result[0]) == int(user_id):
                resp = make_response(render_template("change_hotel.html"))
                res = cur.execute(f"SELECT price FROM hotel_rooms WHERE room_number={int(room_number)}")
                result = res.fetchone()
                price = result[0]
                resp.set_cookie('end', value="TRUE", httponly=False)
                resp.set_cookie("old_check_in", value = f"{old_check_in}", httponly=False )
                resp.set_cookie("room_price", value = f"{price}", httponly=False )
                resp.set_cookie("room_number", value = f"{room_number}", httponly=False )
                return resp
            else:
                return render_template("change_hotel.html", invalid_fail=True)#returns a specific error message
        elif end !="TRUE":#If end isnt TRUE and no inputs are found then inputs must be empty
            return render_template("change_hotel.html", enter_fail=True)#returns a specific error message
        elif (check_in != "") and (check_out != ""):
            print("end")
            today_date = datetime.now()
            old_check_in = request.cookies.get("old_check_in")#cookies are received as they will no longer be 
            room_number = request.cookies.get("room_number")#submitted by the form as the user is on a different menu
            total = request.cookies.get("total")#total price of the new reservation

            date_check_in = datetime.strptime(check_in,'%Y-%m-%d' )
            date_check_out = datetime.strptime(check_out,'%Y-%m-%d' )

            if date_check_in >= date_check_out:#makes sure check in is before check out

                return render_template("change_hotel.html", date_fail = True)#unique error message is returned
            
            elif (today_date > date_check_in) or (today_date > date_check_out):#checks if is in the past

                return render_template("change_hotel.html", today_fail = True)#unique error message is returned
            
            else:
                con = sqlite3.connect("testing.db")
                cur = con.cursor()
                res = cur.execute(f"SELECT reservation_id, price FROM reservations WHERE room_number={int(room_number)} and check_in_date = '{old_check_in}'")
                result = res.fetchone()#room number and old check in will not be submitted this time as the user submitted those to get to this page
                reserve_id = result[0]#therefore the room number and old check in date must be assigned using the database
                old_price = result[1]
                res = cur.execute(f"SELECT check_in_date, check_out_date FROM reservations WHERE room_number = '{int(room_number)}' and reservation_id != {int(reserve_id)}")
                list = res.fetchall()
                for i in list:
                    reserved = datetime.strptime(i[0],'%Y-%m-%d' )#checks if check in dates are within the users chosen reservation dates
                    if (date_check_in <= reserved < date_check_out):
                        return render_template("change_hotel.html", reserve_fail = True)#unique error message is returned
                
                for i in list:
                    reserved = datetime.strptime(i[1],'%Y-%m-%d' )#checks if check out dates are within the users chosen reservation dates
                    if (date_check_in < reserved < date_check_out):
                        return render_template("change_hotel.html", reserve_fail = True)#unique error message is returned
                
                res = cur.execute(f"UPDATE reservations SET check_in_date = '{check_in}' WHERE room_number = {int(room_number)} and check_in_date = '{old_check_in}'")
                con.commit()
                res = cur.execute(f"UPDATE reservations SET check_out_date = '{check_out}' WHERE room_number = {int(room_number)} and check_in_date = '{check_in}'")
                con.commit()
                res = cur.execute(f"UPDATE reservations SET price = {int(total)} WHERE room_number = {int(room_number)} and check_in_date = '{check_in}'")
                con.commit()

                res = cur.execute(f"SELECT money_spent FROM customers WHERE customer_id = '{user_id}'")
                result = res.fetchone()
                spent = int(result[0])
                spent = spent - int(old_price)#removes old price of the resrvation from money_spent and adds the new price of the resrvation instead
                spent = spent + int(total)
                print(spent)

                res = cur.execute(f"UPDATE customers SET money_spent = {spent} WHERE customer_id = {user_id}")
                con.commit()
                resp = make_response(render_template("change_hotel.html"))
                resp.set_cookie('end', value="", expires=0)#removes all of the cookies as they are no longer needed
                resp.set_cookie('room_price', value="", expires=0)
                resp.set_cookie('total', value="", expires=0)
                resp.set_cookie('old_check_in', value="", expires=0)
                resp.set_cookie('room_number', value="", expires=0)
                return resp
        else:
            return render_template("change_hotel.html", enter_fail = True)#unique error message is returned
        
    return render_template("change_hotel.html",)


#this function allows the user to change their password by taking the old password as verification
#and then after hashing the password and checking it against the password in the database
#it hashes the new password and updates that into the database
@app.route("/manage", methods=["GET", "POST"])
def manage():
    if request.method == "POST":
        new = request.form.get("new")#recieves user inputs
        current = request.form.get("current")
        #receives user id from cookies
        user_id = request.cookies.get("user_id")

        if (user_id == "") or (user_id == None):#checks if the inputs are filled in

            return render_template("manage.html", login_fail = True)#unique error message is returned
        
        if (new == "") or (new == None) or (current == "") or (current == None):#checks if inputs are filled in

            return render_template("manage.html", enter_fail = True)#unique error message is returned
        
        con = sqlite3.connect("testing.db")
        cur = con.cursor()
        res = cur.execute(f"SELECT p_word FROM customers WHERE customer_id={user_id}")
        result = res.fetchone()
        password = result[0]

        encoded = current.encode(encoding = 'UTF-8', errors = 'strict')#encodes password string
        hashed_pw = hashlib.sha256(encoded).hexdigest()#hashes password string


        if hashed_pw == password:#checks hashed password to hashed password in the database
            encoded = new.encode(encoding = 'UTF-8', errors = 'strict')#encodes new password
            new_hashed_pw = hashlib.sha256(encoded).hexdigest()#hashes new password
            cur = con.cursor()
            res = cur.execute(f"UPDATE customers SET p_word = '{new_hashed_pw}' WHERE customer_id = {user_id}")#changes password
            con.commit()
            return render_template("manage.html", success = True)#unique error message is returned
        else:
            return render_template("manage.html", pass_fail = True)#unique error message is returned

    return render_template("manage.html")

#this function is from the user sign up page and takes inputs for all database columns.
#it then validates all of the data and makes sure that the confirm password is the same as the password
#it then adds the user to the customers table in the database and then logs the user in using cookies
#and returns the user to the home page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["first_name"]#user inputs are taken for each database column
        last_name = request.form["last_name"]
        age = request.form["age"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        email_verification = (r"^\S+@\S+\.\S+$")#regex for email verification

        check_first = re.findall("[a-zA-Z]", first_name)#returns all letter values, which is then checked against the original string.
        check_last = re.findall("[a-zA-Z]", last_name)#therefore if the regex matches has less letters than the string it must have some numbers or special characters
        check_age = re.findall("[a-zA-Z]", age)
        check_email = re.match(email_verification, email)

        #checks if all inputs are filled
        if (first_name == "") or (last_name == "") or (age == "") or (email == "") or (password == "") or (confirm_password == ""):#makesa sure all inputs are filled
            return render_template("signup.html", enter_fail = True)  
        
        elif (" " in first_name) or (" " in last_name) or (len(check_first) != len(first_name)) or (len(check_last) != len(last_name)):#ensures only letters are in the names
            return render_template("signup.html", name_fail=True)
        
        elif (int(age) < 18) or check_age:#makes sure user is over 18
            return render_template("signup.html", age_fail=True)
        
        elif not check_email:#if email doesn't pass the regex
            return render_template("signup.html", email_fail=True)
        
        elif password != confirm_password:#if the confirm password doesn't match the password
            return render_template("signup.html", pass_fail=True)
        
        con = sqlite3.connect("testing.db")#connects to database
        cur = con.cursor()
        res = cur.execute(f"SELECT email FROM customers WHERE email='{email}'")
        emails = res.fetchone()

        print(emails)

        if emails:
            return render_template("signup.html", email_used=True) #unique error message is returned
        
        encoded = password.encode(encoding = 'UTF-8', errors = 'strict')#encodes password string
        hashed_pw = hashlib.sha256(encoded).hexdigest()#hashes password string
        res = cur.execute("SELECT customer_id FROM customers")
        list = res.fetchall()
        print(list)
        if not list:#if no customers are in the table customer_id = 0
            res = cur.execute("INSERT INTO customers VALUES(?,?,?,?,?,?,?)", (0,first_name, last_name, 0, hashed_pw, email, age))
            con.commit()
            print("all done")
            resp = make_response(redirect(url_for("home")))
            resp.set_cookie('user_id', value=f"{0}", max_age=30*24*60*60, httponly=False, secure=True, samesite="strict" )#logs user in using cookies after they sign up
            resp.set_cookie('name', value=f"{first_name}", max_age=30*24*60*60, httponly=False, secure=True, samesite="strict" )
            print("Log in success")
            return resp
        else:#if customers are in the table customer_id is calculated
            last_id = list[-1][0]
            print(last_id)
            new_id = last_id + 1
            res = cur.execute("INSERT INTO customers VALUES(?,?,?,?,?,?,?)", (new_id,first_name, last_name, 0, hashed_pw, email, age))
            con.commit()
            print("all done")
            print("start")
            resp = make_response(redirect(url_for("home")))
            resp.set_cookie('user_id', value=f"{new_id}", max_age=30*24*60*60, httponly=False, secure=True, samesite="strict" )#logs user in using cookies after they sign up
            resp.set_cookie('name', value=f"{first_name}", max_age=30*24*60*60, httponly=False, secure=True, samesite="strict" )
            print("Log in success")
            return resp
    return render_template("signup.html")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        password = request.form.get("password")#receives password from user
        encoded = password.encode(encoding = 'UTF-8', errors = 'strict')#encodes password string
        hashed_pw = hashlib.sha256(encoded).hexdigest()#hashes password string

        user_id = request.cookies.get("user_id")#gets user id from cookies
        print(user_id)

        if not user_id:
            return render_template("delete.html", login_fail = True)#unique error message

        con = sqlite3.connect("testing.db")#connects to database
        cur = con.cursor()
        res = cur.execute(f"SELECT p_word FROM customers WHERE customer_id={user_id}")
        result = res.fetchone()
        p_word = result[0]#gets password 

        if p_word == hashed_pw:#checks password
            print("Deleting")
            res = cur.execute(f"DELETE FROM customers WHERE customer_id={user_id}")
            con.commit()
            resp = make_response(render_template("delete.html", success = True))
            resp.set_cookie('user_id', value="", expires=0)
            resp.set_cookie('name', value="", expires=0)
            return resp
        else:
            return render_template("delete.html", fail = True)#unique error message
        
    return render_template("delete.html")

@app.route('/change_tickets', methods=["GET", "POST"])
def change_tickets():
    user_id = request.cookies.get("user_id")#gets user id from cookies
    if not user_id:
        return redirect("/")
    else:
        if request.method == "POST":
            id = request.form.get("tic_id")
            date = request.form.get("tic_date")
            print(id)
            print(date)

            resp = make_response(redirect(url_for("manage_tickets")))

            resp.set_cookie("tic_date", value = f"{date}", httponly=False )
            resp.set_cookie("tic_id", value = f"{id}", httponly=False )
            resp.set_cookie("tic_user", value = f"{user_id}", httponly=False )
         
            return resp
        else:
            con = sqlite3.connect("testing.db")#connects to database
            cur = con.cursor()
            res = cur.execute(f"SELECT * FROM bought_tickets WHERE customer_id={user_id}")
            print(res)
            return render_template("change_tickets.html", tickets = res)

@app.route('/manage_tickets', methods=["GET", "POST"])
def manage_tickets():
    user_id = request.cookies.get("user_id")#gets user id from cookies
    if not user_id:
        return redirect("/")
    else:
        if request.method == "POST":
            new_date = request.form.get("new_date")
            ticket_user = request.cookies.get("tic_user")
            ticket_id = request.cookies.get("tic_id")
            time.sleep(0.5)
            if user_id == ticket_user:
                print("passed")
                today_date = datetime.now()
                try:
                    if today_date > datetime.strptime(new_date,'%Y-%m-%d' ):#checks if the date chosen is in the past
                        return render_template("manage_tickets.html", date_fail = True)
                    else:
                        con = sqlite3.connect("testing.db")#connects to database
                        cur = con.cursor()
                        res = cur.execute(f"UPDATE bought_tickets SET ticket_date = '{new_date}' WHERE ticket_id = {ticket_id}")
                        con.commit()
                        print("done")

                    res = cur.execute(f"SELECT * FROM bought_tickets WHERE customer_id={user_id}")
                    resp = make_response(render_template("change_tickets.html", tickets = res))
                    resp.set_cookie('tic_id', value="", expires=0)
                    resp.set_cookie('tic_date', value="", expires=0)
                    resp.set_cookie('tic_user', value="", expires=0)
                    return resp
                except:
                    return render_template("manage_tickets.html", date_fail = True)
            else:
                return render_template("manage_tickets.html", invalid_fail = True)

        else:
            return render_template("manage_tickets.html")


@app.route('/testchange', methods=["GET", "POST"])
def test_change():
    user_id = request.cookies.get("user_id")#gets user id from cookies
    if not user_id:
        return redirect("/")
    else:
        if request.method == "POST":
            id = request.form.get("reservation_id")
            date = request.form.get("tic_date")
            print(id)
            print(date)

            resp = make_response(redirect(url_for("manage_tickets")))

            resp.set_cookie("start_date", value = f"{date}", httponly=False )
            resp.set_cookie("end_date", value = f"{date}", httponly=False )
            resp.set_cookie("reservation_id", value = f"{id}", httponly=False )
            resp.set_cookie("tic_user", value = f"{user_id}", httponly=False )
         
            return resp
        else:
            con = sqlite3.connect("testing.db")#connects to database
            cur = con.cursor()
            res = cur.execute(f"SELECT * FROM bought_tickets WHERE customer_id={user_id}")
            return render_template("change_tickets.html", tickets = res)

    



if __name__ == '__main__':
   app.run()

