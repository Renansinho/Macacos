from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from autenticacao.autenticacao_dao import buscar_usuario
from autenticacao.autenticacao_dao import buscar_empresa
from estagiarios.estag_rotas import estag_blueprint
from myempresas.empr_rotas import empresas_blueprint
from extensoes import db

app=Flask(__name__)#criação da aplicação flask
app.register_blueprint(empresas_blueprint)
app.register_blueprint(estag_blueprint)

estagios = []

class LoginForm(FlaskForm):
    cpf_cnpj = StringField("cpf_cnpj", validators=[DataRequired()])
    senha = PasswordField ("senha", validators=[DataRequired(), Length(min=4)])

@app.route('/')
def main():
    return redirect(url_for('login'))


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


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()  # CRIAR INSTÂNCIA NA PÁGINA LOGIN

    if  request.method == "POST":
        
        if not form.validate_on_submit():
            print("123")
            flash("CPF/CNPJ ou senha incorretos")
            return redirect(url_for("login"))
       
        try:
            pagina_html = validar_login(form.cpf_cnpj.data, form.senha.data)
            session["Usuario"] = form.cpf_cnpj.data  #salvar o CPF/CNPJ na sessão
            return render_template(pagina_html)

        except Exception as e:
            flash("CPF/CNPJ ou senha incorretos: " + str(e))

    return render_template("teste.html", form=form)


@app.route("/cada_empresa")
def cada_empresa():
    return render_template("cadastro_empr")

@app.route("/perfil_empresa")
def perfil_empresa():
    return render_template("perfil.html")

@app.route("/estagiar")
def estagiar ():

    if not(session.get("Usuario") in estagios):
        estagios.append(buscar_empresa(session.get("Usuario")))

    print (estagios)
    return redirect("/catalogo_empr")

@app.route("/p")
def p ():

    return f"{estagios[0]}"


if __name__=='__main__':
    app.run(debug=False)

