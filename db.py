import mysql.connector

db = mysql.connector.connect(user="root"
                            ,host="127.0.0.1"
                            ,database="Renan"
                            ,password="Ter@bait")

try:
    connection = db
    if connection is not None:
        print("Conexão com o banco de dados estabelecida com sucesso!")
        try:
            cursor = connection.cursor()
            result = cursor.execute("SELECT * FROM ESTAGIARIOS")
            rows = cursor.fetchall()

            print(rows)
            
            print("Cursor criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar o cursor: {e}")
    else:
        print("Conexão com o banco de dados é 'None'. Ocorreu um problema.")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")