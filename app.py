from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, RadioField
from wtforms.validators import DataRequired, Length
from autenticacao.autenticacao_service import autenticar, salvar_usuario
from autenticacao.autenticacao_dao import estagiarios, Cliente
from autenticacao.autenticacao_dao import empresas, Empresa
from autenticacao.autenticacao_service import  autenticar_empresa, salvar_empresa 


app=Flask(__name__)#criação da aplicação flask
app.config['SECRET_KEY'] = "Maqueicous" #A 'SECRET_KEY' é usada para proteger os dados da sessão e outras coisas sensíveis




class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField ("senha", validators=[DataRequired(), Length(min=3)])

class RegistroForm(FlaskForm):
    email_acad = StringField("email_acad", validators=[DataRequired()])
    senha_esta = PasswordField("senha_esta", validators=[DataRequired(), Length(min=4)])
    nome_esta = StringField("nome_esta", validators=[DataRequired()])
    cpf = StringField("cpf", validators=[DataRequired(), Length(max=14)])
    tel_esta = StringField("tel_esta", validators=[DataRequired(), Length(max=11)])
    genero_esta = RadioField('Gênero', choices=[('female', 'Feminino'), ('male', 'Masculino'), ('others', 'Outros')])

class RegistroFormEmpresa(FlaskForm):
    nome_empresa = StringField("nome_empresa", validators=[DataRequired()])
    cnpj = StringField("cnpj", validators=[DataRequired(), Length(max=17)])
    email_empresa = EmailField("email_empresa", validators=[DataRequired()])
    tel_empresa = StringField("tel_empresa", validators=[DataRequired(), Length(max=14)])
    senha_empresa = PasswordField("senha_empresa", validators=[DataRequired(), Length(min=4)])
    cep_empresa = StringField("cep_empresa", validators=[DataRequired(), Length(max=9)])
    empresa = RadioField('empresa', choices=[('empreendedor_individual', 'Empresa Individual'), ('eireli', 'Eireli'), ('mei', 'icrooemprededor Individual')])



def buscar_esta_cadastrado(cpf):
    for dado in estagiarios:
        if dado.cpf == cpf:
            return dado
   
    return None


def buscar_empresa_cadastrada(cnpj):
    for dado in empresas:
        if dado.cnpj == cnpj:
            return dado
   
    return None

def criar_cadastro_esta(usuario):
    estagiarios.append(usuario)
    #Esta função recebe um objeto de usuário como entrada e o adiciona à lista estagiarios


def criar_cadastro_esta(empresa):
    empresas.append(empresa)


@app.route("/cadastro_empr", endpoint="cadastro2", methods = ['GET', 'POST'])
def cadastro_empr():
    registroformempresa = RegistroFormEmpresa()
    
    if request.method == 'GET':
        return render_template('cadastro_empr.html', form=registroformempresa)
    
    if request.method == 'POST':

        if not registroformempresa.validate_on_submit():
            flash("Dados obrigatorios não preenchidos")
            return render_template("cadastro_empr.html", form=registroformempresa)
        
        empresa = Empresa(
            registroformempresa.nome_empresa.data,
            registroformempresa.cnpj.data,
            registroformempresa.email_empresa.data,
            registroformempresa.tel_empresa.data,
            registroformempresa.senha_empresa.data,
            registroformempresa.cep_empresa.data,
            registroformempresa.empresa.data, 
        )
        try:
            salvar_empresa(empresa)
            flash("Empresa cadastrada com sucesso")
            return redirect(url_for("login"))
        except:
            flash("Empresa já cadastrado")
            return render_template("cadastro_empre.html", form=registroformempresa)
    return render_template("cadastro_empr.html", form=registroformempresa)


@app.route("/cadastro_esta", endpoint="cadastro1", methods = ['GET', 'POST'])
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
            flash("Estagiário cadastrado com sucesso")
            return redirect(url_for("login"))
        except:
            flash("Estagiário já cadastrado")
            return render_template("cadastro_esta.html", form=registroform)
    return render_template("cadastro_esta.html", form=registroform)


def buscar_usuario(cpf): #função para veyrificar se o usuario já está cadastrado
    for estagiario in estagiarios: #buscar usuario para saber se ele já ta cadastrado
    
        if estagiario.cpf == cpf:                                      #se o email queeu forneci no login é igual a um deles que está na lista
            return estagiario                                                        #vai retornar os dados do estagiário no código
    
    return None #se colocar o return none dentro na identação vários emails irão dar errado ao acontecer o login, por isso que tem q ser fora

def buscar_empresa(cnpj):
    for empresa in empresas:
        
        if empresa.cnpj == cnpj:
            return empresa
    
    return None


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
        return render_template("catalogo_empr.html")
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

@app.route("/empr_cadastrada")
def empr_cadastrada():
    if session.get("Empresa", None):
        return render_template("teste.html")
    flash("Cadastre-se corretamente")
    return redirect(url_for("cadastro_empr"))



if __name__=='__main__':
    app.run(debug=False)
