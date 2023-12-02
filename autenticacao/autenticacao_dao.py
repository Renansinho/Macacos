from extensoes import db
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

def buscar_esta(): #cadasttro estagiário
    cursor = db.connect.cursor()
    cursor.execute("SELECT email_acad, senha_esta, nome_estag, cpf_estag, telef_estag, genero_esta FROM ESTAGIARIOS")
    resultado = cursor.fetchall()
    lista = []
    for valor in resultado:
        lista.append(Cliente(valor[1], valor[2], valor[3], valor[4], valor[5], valor[6]))
    return lista

def buscar_usuario_por_login(login):
    cursor = db.connect.cursor()
    cursor.execute("SELECT cpf_estag, senha_esta FROM ESTAGIARIOS WHERE cpf_estag = %s", [login])
    resultado = cursor.fetchone()
    return Usuario(resultado[0], resultado[1], None, None) if resultado else None
    
    #for dado in estagiarios:
     #   if dado.cpf_cnpj == login:
      #      return dado
#Ela percorre a lista estagiarios e compara o
#  atributo email_acad de cada objeto Cliente com 
# o login fornecido. Se encontrar um objeto com o 
# mesmo e-mail, ela retorna esse objeto Cliente.
    #return None

def buscar_por_cpfcnpj_esta(cpf_cnpj):
    cursor = db.connect.cursor()
    cursor.execute(
        "SELECT cpf_estag,  FROM ESTAGIARIOS where cpf_estag = %s" 
        [cpf_cnpj],
    )
    resultado = cursor.fetchone()
    estagiario = Cliente(resultado[0])
    estagiario.cpf_cnpj = resultado[0]
    return estagiario

def salvar_estag(estagiarios: Cliente):
    connection = db.connect
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO estagiarios (email_acad, senha_esta, nome_estag, cpf_estag, telef_esta, cep_estag) VALUES (%s, %s, %s, %s)",
        [estagiarios.email_acad, estagiarios.senha_esta, estagiarios.nome_estag, estagiarios.cpf_estag, estagiarios.telef_estag, estagiarios.cep_estag]
    )
    connection.commit()











def buscar_empr(): #cadastro empresa
    cursor = db.connect.cursor()
    cursor.execute("SELECT cnpj_empr, nome_empr, email_empr, rua_empr, cidade_empr, logradouro_empr, cep_empr, telef_empr, uf_empr FROM EMPRESAS")
    resultado2 = cursor.fetchall()
    lista2 = []
    for valor in resultado2:
        lista2.append(Empresa(valor[1], valor[2], valor[3], valor[4], valor[5], valor[6], valor[7]))
    return lista2

def buscar_empresa_por_login(login):
    for deido in empresas:
        if deido.cpf_cnpj == login:
            return deido
    return None  

def buscar_por_cnpj_empr(cnpj_empr):
    cursor = db.connect.cursor()
    cursor.execute(
        "SELECT cnpj_empr,  FROM ESTAGIARIOS where cnpj_empr = %s" 
        [cnpj_empr],
    )
    resultado2 = cursor.fetchone()
    empresa = Empresa(resultado2[0])
    empresa.cnpj_empr = resultado2[0]
    return empresa      

def salvar_empresa(empresas: Empresa):
    connection = db.connect
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO empresas (cnpj_empr, nome_empr, email_empr, cep_empr, telef_empr FROM EMPRESAS)"
        [empresas.cnpj_empr, empresas.nome_empr, empresas.email_empr, empresas.cep_empr, empresas.telef_empr, empresas.cep_estag, empresas.tipo_empr]
    )


    connection.commit()


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
