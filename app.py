import mysql.connector
from mysql.connector import Error
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os
from web_hook import web_hook

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL")

def create_connection():
    """Cria uma conexão com o banco de dados."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def main():
    try:
        connection = create_connection()
        if connection is None:
            return 0

        cursor = connection.cursor()

        query = """
        SELECT cod_fluxo
        FROM tb_tickets
        WHERE cod_fluxo > 2000 AND status NOT IN ('Cancelado', 'Finalizado')
        """

        cursor.execute(query)
        retorno = cursor.fetchall()

        contador = 0

        for cod_fluxo in retorno:
            # url = f"https://kora-api-gxb53d5kyq-rj.a.run.app/sla"
            print(f"Atualizando SLA do ticket {cod_fluxo[0]}")
            url = f"{BACKEND_URL}/tickets/update/sla?cod_fluxo={cod_fluxo[0]}"

            payload = {}
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload).json()

            result = {
                "cod_fluxo": cod_fluxo[0],
                "data": response
            }

            print(result)
            contador += 1

        cursor.close()
        connection.close()

        return contador
    
    except Error as e:
        print(f"Erro ao executar a consulta: {e}")
        web_hook(f" FLUXO ATUALIZAÇÃO DE SLA TICKETS \n Erro ao executar a consulta: {e}")
        return 0

if __name__ == '__main__':
    inicio = datetime.now()

    itens = main()

    fim = datetime.now()
    result = {
        "inicio": inicio.strftime('%Y-%m-%d %H:%M:%S'),
        "fim": fim.strftime('%Y-%m-%d %H:%M:%S'),
        "itens_atualizados": itens
    }

    print(result)
