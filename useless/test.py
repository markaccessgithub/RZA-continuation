import hashlib
import sqlite3
import re

test = "password"
test = test.encode(encoding = 'UTF-8', errors = 'strict')
test = hashlib.sha256(test).hexdigest()

a = (r"^\S+@\S+\.\S+$")
y="marongmail.co"
x = x = re.match(a, y)

print(x)
_in="2024-12-18"
out="2024-12-20"
con = sqlite3.connect("another.db")
cur = con.cursor()
res = cur.execute("INSERT INTO reservations VALUES(?,?,?,?,?,?)", (1,_in,out,"100",0,"101"))
con.commit()