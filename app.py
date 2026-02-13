import mysql.connector
from mysql.connector import Error
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def create_connection():
    """Cria uma conexão com o banco de dados."""
    try:
        connection = mysql.connector.connect(
            host='35.243.184.164',
            user='helper',
            password='V2OWN-Uy4*3HuX6ce_Wk',
            database='itsm'
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def main():
    connection = create_connection()
    if connection is None:
        return 0

    cursor = connection.cursor()

    query = """
    SELECT COUNT(*)
    FROM tb_tickets
    WHERE cod_fluxo > 2000 AND status NOT IN ('Cancelado', 'Finalizado')
    """

    cursor.execute(query)
    retorno = cursor.fetchone()
    print(f"Total: {retorno[0]}")

    query = """
    SELECT cod_fluxo
    FROM tb_tickets
    WHERE cod_fluxo > 2000 AND status NOT IN ('Cancelado', 'Finalizado')
    """

    cursor.execute(query)
    retorno = cursor.fetchall()

    contador = 0

    for cod_fluxo in retorno:
        url = "https://kora-api-gxb53d5kyq-rj.a.run.app/sla"

        payload = json.dumps({
            "cod_fluxo": cod_fluxo[0],
            "N° Ticket": cod_fluxo[0]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload).json()

        result = {
            "cod_fluxo": cod_fluxo[0],
            "data": response.get("data")
        }

        print(result)
        contador += 1

    cursor.close()
    connection.close()

    return contador

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
