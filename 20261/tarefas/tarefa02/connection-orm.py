from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, VARCHAR, ForeignKey
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import sessionmaker

# Configurações Iniciais do Banco de Dados ---------------------------------

USER = 'postgres'
PASS = 'postgres'
HOST = 'localhost'
PORT = '5432'
DB   = 'atividadesBD-ODBC' # Nome do banco que você criou no pgAdmin

# Criação dos Models e Engine -------------------------------------------------------

engine = create_engine(f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")
print("Tentando conectar via ORM...")
Base = declarative_base()

class Funcionario(Base):
    __tablename__ = 'funcionario'

    # colunas da tabela funcionario viram variáveis
    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    sexo = Column(VARCHAR(1), nullable=False)
    dt_nasc = Column(Date, nullable=False)
    salario = Column(MONEY, nullable=False)
    supervisor = Column(Integer, ForeignKey('funcionario.codigo'), nullable=False)
    depto = Column(Integer, nullable=False)

class Departamento(Base):
    __tablename__ = 'departamento'

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(VARCHAR(100), unique=True, nullable=False)
    sigla = Column(VARCHAR(10), unique=True, nullable=False)
    descricao = Column(VARCHAR(250), nullable=False)
    gerente = Column(Integer, ForeignKey('funcionario.codigo'), nullable=False)

class Projeto(Base):
    __tablename__ = 'projeto'

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(VARCHAR(50), unique=True, nullable=False)
    descricao = Column(VARCHAR(250), nullable=False)
    responsavel = Column(Integer, ForeignKey('funcionario.codigo'), nullable=False)
    depto = Column(Integer, nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)


class Atividade(Base):
    __tablename__ = 'atividade'

    codigo = Column(Integer, primary_key=True, autoincrement=True)
    projeto = Column(Integer, ForeignKey('projeto.codigo'), nullable=False)
    descricao = Column(VARCHAR(250), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)

# Criação do Session ------------------------------------------------

Session = sessionmaker(bind=engine)
session = Session()

# Bloco Try/Exception ----------------------------------------------

try:
    with engine.connect() as conexao_bd:
        print("Conexão com o banco de dados realizada com sucesso!")

        # Criação das tabelas se ainda não existirem (descomentar a próxima linha)
        #Base.metadata.create_all(engine)  

        # Questão 6 da Tarefa - ODBC e ORM -------------------------
        # item a. Inserir uma atividade em algum projeto

        nova_atividade = Atividade(
            descricao = 'Monitoria - Atividade 2',
            projeto = 2,
            data_inicio = '2026-04-29',
            data_fim = '2026-04-30'
        )

        session.add(nova_atividade) # Adiciona a nova atividade
        session.commit()      # Salva no banco
        print("\n Objeto inserido com sucesso!")

        print(f" A nova atividade é: \n")
        print(f" NOME: {nova_atividade.descricao}  |  PROJETO: {nova_atividade.projeto} \n")
        print('-' * 60)


        # item b. Atualizar o líder de algum projeto

        # atualizando projeto 'BD'
        atualizar_lider_proj = session.query(Projeto).filter(Projeto.nome == 'BD').first()

        if atualizar_lider_proj:
            id_novo_lider = 4
            atualizar_lider_proj.responsavel = id_novo_lider  # coloca Josefa (codigo = 4) como responsável

            lider_atualizado = session.query(Funcionario).get(id_novo_lider)

            session.commit()
            print(" Líder de projeto atualizado com sucesso!")
            print(f" NOME DO PROJETO: {atualizar_lider_proj.nome} | Novo Líder: {lider_atualizado.nome} \n")
            print('-' * 60)

        # item c. Listar todos os projetos e suas atividades

        lista_proj_atvs = session.query(
            Projeto.codigo, Projeto.nome.label("nome_proj"), Projeto.descricao.label("proj_descricao"),
            Projeto.depto.label("depto_proj"), Atividade.descricao.label("nome_atv"),
            Atividade.data_inicio, Atividade.data_fim
            ).join(Atividade, Projeto.codigo == Atividade.projeto
            ).group_by(
                Projeto.codigo,
                Projeto.nome,
                Projeto.descricao,
                Projeto.depto,
                Atividade.descricao,
                Atividade.data_inicio,
                Atividade.data_fim
            ).order_by(
                Projeto.nome.asc()
            ).all()
        
        ultimo_projeto_id = None   # variável que faz a mudança de id

        print("=== LISTA DE PROJETOS E SUAS ATIVIDADES ===")
        
        for row in lista_proj_atvs:
            # Se o código do projeto mudou, imprime o cabeçalho do projeto
            if row.codigo != ultimo_projeto_id:
                print(f"\n PROJETO: {row.nome_proj.upper()} DESCRIÇÃO: {row.proj_descricao.upper()} (Depto: {row.depto_proj})")
                print(f"{' ' * 4}{'-' * 60}")
                print(f"{' ' * 4}{'ATIVIDADE':<30} | {'INÍCIO':<12} | {'FIM':<12}")
                ultimo_projeto_id = row.codigo
            
            # Imprime os detalhes da atividade com um recuo (identação)
            # Tratando a data caso ela venha como objeto datetime/date
            inicio = row.data_inicio.strftime('%d/%m/%Y') if row.data_inicio else "-"
            fim = row.data_fim.strftime('%d/%m/%Y') if row.data_fim else "-"

            print(f"{' ' * 4}{row.nome_atv:<30} | {inicio:<12} | {fim:<12}")
        
except Exception as e:
    session.rollback()
    print(f"Erro: {e}")

finally:
    session.close()
    print("Sessão finalizada!")