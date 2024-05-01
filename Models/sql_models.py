import pyodbc

class SQL_Connection:
    def __init__(self, driver, server, database, user=None, password=None):
        # Inicializa a classe com os parâmetros de conexão
        self.connection_string = f'Driver={driver};Server={server};Database={database};'
        if user and password:
            self.connection_string += f'UID={user};PWD={password};'
        self.connection = None  # Inicializa a conexão como None

    def connect(self):
        # Método para estabelecer a conexão com o banco de dados
        try:
            self.connection = pyodbc.connect(self.connection_string)  # Tenta conectar
            print("Conexão estabelecida com sucesso.")
        except pyodbc.Error as e:
            print("Erro ao conectar:", e)  # Trata erros de conexão

    def execute_query(self, query):
        # Método para executar consultas SQL
        if self.connection:
            try:
                cursor = self.connection.cursor()  # Cria um cursor
                cursor.execute(query)  # Executa a consulta
                #cursor.close()  # Fecha o cursor
                print("Consulta executada com sucesso.")
            except pyodbc.Error as e:
                print("Erro ao executar consulta:", e)  # Trata erros de consulta
        else:
            print("Conexão não estabelecida.")  # Informa se não houve conexão

    def commit(self):
        # Método para comitar as alterações
        if self.connection:
            try:
                self.connection.commit()  # Comita as alterações
                print("Transação comitada com sucesso.")
            except pyodbc.Error as e:
                print("Erro ao comitar transação:", e)  # Trata erros de commit
        else:
            print("Conexão não estabelecida.")  # Informa se não houve conexão

    def close_connection(self):
        # Método para fechar a conexão
        if self.connection:
            self.connection.close()  # Fecha a conexão
            print("Conexão fechada.")
        else:
            print("Conexão não estabelecida.")  # Informa se não houve conexão
                   
class SQLHandler:
    def __init__(self, cursor):
        # Inicializa a classe com o cursor da conexão com o banco de dados
        self.cursor = cursor
    
    def sql_format_table(self, df, table_name):
        # Método para criar a query de criação da tabela com colunas flexíveis
        create_table_query = f'CREATE TABLE {table_name} ('
        for coluna in df.columns:
            # Determina o tipo de coluna com base no tipo de dados do DataFrame
            if df[coluna].dtype == 'object':
                tipo_coluna = 'VARCHAR(255)'
            elif df[coluna].dtype == 'int64':
                tipo_coluna = 'INT'
            elif df[coluna].dtype == 'float64':
                tipo_coluna = 'FLOAT'
            else:
                tipo_coluna = 'VARCHAR(255)'
                
            create_table_query += f'[{coluna}] {tipo_coluna}, '  # Adiciona coluna à query
            
        create_table_query = create_table_query[:-2] + ')'  # Remove a última vírgula e fecha a query
        
        self.cursor.execute(create_table_query)
    
    def sql_format_row(self,  df, table_name):
        for index, row in df.iterrows():
            colunas = ', '.join([f'[{col}]' for col in row.index])  # Colunas entre colchetes
            valores = ', '.join([f"'{val}'" for val in row.values])  # Valores entre aspas simples
            # Construindo a string SQL
            sql = f'INSERT INTO {table_name} ({colunas}) VALUES ({valores})'
            self.cursor.execute(sql)
            
    def table_exists(self, table_name):
        query = f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
        self.cursor.execute(query)
        row_count = self.cursor.fetchone()[0]
        return row_count > 0