# NotebookLM (Gemini Notebook) por useapi.net

**Autor:** useapi · **Versão:** 0.1.1 · **Tipo:** ferramenta · **Código-fonte:** https://github.com/useapi/notebooklm-api/tree/main/dify-plugin · **Contato:** support@useapi.net

Use o Google **NotebookLM**, agora chamado **Gemini Notebook**, em workflows, chatflows e agentes do Dify. Crie notebooks, adicione páginas web, vídeos do YouTube, texto, arquivos do Google Drive e uploads como fontes, faça perguntas respondidas com citações, rode o Deep Research e gere todos os resultados do Studio: **Visões gerais em áudio** (o podcast do NotebookLM), **Visões gerais em vídeo**, apresentações de slides, infográficos, relatórios, tabelas de dados, testes, cartões de estudo e mapas mentais. Áudio, vídeo, slides e imagens voltam como arquivos do Dify.

> Este plugin usa a [Gemini Notebook API](https://useapi.net/docs/api-gemini-notebook-v1?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin) da useapi.net, uma API de terceiros. Ela não é feita pelo Google, nem afiliada ou endossada por ele. É preciso ter uma assinatura da useapi.net (US$ 15/mês, cobre todas as APIs da useapi.net) e sua própria conta Google. A geração usa o plano do NotebookLM dessa conta Google, inclusive o gratuito, sem cobrança por chamada da useapi.net.

O Google não oferece API do NotebookLM para contas Google comuns; a única, a Gemini Notebook Enterprise API, exige licenças Enterprise em um projeto do Google Cloud. Este plugin funciona com uma conta Google comum.

## Configuração

1. **Pegue um token de API da useapi.net.** Assine e copie o token: [Setup useapi.net](https://useapi.net/docs/start-here/setup-useapi?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin).
2. **Conecte sua conta Google uma vez.** Siga o [Setup Gemini Notebook](https://useapi.net/docs/start-here/setup-gemini-notebook?utm_source=marketplace.dify.ai&utm_medium=referral&utm_campaign=dify-plugin): basta entrar com o Google, sem copiar cookies e sem projeto do Google Cloud. Cada assinatura cobre 3 contas Google (até 100), e os novos jobs são distribuídos entre elas.
3. **Instale o plugin** pelo Marketplace do Dify (procure "NotebookLM") ou envie o `.difypkg` dos [releases no GitHub](https://github.com/useapi/notebooklm-api/releases) em Plugins > Instalar plugin > Arquivo de pacote local.
4. **Autorize.** Em Ferramentas, abra "NotebookLM (Gemini Notebook) por useapi.net", clique em Autorizar e preencha:

| Credencial | Obrigatória | O que é |
|---|:-:|---|
| Token de API da useapi.net | Sim | O token do passo 1. O Dify guarda como segredo. |
| E-mail padrão da conta Google | Não | Qual conta Google conectada usar quando uma ferramenta precisar. Deixe vazio para a useapi.net escolher a conta menos ocupada. |

Ao salvar, o plugin faz uma chamada rápida, `GET /accounts`, para confirmar que o token funciona e que há ao menos uma conta Google conectada.

### Requisitos de conexão

O plugin se conecta apenas a `https://api.useapi.net/v1/gemini-notebook` por HTTPS, com o token no cabeçalho `Authorization: Bearer`. Um Dify auto-hospedado precisa de saída HTTPS para `api.useapi.net`.

## Ferramentas

São 56 ferramentas, uma por tarefa, com as opções da API em listas de seleção. A lista completa com os endpoints está no README em inglês.

- **Contas e jobs**: listar contas Google, ver uso da conta, listar jobs em execução, ver status do job, cancelar job.
- **Notebooks**: listar, criar, obter, renomear, excluir e copiar notebooks, guia do notebook, ver e alterar o compartilhamento.
- **Fontes**: adicionar URLs/YouTube/texto/Google Drive/Play Livros, enviar arquivo, obter, renomear e excluir fontes, sincronizar fonte do Drive, acrescentar texto, pesquisar nas fontes, listar Play Livros.
- **Chat**: perguntar ao notebook (com citações), histórico, limpar chat, configurar estilo e tamanho das respostas.
- **Pesquisa**: Descobrir fontes (rápida) ou Deep Research, e importar os resultados.
- **Resultados do Studio**: Visão geral em áudio (podcast), Visão geral em vídeo, slides, infográfico, relatório, relatório interativo, tabela de dados, teste, cartões de estudo, mapa mental, gerar um item sugerido, tentar de novo um artefato com falha e revisar um slide.
- **Artefatos**: listar, obter, baixar, excluir e exportar para Google Docs ou Planilhas.
- **Notas, rótulos e coleções**: listar/criar/excluir notas e convertê-las em fontes, rotular fontes, listar/criar/atualizar coleções.

As ferramentas de geração aceitam um ID de `notebook` ou `urls` e/ou `text` para criar um notebook na hora. Por padrão elas aguardam até 120 segundos e retornam o texto, os arquivos e variáveis de workflow. Se o job ainda estiver rodando, retornam uma mensagem com o `jobid`: não gere de novo, consulte com Ver status do job (que também espera até 120 segundos por chamada). Em um workflow, aumente a Espera máxima para até 540 segundos para receber o arquivo em um só nó.

## Exemplos de uso

### Workflow: links viram podcast em um nó

```
[Início: urls (parágrafo)]
   -> [NotebookLM > Gerar Visão geral em áudio (podcast)]  urls = {{Início.urls}}, formato = Análise aprofundada, duração = Curto, idioma = pt_BR
   -> [Fim: podcast = {{Gerar Visão geral em áudio.files}}, resumo = {{Gerar Visão geral em áudio.text}}]
```

### Agente: um assistente de pesquisa sobre seus notebooks

Adicione as ferramentas Listar notebooks, Obter notebook, Adicionar fontes, Perguntar ao notebook, Gerar Visão geral em áudio e Ver status do job, e escreva nas instruções: responda só com o resultado de Perguntar ao notebook, mantendo os números das citações; antes de gerar áudio ou vídeo, confirme com o usuário, pois isso consome o uso da conta Google dele.

## Espera, limites e erros

- O chat responde em 15 a 30 segundos; Descobrir fontes leva cerca de 15 segundos; Deep Research, 3 a 5 minutos; uma Visão geral em áudio, 3 a 10 minutos; uma Visão geral em vídeo, 10 minutos ou mais. O plugin consulta a cada 15 segundos e, por padrão, espera até 120 segundos por chamada (em workflows, até 540 segundos, abaixo do limite padrão de 600 segundos do Dify para plugins).
- Cada conta Google tem o próprio limite de uso do NotebookLM, renovado a cada 5 horas, mais um limite semanal. Ver uso da conta mostra o que resta.
- Os erros voltam como mensagens legíveis, por exemplo: token inválido (401), assinatura vencida (402), conta não conectada (404), fontes ainda em processamento (409), conta ocupada ou sem uso disponível, com o horário de renovação (429), conta desconectada pelo Google (596).

## Privacidade

O plugin envia pedidos só para `api.useapi.net` e não guarda nada. Veja o [PRIVACY.md](../PRIVACY.md) e os [Termos e Política de Privacidade](https://useapi.net/docs/legal) da useapi.net.

## Suporte

- Referência da API: https://useapi.net/docs/api-gemini-notebook-v1
- Exemplos de código: https://github.com/useapi/notebooklm-api
- E-mail support@useapi.net, ou pergunte no [Discord](https://discord.gg/w28uK3cnmF) ou no [Telegram](https://t.me/use_api).
