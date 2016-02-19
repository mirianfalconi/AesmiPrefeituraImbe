from flask import Flask, render_template, json, request, redirect, session, url_for, jsonify
from hash import User
from forms import SignForm, RegistrationForm, SignIn, IndexProtocoloForm, ComunicadoForm, RegistrationCurso
from db import acessa_proc, acessa_sql
from momentjs import Markup, momentjs
from flask_weasyprint import HTML, render_pdf


app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

app.secret_key = 'why would I tell you my secret key?'

app.jinja_env.globals['momentjs'] = momentjs


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('user'):
        name = session.get('user')
        bairro = acessa_sql('SELECT bairro FROM BAIRRO;')
        form = RegistrationForm(request.form)
        return render_template('cadastro.html', form=form, bairro=bairro, name=name)
    else:
        return redirect(url_for('signin'))


@app.route('/escola/<cpf>/')
@app.route('/escola', methods=['POST', 'GET'], defaults={'cpf': '000.000.000-00'})
def escola(cpf):
    if session.get('user'):
        name = session.get('user')
        local = acessa_sql('select local from LOCAL')
        form = RegistrationCurso(request.form)
        return render_template('escola.html', form=form, local=local, name=name, cpf=cpf)
    else:
        return redirect(url_for('signin'))


@app.route('/postEscola', methods=['POST', 'GET'])
def postEscola():
    form = RegistrationCurso(request.form)
    cpf = request.form.get('cpf')
    instituicao = request.form.get('instituicao')
    sql = str(cpf), form.curso.data, instituicao
    local = request.form.get('local')
    locais = request.form.get('locais')
    insti = request.form.get('insti')
    if locais:
        if insti:
            acessa_sql('INSERT INTO INSTITUICAO (ID_local, instituicao) VALUES((select ID_local from LOCAL where local=' + locais + '),' + insti + ');')
            print 1
        else:
            print locais
            sql = 'INSERT INTO LOCAL (local) VALUES ("' + locais + '");'
            data = acessa_sql(sql)
            print data
    if insti:
        if not locais:
            print 3
            acessa_sql('INSERT INTO INSTITUICAO (ID_local, instituicao) VALUES((select ID_local from LOCAL where local=' + local + '),' + insti + ');')
    acessa_proc('sp_insertInfo_escola', sql)
    return redirect('/admin')


@app.route('/setInstituicao', methods=['POST', 'GET'])
def setInstituicao():
    local = request.args.get('local').encode('utf8')
    parametros = str(local,)
    data = acessa_sql('select instituicao from INSTITUICAO I, LOCAL L where L.ID_local=I.ID_local AND local=\'' + parametros + '\'')
    if data is None:
        return redirect('/escola')
    return jsonify(instituicao=data)


@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    app.logger.debug(search)
    curso = acessa_sql('select curso from CURSO')
    cursos = []
    [cursos.append(x) for xs in curso for x in xs]
    return jsonify(json_list=cursos)


@app.route('/postForm', methods=['GET', 'POST'])
def postForm():
    form = RegistrationForm(request.form)
    sql = form.cpf.data, form.nome.data, form.rg.data, form.bairro.data, form.rua.data, form.casa.data, form.phone.data
    cpf = form.cpf.data
    acessa_proc('DADOS', sql)
    acessa_proc('sp_uploadParaAlunos', sql)
    if not cpf:
        cpf = '000.000.000-00'
    return redirect(url_for('escola',cpf=cpf))


@app.route('/add', methods=['GET', 'POST'])
def add():
    cpf = request.args.get('cpf').encode('utf8')
    parametros = cpf,
    data = acessa_proc('sp_selectInserteParaAlunos', parametros)
    if data is None:
        return redirect('/admin')
    else:
        nome = data[0][0]
        rg = data[0][1]
        bairro = data[0][4]
        rua = data[0][2]
        casa = data[0][3]
        phone = data[0][5]
    return jsonify(nome=nome, rg=rg, bairro=bairro, rua=rua, casa=casa, phone=phone)


