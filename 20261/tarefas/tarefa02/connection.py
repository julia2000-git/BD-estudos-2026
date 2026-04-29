import pyodbc

# Iniciando a conexão com o BD
conn = pyodbc.connect("DSN=PostgresAtvODBC;") #nome do DSN foi: PostgresAtvODBC
# Criação do cursor para executar os comandos
cursor = conn.cursor()

try:
    
    # Etapa 1: vamos fazer a criação das tabelas
    with open('esquema_create_tables.sql', 'r', encoding='utf-8') as arq_create:
        sql_criar_tabelas = arq_create.read()

    cursor.execute(sql_criar_tabelas) # cursor executa a função
    conn.commit() # salva a criação

    print("Sucesso! As tabelas da atividade foram criadas1")

    # Etapa 2: vamos inserir os dados nas tabelas
    
    # Criar um cursor para executar comandos SQL
    #cursor = conn.cursor()
    #cursor.execute("SELECT version();")
    #row = cursor.fetchone()
    #print(f"Versão do Banco: {row[0]}")
    
except Exception as e:
    print(f"Erro na conexão: {e}")

finally:
    # 2. Fecha tudo ao final
    cursor.close()
    conn.close()
