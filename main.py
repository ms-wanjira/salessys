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
def inventories_mimi():
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
            # print(rows)
            # print (len(rows))
            # print(type(rows[0]))
            return render_template("inventories.html", rows=rows)


@app.route('/sales', methods=['POST', 'GET'])
def sales():
    cur = conn.cursor()
    cur.execute("""SELECT id,product_id,quantity,DATE(sales_date),product_name FROM sales """)
    x = cur.fetchall()
    # print(x)
    # return redirect(url_for('sales'))
    
    if request.method == "POST":
        cur = conn.cursor()
        r=request.form["product_id"]
        t=request.form["product_name"]
        q= request.form["quantity"]
        cur.execute("""select quantity from inventories where id=%(r)s and name =%(t)s""",{"r":r, "t":t})
        y=cur.fetchone()
        q=int(q)
        # print(q)
        b=y[0]-q
        # print(b)
        if b>=0:
                cur.execute(""" UPDATE inventories SET quantity=%(b)s WHERE id=%(r)s AND name =%(t)s""",{"b":b,"t":t ,"r":r})
                cur.execute("""INSERT INTO sales(product_id,product_name,quantity) VALUES(%(r)s,%(t)s,%(q)s)""",{"r":r,"t":t,"q":q})
                conn.commit()           
                # print("THIS IS THE ID",r,b)
                return redirect(url_for('.sales'))

    return render_template("sales.html", rows=x)



@app.route('/sales/<int:x>')
def viewsale(x):
    cur = conn.cursor()
    cur.execute("""SELECT id,product_id,quantity,DATE(sales_date),product_name FROM sales where product_id=%(product_id)s """,{"product_id":x})
    x = cur.fetchall()
    # print(x)
    return render_template('sales.html' ,rows=x)


@app.route('/inventories')
def editsale():
    if request.method =="POST":
        cur = conn.cursor()
        v=request.form["id"]
        w=request.form["name"]
        x=request.form["quantity"]
        y=request.form["buyingprice"]
        z=request.form["sellingprice"]
        if x<=0:
            cur.execute(""" UPDATE inventories SET quantity=%(x)s buyingprice=%(y)s sellingprice%(z)s WHERE id=%(v)s AND name =%(w)s""",{"x":x,"y":y ,"z":z,"v":v,"w":w})
            cur.execute("""INSERT INTO inventories(quantity,buyingprice,sellingprice) VALUES(%(x)s,%(y)s,%(z)s)""",{"x":x,"y":y,"z":z})
            conn.commit()           
            # return redirect(url_for('.inventories'))
        return render_template('inventories.html')
       
  
    
@app.route('/insights')
def dashboard():
    cur = conn.cursor()
    cur.execute("""SELECT (extract ('month' from sales.sales_date)), sum(sales.quantity * inventories.selling_price) FROM sales JOIN inventories ON sales.product_id=inventories.id group by sales_date,sales.quantity;""")
    spm=cur.fetchall()
    print (spm)
# convert spm to how chartjs expects.....




    # cur = conn.cursor()
    # cur.execute("""SELECT  quantity,product_name FROM sales;""")
    # sbp=cur.fetchall()
    # print (sbp)


    # cur = conn.cursor()
    # cur.execute("""SELECT  quantity,product_name FROM sales;""")
    # sbp=cur.fetchall()
    # print (sbp)
    
    return render_template("insights.html", spm=spm)




app.run(debug=True)





















































