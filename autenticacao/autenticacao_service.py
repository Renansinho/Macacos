from autenticacao.autenticacao_dao import buscar_usuario_por_login, criar
from autenticacao.autenticacao_dao import buscar_empresa_por_login, criar_empresa

def autenticar(email_acad, senha_esta):
    usuario = buscar_usuario_por_login(email_acad)#para tentar encontrar um usuário com o email especificado

    if usuario == None:
        raise Exception("Usuário não cadastrado")

    return usuario.senha == senha_esta
    #retorna true se der certo, ou False se der errado



def autenticar_empresa (cnpj, senha_empresa):
    empresa = buscar_empresa_por_login(cnpj)#para tentar encontrar um usuário com o email especificado

    if empresa == None:
        raise Exception("Empresa não cadastrada")

    return empresa.senha == senha_empresa




def salvar_usuario(usuario):
    dado = buscar_usuario_por_login(usuario.email_acad)

    if dado != None:
        raise Exception("Usuário já cadastrado")

    criar(usuario)



def salvar_empresa(empresa):
    dado = buscar_empresa_por_login(empresa.cnpj)


    if dado!= None:
        raise Exception("Empresa já cadastrada")
    
    criar_empresa(empresa)