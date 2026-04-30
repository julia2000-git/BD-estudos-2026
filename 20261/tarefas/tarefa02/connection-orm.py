from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, VARCHAR, ForeignKey
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import sessionmaker

USER = 'postgres'
PASS = 'postgres'
HOST = 'localhost'
PORT = '5432'
DB   = 'atividadesBD-ODBC' # Nome do banco que você criou no pgAdmin

# Models
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


engine = create_engine(f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB}")
print("Tentando conectar via ORM...")

Session = sessionmaker(bind=engine)
session = Session()

try:
    with engine.connect() as conexao_bd:
        print("Conexão com o banco de dados realizada com sucesso!")


        # Questão 6 da Tarefa - ODBC e ORM
        # item a. Inserir uma atividade em algum projeto

        nova_atividade = Atividade(
            descricao = 'Monitoria - Atividade 2',
            projeto = 2,
            data_inicio = '2026-04-29',
            data_fim = '2026-04-30'
        )

        session.add(nova_atividade) # Adiciona a nova atividade
        session.commit()      # Salva no banco
        print("Objeto inserido com sucesso!")


        # item b. Atualizar o líder de algum projeto

        

except Exception as e:
    print(f"Erro: {e}")