import mysql.connector

db = mysql.connector.connect(user="root"
                             ,password="Ter@bait"
                             ,host="127.0.0.1"
                             ,database="renan"
)
try:
    connection = db
    if connection is not None:
        print("Conexão com o Banco de Dados estabelecida com sucesso!")
        try:
            cursor = connection.cursor()
            print("Cursor criado com sucesso")
        except Exception as e:
            print(f"Erro dao criar o cursor:{e}")
    else:
        print("Conexão com o Bando de Dados é 'None'. Ocorreu um erro")

except Exception as e:
    print(f"Erro ao conectR AO BANCO DE DADOS {e}")