# Bot-Contas (WhatsApp + Google Planilhas)

Script em Python que lê uma planilha do Google Planilhas e envia, pelo WhatsApp Web, a mensagem de cada linha para o telefone indicado. Depois do envio, marca a linha como enviada. Usa apenas ferramentas gratuitas.

De forma 'Semi-manual' para evitar bloqueios pela meta

(Sempre que aparecer *SPREADSHEET* me refiro ao google planilhas :3)

## Como funciona

1. Lê a planilha via API do Google (OAuth, com `gspread`).
2. Para cada linha com `status = x` (pendente), abre o WhatsApp Web com `pywhatkit`, pressiona Enter com `pyautogui` e fecha a aba.
3. Atualiza o `status` da linha para `s` (enviada).

Obs.: Funciona só com o *WhatsApp Web já logado* no navegador padrão e com a tela do computador liberada (o script controla teclado e mouse). 

--- Não mexa no computador durante a execução. ---

## Formato da planilha

A primeira linha deve ter, no mínimo, as colunas (a ordem não importa, maiúsculas/minúsculas também não):

| Coluna | Descrição |
|---|---|
| `telefone` | Número com código do país e DDD, só dígitos (ex.: `5511999999999`) |
| `mensagem` | Texto final a enviar (pode ser montado por fórmula na própria planilha) |
| `status` | `x` = pendente, `s` = enviada | (você pode persnalizar a sua a depender da necessidade)

Outras colunas (nome, valores, cálculos etc.) são livres. Veja `exemplo_planilha.csv`. Dica: use formatação condicional na coluna `status` (`x` vermelho, `s` verde).

## Instalação

```bash
git clone https://github.com/Diogo-Alves87/bot-contas-whatsapp.git
cd bot-contas-whatsapp
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
```

## Credenciais do Google

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/) e crie um projeto.
2. Ative as APIs *Google Sheets API* e *Google Drive API*.
3. Em *APIs e serviços > Tela de consentimento OAuth*, configure o app (modo teste) e adicione seu e-mail como usuário de teste.
4. Em *Credenciais*, crie um *ID do cliente OAuth* do tipo *App para computador* e baixe o JSON.
5. Salve o arquivo como `credentials/credentials_bot.json`.

Na primeira execução, o navegador abrirá para você autorizar o acesso; o token fica salvo em `credentials/authorized_user.json`.

## Configuração

```bash
copy .env.example .env     # Linux/macOS: cp .env.example .env
```

Edite o `.env` e preencha `SPREADSHEET_ID` (trecho da URL da planilha entre `/d/` e `/edit`). Os demais valores têm padrões razoáveis; aumente `WAIT_TIME` se o WhatsApp Web demorar a carregar, ou diminua caso ache que está lento de mais.

## Uso

```bash
python bot_contas.py
```

## Segurança

- *Nunca* envie ao GitHub o `.env`, `credentials_bot.json` ou `authorized_user.json` (o `.gitignore` já os ignora).
- Se algum desses arquivos for publicado por engano, revogue as credenciais no Google Cloud e gere novas.

## Limitações e avisos

- A automação depende da interface do WhatsApp Web e de tempos de espera; pode falhar se o layout mudar.

- Use apenas para enviar mensagens a pessoas que esperam recebê-las. Envio em massa ou não solicitado pode levar ao bloqueio do número pelo WhatsApp.

- Não é usual para grandes volumes, para um uso mais comercial, tente a API oficial do WhatsApp Business.

## Atualizações

- Estudarei alguma forma de manter a aba do whatsapp aberta.

**PROJETO EM DESENVOLVIMENTO, PODE NÃO REPRESENTAR O PROJETO FINAL**

## Licença

MIT. Veja [LICENSE](LICENSE).
