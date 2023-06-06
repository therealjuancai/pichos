
from flask import Flask, render_template, redirect, request, flash, g, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, EqualTo
import sqlite3
from flask_mail import Mail, Message

app=Flask(__name__, static_folder='static')

app.secret_key = "secret_password"

'''MAIL_SERVER ="smtp.mail.yahoo.com"
MAIL_PORT=587
MAIL_USE_SSL=False
MAIL_USE_TLS=True
MAIL_USERNAME="pichotech13@yahoo.com"
MAIL_PASSWORD="Pichonescagones13"
mail=Mail(app)'''


@app.route('/', methods=['GET', 'POST','DELETE'])
def home():
    session.modified=True
    sqliteConnection = sqlite3.connect('base.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM product;")
    rows=cursor.fetchall()
    totalprice=0
    count=0
    if 'user' in session:
        email=session['user']
        for item in session['carrito']:
            count=count+1
            totalprice=totalprice+item['price']
        if request.method=='POST':
            if request.form['_method']=='PUT':
                pid=request.form["code"]
                cursor.execute("SELECT * FROM product WHERE pid=?;", (pid))
                row = cursor.fetchone()

                itemArray={'pid' : row[0], "img" : row[1], "name" : row[2], "price": row[6], "cantidad" : 1 } 

                session['carrito'].append(itemArray)
                print(session['carrito'])
            
            if request.form['_method']=='DELETE':
                id=0
                for item in session['carrito']:
                    if item['pid']==int(request.form['code']):
                        id=item

                if id in session['carrito']:
                    session['carrito'].remove(id)
            count=0
            totalprice=0
            for item in session['carrito']:
                count=count+1
                totalprice=totalprice+item['price']
        return render_template('index.html', name=email , products=rows, carrito=session['carrito'], totalprice=totalprice, count=count)
    else:
        return render_template('index.html', products = rows, totalprice=totalprice, count=count)


@app.route('/login-register', methods=['GET', 'POST'])
def login_register():
    sqliteConnection = sqlite3.connect('base.db')
    cursor = sqliteConnection.cursor()
    if request.method == 'POST':
        action=request.form["action"]
        email=request.form["email"]
        password=request.form["password"]
        if action == 'Create':

            # Verificar si el usuario ya existe en la base de datos
            
            cursor.execute("SELECT * FROM User WHERE email=?;", (email,))
            user = cursor.fetchone()
            if user is not None:
                flash('El usuario ya está registrado', 'error')
            else:
                # Insertar nuevo usuario en la base de datos
                cursor.execute("INSERT INTO User (email, password) VALUES (?, ?);", (email, password))
                sqliteConnection.commit()
                flash('Registro exitoso. Por favor, inicia sesión.', 'success')

        elif action == 'Login':
            # Verificar las credenciales del usuario en la base de datos
            cursor.execute("SELECT * FROM User WHERE email=?;", (email,))
            user = cursor.fetchone()
            if user is not None and password == user[2]:
                session['user']=email
                items=[]
                session['carrito']=items
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('home'))
            else:
                flash('Credenciales inválidas', 'error')

    return render_template('login.html')

@app.route('/acerca')
def acerca():
    if 'user' in session:
        email=session['user']
        return render_template('acerca.html', name=email)
    else:
        return render_template('acerca.html')
    
@app.route('/TodosLosProductos', methods=['GET', 'POST'])
def todoslosproductos():
    session.modified=True
    sqliteConnection = sqlite3.connect('base.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT * FROM product;")
    rows=cursor.fetchall()
    totalprice=0
    count=0
    if 'user' in session:
        email=session['user']
        for item in session['carrito']:
            count=count+1
            totalprice=totalprice+item['price']
        if request.method=='POST':
            if request.form['_method']=='PUT':
                pid=request.form["code"]
                cursor.execute("SELECT * FROM product WHERE pid=?;", (pid))
                row = cursor.fetchone()

                itemArray={'pid' : row[0], "img" : row[1], "name" : row[2], "price": row[6], "cantidad" : 1 } 

                session['carrito'].append(itemArray)
                print(session['carrito'])
            
            if request.form['_method']=='DELETE':
                id=0
                for item in session['carrito']:
                    if item['pid']==int(request.form['code']):
                        id=item

                if id in session['carrito']:
                    session['carrito'].remove(id)
            count=0
            totalprice=0
            for item in session['carrito']:
                count=count+1
                totalprice=totalprice+item['price']
        return render_template('todoslosproductos.html', name=email, products=rows, carrito=session['carrito'], totalprice=totalprice, count=count)
    else:
        return render_template('todoslosproductos.html', products=rows, totalprice=totalprice, count=count)
    
@app.route('/articulospopulares')
def articulospopu():
    if 'user' in session:
        email=session['user']
        return render_template('articulospopu.html', name=email)
    else:
        return render_template('articulospopu.html')

@app.route('/recienllegados')
def recienllegados():
    if 'user' in session:
        email=session['user']
        return render_template('recienllegados.html', name=email)
    else:
        return render_template('recienllegados.html')
    

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    session.modified=True
    totalprice=0
    count=0
    if 'user' in session:
        email=session['user']
        for item in session['carrito']:
            count=count+1
            totalprice=totalprice+item['price']

        return render_template('contacto.html', name=email, carrito=session['carrito'], totalprice=totalprice, count=count)
    else:
        return render_template('contacto.html', carrito=session['carrito'], totalprice=totalprice, count=count)



@app.route('/compra', methods=['GET', 'POST'])
def compra():
    if 'user' in session:
        email=session['user']
        session.modified=True
        if request.method == 'POST':
            cuantity= request.form['cuantity']
            if cuantity=='<':
                id=request.form['code']
                for item in session['carrito']:
                    if int(id)==item['pid'] and item['cantidad']>1 :
                        item['cantidad']= int(item['cantidad'])-1
            if cuantity == '>':
                id=request.form['code']
                for item in session['carrito']:
                    if int(id)==item['pid']:
                        print('aqui llega')
                        item['cantidad']= int(item['cantidad'])+1
        totalprice=0
        for item in session['carrito']:
            totalprice=totalprice+(item['price']*item['cantidad'])
        iva=totalprice*0.1
        envio=10000
        if totalprice>=500000:
            envio=0
        totalpay=iva+envio+totalprice

        return render_template('compra.html', name=email, totalprice=totalprice, iva=iva, envio=envio, totalpay=totalpay, carrito=session['carrito'])
    else:
        return "no tiene permiso para acceder a esta zona"
    


@app.route('/pago')
def pago():
    session.modified=True
    totalprice=0
    for item in session['carrito']:
        totalprice=totalprice+(item['price']*item['cantidad'])
    iva=totalprice*0.1
    envio=10000
    if totalprice>=500000:
        envio=0
    totalpay=iva+envio+totalprice
    if 'user' in session:
        email=session['user']
        return render_template('pago.html', name=email, totalprice=totalprice, envio=envio, totalpay=totalpay)
    else:
        return "no tiene permiso para acceder a esta zona"
    
@app.route('/complete', methods=['GET', 'POST'])
def complete():
    if 'user' in session:
        email=session['user']
        '''mensaje = Message('Tu envio está en preparación', sender= "pichotech13@yahoo.com", recipients=[email])
        mensaje.body = 'Te agradecemos por tu compra. tu pedido ha de llegar a tu domicilio en menos de 72 horas'
        mail.send(mensaje)'''
        return render_template('complete.html', name=email)
    else:
        return "no tiene permiso para acceder a esta zona"
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__== '__main__':
    #mail.init_app(app)
    app.run(debug=True)