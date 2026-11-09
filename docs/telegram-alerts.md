# Alertas de falha no Telegram

Toda DAG envia uma mensagem no Telegram quando uma task falha depois de esgotar os
retries. É opcional: sem a Variable abaixo, o alerta é ignorado e o projeto roda normalmente.

A verificação de freshness usa o mesmo alerta. Se uma tabela bronze passar do prazo, a mensagem
também chega aqui, inclusive quando a DAG de carga está pausada e não falhou.

## 1. Criar o bot

1. No Telegram, abra uma conversa com **@BotFather**.
2. Envie `/newbot` e escolha um nome e um username.
3. Guarde o **token** que ele responder, no formato `123456789:AAE...`.

## 2. Descobrir o chat id

1. Envie qualquer mensagem para o seu bot.
2. Abra `https://api.telegram.org/bot<TOKEN>/getUpdates` no navegador.
3. O número em `"chat":{"id":...}` é o seu **chat id**.

## 3. Configurar no Airflow

Em **Admin > Variables**, crie a Variable abaixo. O token nunca entra no código nem no repo.

| Key | Value |
|---|---|
| `telegram` | `{"bot_token": "<token>", "chat_id": "<chat id>"}` |

Uma Variable criada pela UI some no `astro dev kill`. Para mantê-la, use o bloco `variables`
do `airflow_settings.yaml`, que fica fora do Git.

Quando uma task falhar, a mensagem chega assim:

```
🚨 Airflow task failed
DAG: <id da DAG>
Task: <id da task>
Logs: http://localhost:8080/...
```
