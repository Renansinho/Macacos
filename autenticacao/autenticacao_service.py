from autenticacao.autenticacao_dao import buscar_usuario_por_login, criar
from autenticacao.autenticacao_dao import buscar_empresa_por_login, criar_empresa
import autenticacao.dao as autenticacao
from autenticacao.dao import Cliente
from autenticacao.dao import Empresa

def autenticar(cpf_cnpj, senha_esta):
    usuario = buscar_usuario_por_login(cpf_cnpj)#para tentar encontrar um usuário com o email especificado

    if usuario == None:
        raise Exception("Usuário não cadastrado")

    return usuario.senha == senha_esta
    #retorna true se der certo, ou False se der errado



def autenticar_empresa (cpf_cnpj, senha_empresa):
    empresa = buscar_empresa_por_login(cpf_cnpj)#para tentar encontrar um usuário com o email especificado

    if empresa == None:
        raise Exception("Empresa não cadastrada")

    return empresa.senha == senha_empresa




def salvar_usuario(usuario):
    #dado = buscar_usuario_por_login(usuario.cpf_cnpj)

    #if dado != None:
     #   raise Exception("Estagiário já cadastrado")

    #criar(usuario)
    autenticacao.salvar_estag(usuario)



def salvar_empresa(empresa):
    #deido = buscar_empresa_por_login(empresa.cpf_cnpj)


    #if deido != None:
     #   raise Exception("Empresa já cadastrada")
    
    #criar_empresa(empresa)
    autenticacao.salvar_empresa(empresa)