"""Bot-Contas: envia mensagens pelo WhatsApp Web a partir de uma planilha do Google Planilhas.

Resumo das funções:

Para cada linha com status "x" (pendente), envia o texto da coluna "mensagem"
para o número da coluna "telefone" e marca a linha com "s" (enviada).
"""

import os
import sys
import time

import gspread
import pyautogui
import pywhatkit
from dotenv import load_dotenv

load_dotenv()


def _env_int(nome: str, padrao: int) -> int:
    try:
        return int(os.getenv(nome, padrao))
    except ValueError:
        return padrao


# --- Configuração (veja o arquivo .env.example) ---
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE", "credentials/credentials_bot.json")
AUTHORIZED_USER_FILE = os.getenv("AUTHORIZED_USER_FILE", "credentials/authorized_user.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

WAIT_TIME = _env_int("WAIT_TIME", 10)          # segundos para o WhatsApp Web carregar
TYPE_DELAY = _env_int("TYPE_DELAY", 5)         # espera a mensagem aparecer na caixa de texto
AFTER_SEND_DELAY = _env_int("AFTER_SEND_DELAY", 3)
BETWEEN_MESSAGES = _env_int("BETWEEN_MESSAGES", 10)
CLOSE_TAB = os.getenv("CLOSE_TAB", "true").strip().lower() in ("1", "true", "sim", "yes")

COL_TELEFONE = "telefone"
COL_MENSAGEM = "mensagem"
COL_STATUS = "status"
PENDENTE = "x"
ENVIADA = "s"


def conectar_planilha():
    if not SPREADSHEET_ID:
        sys.exit("Defina SPREADSHEET_ID no arquivo .env (veja .env.example).")
    if not os.path.exists(CREDENTIALS_FILE):
        sys.exit(
            f"Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}\n"
            "Veja a seção 'Credenciais do Google' no README."
        )
    gc = gspread.oauth(
        credentials_filename=CREDENTIALS_FILE,
        authorized_user_filename=AUTHORIZED_USER_FILE,
    )
    return gc.open_by_key(SPREADSHEET_ID).sheet1


def enviar_mensagem(telefone: str, mensagem: str) -> None:
    pywhatkit.sendwhatmsg_instantly(
        phone_no="+" + telefone,
        message=mensagem,
        wait_time=WAIT_TIME,
        tab_close=False,  # a aba é fechada por nós, após o envio
    )
    time.sleep(TYPE_DELAY)           # espera a mensagem aparecer na caixa de texto
    pyautogui.press("enter")         # envia
    time.sleep(AFTER_SEND_DELAY)     # dá tempo de a mensagem sair
    if CLOSE_TAB:
        pyautogui.hotkey("ctrl", "w")  # fecha a aba para não acumular abas
#    TEMPORÁRIO       ↑

def main() -> None:
    planilha = conectar_planilha()

    dados = planilha.get_all_values()
    if not dados:
        sys.exit("A planilha está vazia.")

    cabecalho = [c.strip().lower() for c in dados[0]]
    try:
        col_tel = cabecalho.index(COL_TELEFONE)
        col_msg = cabecalho.index(COL_MENSAGEM)
        col_status = cabecalho.index(COL_STATUS)
    except ValueError as e:
        sys.exit(f"Coluna obrigatória não encontrada no cabeçalho: {e}")

    enviadas = 0

    for i, linha in enumerate(dados[1:], start=2):  # i = número da linha na planilha
        telefone = linha[col_tel].strip() if len(linha) > col_tel else ""
        mensagem = linha[col_msg].strip() if len(linha) > col_msg else ""
        status = linha[col_status].strip().lower() if len(linha) > col_status else ""

        # só envia se estiver marcada com "x" (pendente)
        if status != PENDENTE or not telefone or not mensagem:
            continue

        try:
            enviar_mensagem(telefone, mensagem)
            planilha.update_cell(i, col_status + 1, ENVIADA)
            print(f"Linha {i}: enviado")
            enviadas += 1
        except Exception as e:
            print(f"Linha {i}: erro -> {e}")

        time.sleep(BETWEEN_MESSAGES)  # pausa entre mensagens

    if enviadas == 0:
        print(
            'Nenhuma linha pendente (marque "x" na coluna status, '
            "ou verifique as colunas telefone e mensagem)."
        )
    else:
        print(f"Concluído: {enviadas} mensagem(ns) enviada(s).")


if __name__ == "__main__":
    main()
