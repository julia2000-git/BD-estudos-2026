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

    print("Sucesso! As tabelas da atividade foram criadas!")

    # Etapa 2: vamos inserir os dados nas tabelas
    with open('esquema_inserts_data.sql', 'r', encoding='utf-8') as arq_insert:
        sql_inserir_dados = arq_insert.read()

    cursor.execute(sql_inserir_dados) # cursor executa a inserção
    conn.commit() # salva a inserção

    print("Sucesso! As inserções foram realizadas!")

    # Criar um cursor para executar comandos SQL
    #cursor = conn.cursor()
    #cursor.execute("SELECT version();")
    #row = cursor.fetchone()
    #print(f"Versão do Banco: {row[0]}")

    # ----------------------------------------------
    # Questão 5 da Tarefa - ODBC e ORM
    # item a. Inserir uma atividade em algum projeto

    descricao_atv = 'BD - Atividade 4'  # declaração de variáveis
    cod_projeto = 3
    data_in = '2026-03-25'
    data_f = '2026-04-28'

    sql_inserir_atv_proj = """
        INSERT INTO atividade (descricao, projeto, data_inicio, data_fim)
        VALUES
        (?, ?, ?, ?);
        """
        
    cursor.execute(sql_inserir_atv_proj, (descricao_atv, cod_projeto, data_in, data_f))
    conn.commit()
    print("A atividade foi inserida em um projeto!")

    # ----------------------------------------------
    # Item b. Atualizar o líder de algum projeto

    sql_atualizar_lider = """
        UPDATE projeto SET responsavel = 14 WHERE nome LIKE 'Monitoria';
        """
    
    cursor.execute(sql_atualizar_lider)
    conn.commit()
    print("Líder de projeto atualizado!")

    # ----------------------------------------------
    # Item c. Listar todos os projetos e suas atividades

    sql_listar_proj_atv = """
        SELECT p.codigo, p.nome as nome_proj, p.descricao as descricao_proj, p.depto as depto_proj, 
        a.descricao as nome_atvd, a.data_inicio as inicio_atvd, a.data_fim as fim_atvd 
        FROM projeto p JOIN atividade a ON p.codigo = a.projeto
        GROUP BY p.codigo, a.descricao, a.data_inicio, a.data_fim, p.nome
        ORDER BY p.nome ASC;
        """

    cursor.execute(sql_listar_proj_atv)
    conn.commit()

    print("Projetos e suas atividades listados!")

    # verificando se funcionou
    linhas = cursor.fetchall()

    if not linhas:
        print("A consulta executou, mas a tabela está vazia.")
    else:
        print(f"Sucesso! Foram encontradas {len(linhas)} linhas:")
        for linha in linhas:
            print(linha)

except Exception as e:
    print(f"Erro na conexão: {e}")

finally:
    # 2 Fechando tudo ao final
    cursor.close()
    conn.close()
