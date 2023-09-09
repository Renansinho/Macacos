from autenticacao.autenticacao_dao import buscar_usuario_por_login, criar


def autenticar(login, senha):
    usuario = buscar_usuario_por_login(login)#para tentar encontrar um usuário com o email especificado

    if usuario == None:
        raise Exception("Usuário não cadastrado")

    return usuario.senha == senha
    #retorna true se der certo, ou False se der errado





def salvar_usuario(usuario):
    dado = buscar_usuario_por_login(usuario.email_acad)

    if dado != None:
        raise Exception("Usuário já cadastrado")

    criar(usuario)