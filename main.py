from itertools import product
from flask import Flask, render_template, request, url_for
import psycopg2
from werkzeug.utils import redirect
# try:
conn = psycopg2.connect("dbname='mytechshop' user='postgres' host='localhost' password='Tamara98'")


# except:
#     print ("I am unable to connect to the database")
app = Flask(__name__)


# @app.route('/users/<myname>')
# def hello_world(myname):
#     return f"hello {myname}"

@app.route('/')
def index():
    text="Your best shop where good quality materials is guranteed and customer satisfaction is the best in the market."
    return render_template('index.html', text=text)


@app.route('/inventories', methods=['POST', 'GET'])
def inventories():
    if request.method=='POST':
            cur=conn.cursor()
            name=request.form["name"]
            quantity=request.form['quantity']
            buyingprice=request.form["buyingprice"]
            sellingprice=request.form["sellingprice"]

            print(name,quantity,buyingprice,sellingprice)


            cur = conn.cursor()
            cur.execute("""INSERT INTO inventories(name,quantity,buying_price,selling_price) VALUES (%(n)s, %(quan)s,%(bp)s,%(sp)s)""",{"n":name, "quan":quantity,"bp":buyingprice,"sp":sellingprice})
            conn.commit()
            return redirect("/inventories")
    else:

            cur = conn.cursor()
            cur.execute("""SELECT * FROM  inventories""")
            rows = cur.fetchall()
            print(rows)
            # print (len(rows))
            # print(type(rows[0]))
            return render_template("inventories.html", rows=rows)


@app.route('/sales', methods=['POST', 'GET'])
def sales():
    cur = conn.cursor()
    cur.execute("""SELECT * FROM sales """)
    x = cur.fetchall()
    # print(x)
    # return redirect(url_for('sales'))
    
    if request.method == "POST":
        cur = conn.cursor()
        r=request.form["id"]
        q= request.form["quantity"]
        cur.execute("""select quantity from inventories where id=%(r)s""",{"r":r})
        y=cur.fetchone()
        q=int(q)
        # print(q)
        b=y[0]-q
        # print(b)
        if b>=0:
                cur.execute(""" UPDATE inventories SET quantity=%(b)s WHERE id=%(r)s""",{"b":b,"r":r})
                cur.execute("""INSERT INTO sales(id,quantity) VALUES(%(r)s,%(q)s)""",{"r":r,"q":q})
                conn.commit()
            
                print("THIS IS THE ID",r,b)
                return redirect(url_for('sales'))

    return render_template("sales.html", rows=x)
   
app.run(debug=True)






















