@app.route('/')
def index():
    data = acessa_proc('sp_selectComunicado', '8')
    return render_template('index.html', data=data)


@app.route('/grafico')
def grafico():
    if session.get('user'):
        name = session.get('user')
        return render_template('grafico.html', name=name)
    else:
        return redirect(url_for('signin'))


@app.route('/graficoInfo')
def graficoInfo():
    datas = acessa_proc('sp_selectQTDAlunos', '8')
    adata = []
    for aluns in datas:
        a = (aluns[0], aluns[1], (str(aluns[2])))
        adata.append(a)
    fields = ["alunos", "year", "name"]
    data = [dict(zip(fields, d)) for d in adata]
    return json.dumps(data)


@app.route('/protocolos', methods=['POST', 'GET'])
def protocolos():
    if session.get('user'):
        name = session.get('user')
        data  = acessa_proc('sp_selectProtocolo', '8')
        return render_template('protocolos.html', name=name, data=data)
    else:
        return redirect(url_for('signin'))


@app.route('/indexProtocolo', methods=['POST', 'GET'])
def indexProtocolo():
    form = IndexProtocoloForm(request.form)
    sql = form.assunto.data, form.email.data, form.cpf.data
    if form.assunto.data is not None:
        acessa_proc('InsereProtocolo', sql)
    return render_template('protocolo.html', form=form)


@app.route('/relatorio/', methods=['POST', 'GET'], defaults={'name': 'mirian@hotmail.com'})
@app.route('/relatorio/<name>/')
def relatorio(name):
    if session.get('user'):
        name = session.get('user')
        dado = acessa_proc('sp_selectRelatorioCompleto', '8')
        return render_template('relatorio.html', name=name)
    else:
        return redirect(url_for('signin'))

@app.route('/print_<name>.pdf')
def print_pdf(name):
    return render_pdf(url_for('externo', name=name))


@app.route('/externo/<name>/', methods=['POST', 'GET'])
def externo(name):
    return render_template('externo.html', name=name)


@app.route('/controle', methods=['POST', 'GET'])
def controle():
    if session.get('user'):
        name = session.get('user')
        form = ComunicadoForm(request.form)
        sql = form.assuntos.data, name
        if form.assuntos.data is not None:
            dados = acessa_proc('InsereComunicado', sql)
            print dados
        return render_template('controle.html', name=name, form=form)
    else:
        return redirect(url_for('signin'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/admin')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignIn(request.form)
    try:
        _username = request.form['user']
        _password = form.password.data

        data = acessa_sql('SELECT PASSWD FROM PASS WHERE LOGIN="'+ _username +'";')

        if len(data) > 0:
            me = User(_username, _password)
            if me.verifica_password(str(data[0][0]), _password):
                session['user'] = _username
                return redirect('/admin')
            else:
                return render_template('signin.html', error='Email ou senha errados.', form=form)
        else:
            return render_template('signin.html', error='Email ou senha errados.', form=form)

    except:
        return render_template('signin.html', form=form)


@app.route('/showSignUp')
def showSignUp():
    if session.get('user'):
        name = session.get('user')
        form = SignForm(request.form)
        return render_template('signup.html', form=form, name=name)
    else:
        return redirect(url_for('signin'))


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if session.get('user'):
        form = SignForm(request.form)
        name = session.get('user')
        if request.method == 'POST' and form.validate():
            acessa_login(form.username.data, form.email.data, form.password.data)
            return redirect('/admin')
        return render_template('signup.html', form=form, name=name)
    else:
        return json.dumps({'error': 'Acesso Negado.'})


def acessa_login(_name, _email, _password):
    me = User(_email, _password)
    _hashed_password = me.seta_password(_password)
    parametros = _email, _hashed_password, _name
    acessa_proc('sp_createUser', parametros)


if __name__ == "__main__":
    app.run(app.config['IP'], app.config['PORT'], debug=True)

