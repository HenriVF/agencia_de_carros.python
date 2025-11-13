from flask import Flask, render_template, request, redirect, url_for
import mysql.connector


app = Flask(__name__)


#------------------Configuração do Banco de Dados-------------------
DB_CONFIG ={
    "host": "localhost",
    "user": "root",
    "password": "", #Deixe vazio se não usa senha
    "database": "agencia_carros"
}


def get_connection():
    #Cria e retorna uma conexão com o banco de dados."""
    return mysql.connector.connect(**DB_CONFIG)
   


#------------------Rotas principais-----------------
@app.route('/')
def index():
    return render_template('index.html')


#------------------Rotas Clientes-----------------
@app.route('/clientes')
def clientes():
    #Listar todos os clientes"""
    conn = get_connection()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("SELECT * FROM  clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes = clientes)


@app.route('/cliente/novo', methods=['GET', 'POST'])
def cliente_novo():
    #Cadastrar um novo cliente"""
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']


        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes(nome, email, telefone, endereco) VALUES(%s, %s, %s, %s)", (nome, email, telefone, endereco))


        conn.commit()
        cursor.close()
        conn.close()


        return redirect(url_for('clientes'))


    return render_template('cliente_form.html')
   


@app.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
def cliente_editar(id):
    #Edita um cliente existente."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']


        cursor.execute("""
            UPDATE clientes
            SET nome=%s, email=%s, telefone=%s, endereco=%s
            WHERE id=%s
        """, (nome, email, telefone, endereco, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('clientes'))


    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('cliente_form.html', cliente=cliente)




@app.route('/cliente/deletar/<int:id>')
def clientes_deletar(id):
    #Deleta cliente pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM  clientes WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('clientes'))


#------------------Rotas Veiculos-----------------
@app.route('/veiculos')
def veiculos():
    #Listar todos os veículos e permitir pesquisa"""
    marca = request.args.get('marca', '').strip()
    modelo = request.args.get('modelo', '').strip()
    cor = request.args.get('cor', '').strip()
    valor_max = request.args.get('valor_max', '').strip()


    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    sql = "SELECT * FROM veiculos WHERE 1=1 "
    params = []


    if marca:
        sql += " AND marca LIKE %s "
        params.append(f"%{marca}%")


    if modelo:
        sql += " AND modelo LIKE %s "
        params.append(f"%{modelo}%")


    if cor:
        sql += " AND cor LIKE %s "
        params.append(f"%{cor}%")


    if valor_max:
        sql += " AND preco <= %s "
        params.append(valor_max)


    sql += " ORDER BY id DESC "


    cursor.execute(sql, params)
    veiculos = cursor.fetchall()


    cursor.close()
    conn.close()


    return render_template('veiculos.html', veiculos=veiculos)


@app.route('/veiculo/novo', methods=['GET', 'POST'])
def veiculo_novo():
    #Cadastrar um novo veiculo"""
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano = request.form['ano']
        preco = request.form['preco']
        cor = request.form['cor']


        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO veiculos(marca, modelo, ano, preco, cor) VALUES(%s, %s, %s, %s, %s)", (marca, modelo, ano, preco, cor)
        )
        conn.commit()
        cursor.close()
        conn.close()
       
        return redirect(url_for('veiculos'))
       
    return render_template('veiculo_form.html')




@app.route('/veiculo/editar/<int:id>', methods=['GET', 'POST'])
def veiculo_editar(id):
    #Edita um veiculo existente."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano = request.form['ano']
        preco = request.form['preco']
        cor = request.form['cor']


        cursor.execute("""
            UPDATE veiculos
            SET marca=%s, modelo=%s, ano=%s, preco=%s, cor=%s
            WHERE id=%s
            """, (marca, modelo, ano, preco, cor, id))
           
        conn.commit()
        cursor.close()
        conn.close()
           
        return redirect(url_for('veiculos'))


    cursor.execute("SELECT * FROM veiculos WHERE id=%s", (id,))
    veiculo = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('veiculo_form.html', veiculo=veiculo)


@app.route('/veiculo/deletar/<int:id>', methods=['POST'])
def veiculo_deletar(id):
    #Deleta veiculo pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM  veiculos WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('veiculos'))


#------------------Rotas Vendas-----------------
@app.route('/vendas')
def vendas():
    #Lista todas as vendas com dados do cliente e do veiculo"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    cursor.execute("""
        SELECT
            v.id,
            c.nome AS cliente_nome,
            ve.marca AS veiculo_marca,
            ve.modelo AS veiculo_modelo,      
            ve.cor AS veiculo_cor,
            v.valor,
            v.data_venda
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN veiculos ve ON v.veiculo_id = ve.id
        ORDER BY v.data_venda DESC
    """)
    vendas = cursor.fetchall()


    cursor.close()
    conn.close()
    return render_template('vendas.html', vendas = vendas)


@app.route('/venda/nova', methods=['GET', 'POST'])
def venda_nova():
    #Cadastrar uma nova venda"""


    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    """Busca clientes e veiculos para o form"""
    cursor.execute("SELECT id, nome FROM clientes")
    clientes = cursor.fetchall()
    cursor.execute("SELECT id, marca, modelo FROM veiculos")
    veiculos = cursor.fetchall()
   
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        veiculo_id = request.form['veiculo_id']
        valor = request.form['valor']


        cursor.execute(
            "INSERT INTO vendas (cliente_id, veiculo_id, valor) VALUES(%s, %s, %s)",
            (cliente_id, veiculo_id, valor)
        )
        conn.commit()
        cursor.close()
        conn.close()
           
        return redirect(url_for('vendas'))


    cursor.close()
    conn.close()
    return render_template('venda_form.html', clientes = clientes, veiculos = veiculos)


@app.route('/venda/editar/<int:id>', methods=['GET', 'POST'])
def venda_editar(id):
    #Edita uma venda existente."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)


    #Busca cliente e veiculos para o dropdown
    cursor.execute("SELECT id, nome FROM clientes")
    clientes = cursor.fetchall()
    cursor.execute("SELECT id, marca, modelo FROM veiculos")
    veiculos = cursor.fetchall()


    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        veiculo_id = request.form['veiculo_id']
        valor = request.form['valor']


        cursor.execute("""
            UPDATE vendas
            SET cliente_id = %s, veiculo_id =%s, valor = %s
            WHERE id = %s
        """, (cliente_id, veiculo_id, valor, id))
        conn.commit()
        cursor.close()
        conn.close()
           
        return redirect(url_for('vendas'))
   
    #Busca a venda atual com dados completos para exibir no form
    cursor.execute("""
        SELECT
            v.id,
            v.cliente_id,
            v.veiculo_id,
            v.valor,
            c.nome AS cliente_nome,
            ve.marca AS veiculo_marca,
            ve.modelo AS veiculo_modelo
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN veiculos ve ON v.veiculo_id = ve.id
        WHERE v.id=%s
    """, (id,))
    venda = cursor.fetchone()


    cursor.close()
    conn.close()
    return render_template('venda_form.html', venda = venda, clientes = clientes, veiculos = veiculos)




@app.route('/venda/deletar/<int:id>')
def venda_deletar(id):
    #Deleta venda pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM  vendas WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('vendas'))


# ---------- Execução ----------
if __name__ == '__main__':
    app.run(debug=True)