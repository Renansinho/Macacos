from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from autenticacao.autenticacao_dao import buscar_usuario
from myempresas.empr_rotas import empresas_blueprint
from estagiarios.estag_rotas import estag_blueprint
from autenticacao.autenticacao_dao import buscar_empresa

app=Flask(__name__)#criação da aplicação flask
app.config['SECRET_KEY'] = "Maqueicous" #A 'SECRET_KEY' é usada para proteger os dados da sessão e outras coisas sensíveis
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, RadioField
from wtforms.validators import DataRequired, Length
from autenticacao.autenticacao_service import autenticar, salvar_usuario
from autenticacao.autenticacao_dao import estagiarios, Cliente

app=Flask(__name__)#criação da aplicação flask
app.config['SECRET_KEY'] = "Maqueicous" #A 'SECRET_KEY' é usada para proteger os dados da sessão e outras coisas sensíveis



class Empresa:
    def __init__(self, cnpj, razao_social, email_empr, senha_empr, cep_empr, tel_empr, certificados_empr):
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.email_empr = email_empr
        self.senha_empr = senha_empr
        self.cep_empr = cep_empr
        self.tel_empr = tel_empr
        self.certificados_empr = certificados_empr


        
        
empresas = [
    Empresa('15245632521456', 'Mercadinho Renan', 'mercadinho.renan@gmail.com', 'renan321', '58300000', '83981819023', 'xxxxxxx')
]



class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField ("senha", validators=[DataRequired(), Length(min=3)])

class RegistroForm(FlaskForm):
    email_acad = StringField("email_acad", validators=[DataRequired()])
    senha_esta = PasswordField("senha_esta", validators=[DataRequired(), Length(min=4)])
    nome_esta = StringField("nome_esta", validators=[DataRequired()])
    cpf = StringField("cpf", validators=[DataRequired(), Length(max=11)])
    tel_esta = StringField("tel_esta", validators=[DataRequired(), Length(max=11)])
    genero_esta = RadioField('Gênero', choices=[('female', 'Feminino'), ('male', 'Masculino'), ('others', 'Outros')])

    
def buscar_esta_cadastrado(email_acad):
    for dado in estagiarios:
        if dado.email_acad == email_acad:
            return dado
   
    return None

def criar_cadastro_esta(usuario):
    estagiarios.append(usuario)
    #Esta função recebe um objeto de usuário como entrada e o adiciona à lista estagiarios


@app.route("/cadastro_esta", methods = ['GET', 'POST'])
def cadastro():
    registroform = RegistroForm() #Cria uma instância do formulário de registro 
    
    if request.method == 'GET':
        return render_template('cadastro_esta.html', form=registroform)
    
    
    if request.method == 'POST':
        print(registroform.email_acad.data,
            registroform.senha_esta.data,
            registroform.nome_esta.data,
            registroform.cpf.data,
            registroform.tel_esta.data,
            registroform.genero_esta.data)
        if not registroform.validate_on_submit():
            flash("Dados obrigatorios não preenchidos")
            return render_template("cadastro_esta.html", form=registroform)
    
    #Se o formulário for válido, cria um objeto Cliente com as informações do 
    # estagiário e tenta salvar o usuário usando a função salvar_usuario.
        usuario = Cliente(
            registroform.email_acad.data,
            registroform.senha_esta.data,
            registroform.nome_esta.data,
            registroform.cpf.data,
            registroform.tel_esta.data,
            registroform.genero_esta.data, 
        )

        try:
            salvar_usuario(usuario)
            flash("Usuário cadastrado com sucesso")
            return redirect(url_for("login"))
        except:
            flash("Usuário já cadastrado")
            return render_template("cadastro_esta.html", form=registroform)
    return render_template("cadastro_esta.html", form=registroform)


def buscar_usuario(email): #função para veyrificar se o usuario já está cadastrado
    for estagiario in estagiarios: #buscar usuario para saber se ele já ta cadastrado
    
        if estagiario.email_acad == email:                                      #se o email queeu forneci no login é igual a um deles que está na lista
            return estagiario                                                        #vai retornar os dados do estagiário no código
    
    return None #se colocar o return none dentro na identação vários emails irão dar errado ao acontecer o login, por isso que tem q ser fora

def validar_login (email, senha): 

    usuario_encontrado = buscar_usuario(email)#


    if usuario_encontrado == None:
        raise Exception ("Usario não encontrado")
    
    if not usuario_encontrado.senha_esta == senha:#se a senha que o cara preencheu no login não for encontrada, sobe a mensagem de erro
        raise Exception ("Senha Incorreta")
    
    return usuario_encontrado.email_acad


@app.route('/')
def main():
    return redirect(url_for('login'))



