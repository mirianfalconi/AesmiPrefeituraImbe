from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField


class SignForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35, message='Senha muito curta')])
    password = PasswordField('New Password', [
        validators.DataRequired('Digite a sua senha'),
        validators.EqualTo('confirm', message='As senhas sao diferentes')
    ])
    confirm = PasswordField('Repeat Password')


class SignIn(Form):
    email = StringField('user', [validators.DataRequired('Digite seu email')])
    password = PasswordField('password', [validators.DataRequired('Digite a sua senha')])


class RegistrationForm(Form):
    cpf = StringField('cpf', [validators.DataRequired('Digite seu CPF')])
    nome = StringField('Nome', [validators.Length(min=6, max=65, message='Digite seu nome corretamente')])
    rg = StringField('RG', [validators.DataRequired('Digite seu RG')])
    phone = StringField('phone')
    bairro = StringField('bairro')
    rua = StringField('rua', [validators.Length(min=2, max=35, message='Digite o nome da sua rua corretamente')])
    casa = StringField('casa', [validators.Length(min=2, max=6, message='Digite o numero da sua casa')])


class RegistrationCurso(Form):
    cpf = StringField('cpf', [validators.DataRequired('Digite seu CPF')])
    curso = StringField('curso', [validators.DataRequired('Digite seu curso')])
    locais = StringField('Nome do Local', [validators.Length(max=65, message='Digite o local corretamente')])
    insti = StringField('Nome da Instituicao', [validators.Length(max=65, message='Digite a instituicao corretamente')])


class IndexProtocoloForm(Form):
    cpf = StringField('cpf', [validators.DataRequired('Digite seu CPF')])
    assunto = TextAreaField()
    email = StringField('email', [validators.DataRequired('Digite seu Email')])


class ComunicadoForm(Form):
    assuntos = TextAreaField()

