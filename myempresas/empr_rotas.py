from flask import Blueprint
from wtforms import StringField, EmailField, PasswordField, RadioField
from flask import Flask, render_template, request, redirect, url_for, flash, session
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from autenticacao.autenticacao_dao import empresas, Empresa
from autenticacao.autenticacao_service import  autenticar_empresa, salvar_empresa 
from autenticacao.autenticacao_dao import buscar_empresa_cadastrada

#dentro da criação da minha blueprint, eu coloco o nome dela, passo a variável "global name" (__name__)
empresas_blueprint = Blueprint('enterprise', __name__, template_folder='templates') #estou mostrando a aplicação que 
                                                        #o meu template folder é o que está dentro da pasta "empresas"

class RegistroFormEmpresa(FlaskForm):
    nome_empresa = StringField("nome_empresa", validators=[DataRequired()])
    cnpj = StringField("cpf_cnpj" , validators=[DataRequired()])
    email_empresa = EmailField("email_empresa", validators=[DataRequired()])
    tel_empresa = StringField("tel_empresa", validators=[DataRequired(), Length(max=14)])
    senha_empresa = PasswordField("senha_empresa", validators=[DataRequired(), Length(min=4)])
    cep_empresa = StringField("cep_empresa", validators=[DataRequired(), Length(max=9)])
    empresa = RadioField('empresa', choices=[('empreendedor_individual', 'Empresa Individual'), ('eireli', 'Eireli'), ('mei', 'Microoemprededor Individual'), ('other', 'Outros')])



@empresas_blueprint.route("/cadastro_empr",  methods = ['GET', 'POST'])
def cadastro_empr():
    registroformempresa = RegistroFormEmpresa()
    
    if request.method == 'GET':
        return render_template('cadastro_empr.html', form=registroformempresa)
    
    if request.method == 'POST':

        if not registroformempresa.validate_on_submit():
            print(registroformempresa.errors)
            flash("Dados obrigatorios não preenchidos")
            return render_template("cadastro_empr.html", form=registroformempresa)
        
        cnpj_novo = registroformempresa.cnpj.data
        if buscar_empresa_cadastrada(cnpj_novo):
            flash("Empresa já cadastrada com esse CNPJ")
            return render_template("cadastro_empr.html", form=registroformempresa)
        
        empresa = Empresa(
            registroformempresa.cnpj.data,
            registroformempresa.nome_empresa.data,
            registroformempresa.email_empresa.data,
            registroformempresa.senha_empresa.data,
            registroformempresa.cep_empresa.data,
            registroformempresa.tel_empresa.data,
            registroformempresa.empresa.data, 
        )
        try:
            salvar_empresa(empresa)
            flash("Empresa cadastrada com sucesso")
            return redirect(url_for("login"))
        except:
            flash("Empresa já cadastrada")
            return render_template("cadastro_empr.html", form=registroformempresa)
    return render_template("cadastro_empr.html", form=registroformempresa)


@empresas_blueprint.route("/cadastro_empresa")
def cadastro_empresa():
    return render_template("cadastro_empr.html")

@empresas_blueprint.route("/empr_cadastrada")
def empr_cadastrada():
    if session.get("Empresa", None):
        return render_template("teste.html")
    flash("Cadastre-se corretamente")
    return redirect(url_for("cadastro_empr"))