@app.route("/login",  methods=['POST', 'GET'])
def login():
    form=LoginForm() #CRIAR INSTANCIA NA PÁGINA LOGIN



    if request.method == "POST": #pra ficar visivel o que está sendo enviado
        
        if not form.validate_on_submit(): #se o que está no formulario não tiver correto, essa mensagem sobe na tela
            flash ("Email ou Senha Incorreta") #se email ou senha estiverem errados entrarão nesse if
            return redirect(url_for("login"))
        
        
        try:#Se a validação for bem-sucedida, o email do usuário é armazenado na sessão.
            validacao = validar_login(form.email.data, form.senha.data) #para buscar o email e senha que foi enviado no formulario
            session["Usuario"] = validacao #se usuario conseguiu validar o login dele, então esse cara existe e pode mudar de rota.
            return redirect ("/catalogo") #
            #o session: Se as credenciais estiverem corretas, o email do usuário é armazenado na sessão e o usuário é redirecionado para a rota /catalogo
        
        except:
            flash ("Email ou Senha Incorreta")
        
    
    return render_template ("teste.html", form = form) #form=form está passando a instância do formulário para a página HTML para que ela possa exibir o formulário e interagir com os dados enviados pelo usuário.


@app.route("/catalogo")
def catalogo():
    if session.get("Usuario",None):   #função só permite que usuario entre no catalogo se ele já estiver logado
        return render_template("catalogo.html")
    flash("Faça o login!")
    return redirect(url_for("login"))

@app.route("/escolha")
def escolha():
    return render_template("escolha.html")


@app.route("/cadastro_empr")
def cadastro_empr():
    return render_template("cadastro_empr.html")


@app.route("/esta_cadastrado")
def cadastrado():
    if session.get("Cliente", None):
        return render_template("teste.html")
    flash("Cadastre-se corretamente")
    return redirect(url_for("cadastro_esta"))

@app.route ("/contato")
def contato():
    return render_template("contato.html")

@app.route("/perfil_empr")
def perfil_empresa():
    return render_template("perfil_empr.html")

@app.route("/perfil_esta")
def perfil_estagiario():
    return render_template("perfil_esta.html")


if __name__=='__main__':
    app.run(debug=False)

app.register_blueprint(empresas_blueprint)
app.register_blueprint(estag_blueprint)

class LoginForm(FlaskForm):
    senha = PasswordField ("senha", validators=[DataRequired(), Length(min=4)])
    cpf_cnpj = StringField("cpf_cnpj", validators=[DataRequired()])

def validar_login(cpf_cnpj, senha):
    usuario_encontrado = buscar_usuario(cpf_cnpj)  # Supondo que você tenha uma função buscar_usuario que busca tanto estagiários quanto empresas
    empresa_encontrada = buscar_empresa(cpf_cnpj)

    if not usuario_encontrado and not empresa_encontrada :
        raise Exception("Estagiário ou Empresa não encontrados")

    if usuario_encontrado:
        if len(cpf_cnpj) == 11:  #se o comprimento for 11, é provavelmente um CPF (estagiário)
            if usuario_encontrado.senha_esta != senha:
                raise Exception("Senha incorreta")
            return "catalogo_esta.html"

    if empresa_encontrada:
        if len(cpf_cnpj) == 14:  #se o comprimento for 14, é provavelmente um CNPJ (empresa)
            if empresa_encontrada.senha_empresa != senha:
                raise Exception("Senha incorreta")
            return "catalogo_empr.html"

    else:
        raise Exception("Tipo de usuário inválido")



@app.route('/')
def main():
    return redirect(url_for('login'))




@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()  # CRIAR INSTÂNCIA NA PÁGINA LOGIN

    if request.method == "POST":
        if not form.validate_on_submit():
            flash("CPF/CNPJ ou senha incorretos")
            return redirect(url_for("login"))

        try:
            pagina_html = validar_login(form.cpf_cnpj.data, form.senha.data)
            session["Usuario"] = form.cpf_cnpj.data  #salvar o CPF/CNPJ na sessão
            return render_template(pagina_html)

        except Exception as e:
            flash("CPF/CNPJ ou senha incorretos: " + str(e))

    return render_template("teste.html", form=form)

@app.route("/catalogo")
def catalogo():
    if session.get("Usuario",None):   #função só permite que usuario entre no catalogo se ele já estiver logado
        return render_template("catalogo_empr.html")
    flash("Faça o login!")
    return redirect(url_for("login"))

@app.route("/escolha")
def escolha():
    return render_template("escolha.html")

@app.route("/cada_empresa")
def cada_empresa():
    return render_template("cadastro_empr")

@app.route("/perfil_esta")
def perfil_esta():
    return render_template("perfil_esta.html")

if __name__=='__main__':
    app.run(debug=False)

