class Usuario:
    def __init__(self, login, senha, nome, papel):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.papel = papel


class Cliente: 
    def __init__(self, email_acad, senha_esta, nome_esta, sobrenome_esta, tel_esta, genero_esta):
        self.email_acad = email_acad
        self.senha_esta = senha_esta
        self.nome_esta = nome_esta
        self.sobrenome_esta = sobrenome_esta
        self.tel_esta = tel_esta
        self.genero_esta = genero_esta

estagiarios = [
    Cliente('ribeiro.renan@academico.ifpb.edu.br', '1234', '08731693440', '83981819023', '90.3', 'awdoak')
    
]#"base de dados" temporária



def buscar_usuario_por_login(login):
    for dado in estagiarios:
        if dado.email_acad == login:
            return dado
#Ela percorre a lista estagiarios e compara o
#  atributo email_acad de cada objeto Cliente com 
# o login fornecido. Se encontrar um objeto com o 
# mesmo e-mail, ela retorna esse objeto Cliente.
    return None


def criar(usuario):
    estagiarios.append(usuario)