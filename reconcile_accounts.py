import csv
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple
from pprint import pprint

Transaction = Tuple[str, str, float, str]


def find_matching_transaction(
    transaction1: Transaction, transactions2: List[Transaction]
):
    """
    Encontra uma transacao entre o csvs.

    A correspondencia e baseada nos criterios:
    - Mesmo departamento
    - Mesmo valor
    - Mesmo beneficiario
    - Data com diferenca maxima de 1 dia

    Args:
        transaction1: Unica tupla de transacao.
        transactions2: Lista de transacoes.

    Returns:
        A transacao correspondente ou None, se nenhuma for encontrada.
    """
   
    date_str, transaction_department, transaction_value, transaction_beneficiary = transaction1
    transaction_date = datetime.strptime(date_str, "%Y-%m-%d")

    for transaction2 in transactions2:

        transaction2_date_str, transaction2_department, transaction2_value, transaction2_beneficiary = transaction2
        transaction2_date = datetime.strptime(transaction2_date_str, "%Y-%m-%d")

        if (
            is_same_department(transaction2_department, transaction_department)
            and is_same_value(transaction2_value, transaction_value)
            and is_same_beneficiary(transaction2_beneficiary, transaction_beneficiary)
            and is_within_one_day(transaction2_date, transaction_date)
        ):
            return transaction2

    return None


def is_same_department(dept1: str, dept2: str) -> bool:
    """
        Se mesmo departamento

        Returns:
            True
    """
    return dept1 == dept2

def is_same_value(value1: float, value2: float) -> bool:
    """
        Se mesmo valor

        Returns:
            True
    """
    return value1 == value2

def is_same_beneficiary(beneficiary1: str, beneficiary2: str) -> bool:
    """
        Se mesmo beneficiario

        Returns:
            True
    """
    return beneficiary1 == beneficiary2

def is_within_one_day(date1: datetime, date2: datetime) -> bool:
    """
        Quando houver mais de uma possibilidade de correspondência para uma dada transação, 
        ela deve ser feita com a transação que ocorrer mais cedo.

       " Se necessario o menor valor de data sera utilizado para identificar o correspondente"

        Returns:
            True
    """
    return abs((date1 - date2).days) <= 1



def reconcile_accounts(transactions1, transactions2):
    """
    Receber duas listas de listas (representando as linhas dos dados financeiros) e deve devolver cópias 
    dessas duas listas de listas com uma nova coluna acrescentada à direita das demais, 
    que designará se a transação pôde ser encontrada
    ( FOUND ) na outra lista ou não ( MISSING )

    Args:
        transactions1: Primeira lista do arquivo transactions1.csv
        transactions2: Segunda lista do arquivo transactions2.csv

    Returns:
        Duas listas reconciliadas com um valor adicional FOUND para linhas encontradas e MISSING para nao encontradas.

    """

    updated_t1 = []
    updated_t2 = []
    
    for transaction in transactions1:
        match = find_matching_transaction(transaction, transactions2)
        if match:
            updated_t1.append(transaction + ['FOUND'])
        else:
            updated_t1.append(transaction + ['MISSING'])


    for transaction2 in transactions2:
        match = find_matching_transaction(transaction2, transactions1)
        if match:
            updated_t2.append(transaction2 + ['FOUND'])
        else:
            updated_t2.append(transaction2 + ['MISSING'])


    return updated_t1, updated_t2


if __name__ == "__main__":

    transactions1 = list(csv.reader(Path('transactions1.csv').open()))
    transactions2 = list(csv.reader(Path('transactions2.csv').open()))

    out1, out2 = reconcile_accounts(transactions1, transactions2)

    pprint(out1)
    pprint(out2)