from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, session
from wtforms import StringField, PasswordField, EmailField, RadioField
from flask_wtf import FlaskForm
from autenticacao.autenticacao_dao import  Cliente
from autenticacao.autenticacao_service import salvar_usuario
from wtforms import StringField, EmailField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length



estag_blueprint = Blueprint('estagi', __name__, template_folder='templates')


class RegistroForm(FlaskForm):
    email_acad = EmailField("email_acad", validators=[DataRequired()])
    senha_esta = PasswordField("senha_esta", validators=[DataRequired(), Length(min=4)])
    nome_esta = StringField("nome_esta", validators=[DataRequired()])
    cpf_cnpj = StringField("cpf_cnpj", validators=[DataRequired()])
    tel_esta = StringField("tel_esta", validators=[DataRequired(), Length(max=11)])
    genero_esta = RadioField('genero', choices=[('female', 'Feminino'), ('male', 'Masculino'), ('others', 'Outros')])


@estag_blueprint.route("/cadastro_esta", methods = ['GET', 'POST'])
def cadastro():
    registroform = RegistroForm() #Cria uma instância do formulário de registro 
     
    print(request.method)
    if request.method == 'GET':
        return render_template('cadastro_esta.html', form=registroform)

    if request.method == 'POST':
        print(registroform.cpf_cnpj.data, registroform.email_acad.data, registroform.genero_esta.data, registroform.tel_esta.data, registroform.senha_esta.data)
        
        if not registroform.validate_on_submit():
            flash("Dados obrigatorios não preenchidos")
            return render_template("cadastro_esta.html", form=registroform)
    
    #Se o formulário for válido, cria um objeto Cliente com as informações do 
    # estagiário e tenta salvar o usuário usando a função salvar_usuario.
        usuario = Cliente(
            registroform.email_acad.data,
            registroform.senha_esta.data,
            registroform.nome_esta.data,
            registroform.cpf_cnpj.data,
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

@estag_blueprint.route("/esta_cadastrado")
def cadastrado():
    if session.get("Cliente", None):
        return render_template("teste.html")
    flash("Cadastre-se corretamente")
    return redirect(url_for("cadastro_esta"))

