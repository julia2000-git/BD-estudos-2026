import pyodbc

try:
    # O nome aqui deve ser o que você escreveu em "Data Source"
    conn = pyodbc.connect("DSN=PostgresAtvODBC;") #nome do DSN foi: PostgresAtvODBC
    print("Sucesso! Python e PostgreSQL conectados via ODBC.")
    
    # Criar um cursor para executar comandos SQL
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    row = cursor.fetchone()
    print(f"Versão do Banco: {row[0]}")
    
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {e}")
