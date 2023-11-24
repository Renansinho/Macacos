class Usuario:
    def __init__(self, login, senha, nome, papel):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.papel = papel


class Cliente: 
    def __init__(self, email_acad, senha_esta, nome_esta, cpf_cnpj, tel_esta, genero_esta):
        self.email_acad = email_acad
        self.senha_esta = senha_esta
        self.nome_esta = nome_esta
        self.cpf_cnpj = cpf_cnpj
        self.tel_esta = tel_esta
        self.genero_esta = genero_esta

estagiarios = [
    Cliente('ribeiro.renan@academico.ifpb.edu.br', '1234', 'Renan Ribeiro Silba', '08731693440', '83981819023', 'Masculino')
    
]#"base de dados" temporária

class Empresa:
    def __init__(self, cpf_cnpj, nome_empresa, email_empresa, senha_empresa, cep_empresa, tel_empresa, empresa):
        self.cpf_cnpj = cpf_cnpj
        self.nome_empresa = nome_empresa
        self.email_empresa = email_empresa
        self.senha_empresa = senha_empresa
        self.cep_empresa = cep_empresa
        self.tel_empresa = tel_empresa
        self.empresa = empresa


        
        
empresas = [
    Empresa('08308794000167', 'Mercadinho Renan', 'mercadinho.renan@gmail.com', 'renan321', '58300000', '83981819023', 'Eirele')
]

def buscar_usuario_por_login(login):
    for dado in estagiarios:
        if dado.cpf_cnpj == login:
            return dado
#Ela percorre a lista estagiarios e compara o
#  atributo email_acad de cada objeto Cliente com 
# o login fornecido. Se encontrar um objeto com o 
# mesmo e-mail, ela retorna esse objeto Cliente.
    return None

def buscar_empresa_por_login(login):
    for deido in empresas:
        if deido.cpf_cnpj == login:
            return deido
    return None        

def criar(usuario):
    estagiarios.append(usuario)

def criar_empresa(empresa):
    empresas.append(empresa)    

def buscar_esta_cadastrado(cpf_cnpj):
    for dado in estagiarios:
        if dado.cpf_cnpj == cpf_cnpj:
            return dado
   
    return None


def buscar_empresa_cadastrada(cpf_cnpj):
    for dado in empresas:
        if dado.cpf_cnpj == cpf_cnpj:
            return dado
   
    return None

def buscar_usuario(cpf_cnpj): #função para veyrificar se o usuario já está cadastrado
    for estagiario in estagiarios: #buscar usuario para saber se ele já ta cadastrado
    
        if estagiario.cpf_cnpj == cpf_cnpj:                                      #se o email queeu forneci no login é igual a um deles que está na lista
            return estagiario                                                        #vai retornar os dados do estagiário no código
    
    return None #se colocar o return none dentro na identação vários emails irão dar errado ao acontecer o login, por isso que tem q ser fora

def buscar_empresa(cpf_cnpj):
    for empresa in empresas:
        
        if empresa.cpf_cnpj == cpf_cnpj:
            return empresa
    
    return None
