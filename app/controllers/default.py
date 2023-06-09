from app import app
from app.models.instituicao import Instituicao
from app.database import db

@app.route("/")
def index():
 
    try:

        # Executa uma consulta no banco de dados
        instituicaos = Instituicao.query.all()
        
        # Verifica se a consulta retornou resultados
        if instituicaos:
            # Retorna o número de usuários no banco de dados
            return f"Número de usuários no banco de dados: {len(instituicaos)}"
        else:
            return "Não há usuários no banco de dados"
    except Exception as e:
        return f"Erro ao acessar o banco de dados: {str(e)}"