import sqlite3

class bd:
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('banco_dados.db')
        self.c = self.con.cursor()

    def create_table(self, table):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {table} (
                        id INTEGER PRIMARY KEY,
                        nome TEXT UNIQUE,
                        preco TEXT
                        )''')
        self.con.commit()
    
    def inserir_table(self, nome, preco):
        self.c.execute('''INSERT OR IGNORE INTO resultados(nome, preco) VALUES (?,?)''', (nome, preco))
        self.con.commit()

    def selectAll(self):
        self.c.execute('SELECT nome, preco FROM resultados')
        return self.c.fetchall()