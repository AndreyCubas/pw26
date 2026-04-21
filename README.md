# FinTrack Django

Aplicação web de controle financeiro desenvolvida com Django para cadastrar gastos, acompanhar metas financeiras, visualizar indicadores em dashboard e consultar relatórios filtráveis por período e categoria.

## Descrição do projeto

O projeto oferece uma interface web para gerenciamento financeiro pessoal, com autenticação de usuários e áreas dedicadas para:

- dashboard com indicadores resumidos;
- cadastro, edição e exclusão de gastos;
- acompanhamento de metas financeiras;
- relatórios com filtros por período e categoria;
- formulário de contato;
- administração de dados pelo Django Admin.

## Tecnologias utilizadas

- Python 3.11+
- Django 5.2
- PostgreSQL
- Bootstrap 5
- Bootstrap Icons
- HTML5, CSS3 e templates Django

## Pré-requisitos

Antes de executar o projeto, você precisa ter instalado:

- Python 3.11 ou superior
- `pip`
- PostgreSQL acessível localmente ou remotamente
- Git (opcional, para clonar o repositório)

## Instalação

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd FinanceDjango
```

### 2. Crie e ative um ambiente virtual

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

Como o projeto não possui `requirements.txt` no momento, instale manualmente:

```bash
pip install django psycopg[binary]
```

### 4. Configure o banco de dados

O projeto está preparado para PostgreSQL. Revise a configuração em `pw2026/settings.py` e ajuste a conexão com o seu banco antes de rodar em outro ambiente.

Se preferir, você pode adaptar a configuração para usar variáveis de ambiente ou SQLite durante o desenvolvimento.

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor

```bash
python manage.py runserver
```

## Como usar

Após iniciar o servidor, acesse `http://127.0.0.1:8000/`.

### Passo a passo de uso

1. Acesse a página inicial do sistema.
2. Clique em `Criar conta` para cadastrar um novo usuário.
3. Faça login para liberar o acesso ao dashboard.
4. Cadastre gastos em `Gastos > Novo gasto`.
5. Crie objetivos em `Metas > Nova meta`.
6. Acompanhe os indicadores e gráficos no `Dashboard`.
7. Use a tela de `Relatórios` para filtrar dados por período e categoria.
8. Acesse `/admin` com um superusuário para gerenciar registros pelo painel administrativo.

## Funcionalidades principais

- autenticação de usuários com login, logout e cadastro;
- controle de gastos por título, categoria, valor, data e recorrência;
- metas com valor-alvo, valor atual, prazo e progresso percentual;
- dashboard com métricas e gráficos de apoio;
- relatórios com filtros dinâmicos;
- formulário de contato persistido em banco de dados.

## Exemplos de funcionamento

Adicione capturas de tela ou GIFs nesta seção para demonstrar a interface do sistema. Exemplo de organização:

```md
![Dashboard do sistema](docs/images/dashboard.png)
![Cadastro de gastos](docs/images/gastos.png)
![Fluxo de uso](docs/images/demo.gif)
```

Sugestões de imagens para incluir:

- tela de login/cadastro;
- dashboard principal;
- tela de gastos;
- tela de metas;
- exemplo de relatório filtrado.

## Estrutura resumida do projeto

```text
FinanceDjango/
|- manage.py
|- db.sqlite3
|- pw2026/
|  |- settings.py
|  |- urls.py
|- website/
|  |- models.py
|  |- forms.py
|  |- views.py
|  |- services.py
|  |- templates/
|- static/
   |- css/
```

## Contato

Autor identificado no projeto: João Valério  
GitHub: [https://github.com/Joao-Valerio](https://github.com/Joao-Valerio)

Se desejar, você pode complementar esta seção com e-mail, LinkedIn ou outros canais de contato.

## Licença

Este repositório não possui um arquivo de licença definido até o momento.

Se o projeto for distribuído publicamente, recomenda-se adicionar uma licença, como MIT, Apache 2.0 ou outra de sua preferência.
