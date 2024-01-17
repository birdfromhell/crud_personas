from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'contactos'
mysql=MySQL(app)

app.secret_key='llavesecreta'
    
@app.route('/')
def index():
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM personas')
    data = cur.fetchall()
    return render_template('index.html', personas=data)

@app.route('/agregar_persona', methods=['POST'])
def agregar_persona():
    if request.method == 'POST':
        
        nombre_completo= request.form ['nombre']
        mail= request.form ['mail']
        celular= request.form ['celular']

        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO personas (nombre, mail, celular) VALUES(%s,%s,%s)',
                    (nombre_completo, mail, celular))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')

    return redirect(url_for('index'))

@app.route('/editar_personas/<id>', methods=['POST'])
def editar_personas(id):
    if request.method=='POST':
        nombre=request.form['nombre']
        mail=request.form['mail']
        celular=request.form['celular']
    
    cur=mysql.connection.cursor()
    sql = ('UPDATE personas SET nombre=%s, mail=%s, celular=%s WHERE id=%s')
    data = (nombre, mail, celular,id)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/eliminar_persona/<id>')
def eliminar_persona(id):
    cur=mysql.connection.cursor()
    cur.execute(f'DELETE from personas WHERE id = {id}')
    mysql.connection.commit()
    flash('Contacto removido correctamente')
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(port=3000, debug=True)

