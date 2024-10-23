from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secreto' 


def obtener_productos():
    if 'productos' not in session:
        session['productos'] = []
    return session['productos']

@app.route('/')
def index():
    productos = obtener_productos()
    return render_template('index.html', productos=productos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        producto = {
            'id': len(obtener_productos()) + 1,
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        obtener_productos().append(producto)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('nuevo_producto.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = obtener_productos()
    producto = next((p for p in productos if p['id'] == id), None)
    if request.method == 'POST' and producto:
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    return render_template('nuevo_producto.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    productos = obtener_productos()
    session['productos'] = [p for p in productos if p['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
