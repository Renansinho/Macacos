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

