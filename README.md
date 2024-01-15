# visualizador-pem

Aplicação de visualização para o resultado de estudos com os programas da cadeia oficial de planejamento energético (NEWAVE, DECOMP e DESSEM).

A versão atual consiste em uma aplicação em [dash](https://dash.plotly.com/) para interagir diretamente com os resultados das execuções dos modelos após serem processadas pelos programas de síntese:

- [sintetizador-newave](https://github.com/rjmalves/sintetizador-newave)
- [sintetizador-decomp](https://github.com/rjmalves/sintetizador-decomp)
- [sintetizador-dessem](https://github.com/rjmalves/sintetizador-dessem)

Além da exibição dos resultados, a aplicação permite que sejam salvas comparações feitas no passado por meio da entidade `estudo`. É possível definir estudos que sejam compostos por rodadas `simples` dos modelos de planejamento ou por um conjunto de rodadas `encadeadas`. Os estudos e casos que são salvos são armazenados em bancos de dados relacionais, sendo que por padrão o banco adotado é um baseado em arquivo único localmente armazenado [sqlite](https://www.sqlite.org/index.html). Desta forma, é uma possível dependência da aplicação a existência do pacote `sqlite3` no sistema operacional, bem como o suporte adequado do pacote nativo de `python`.

## Dependências

A comunicação com sistema de arquivos para extração de resultados é feita através da [result-api](https://github.com/rjmalves/result-api), que deve estar instalada no cluster onde são executados os casos, com o devido acesso ao sistema de arquivos.

O acesso ao banco de dados relacional é feito com o uso de um `ORM` provido pelo módulo [SQLAlchemy](https://www.sqlalchemy.org/). O processamento de dados é feito com [pandas](https://pandas.pydata.org/) e [numpy](https://numpy.org/) e os gráficos são feitos com [plotly](https://plotly.com/python/), devido ao suporte nativo do `dash`, e uma combinação de [geopandas](https://geopandas.org/en/stable/) e [networkx](https://networkx.org/) para o gráfico de bolotário.


## Instalação

Apesar de ser um módulo `python`, o visualizador não está disponível nos repositórios oficiais. Para realizar a instalação, é necessário fazer o download do código a partir do repositório e fazer a instalação manualmente:

```
$ git clone https://github.com/rjmalves/visualizador-pem
$ cd visualizador-pem
$ pip install -r requirements.txt
```

## Configuração

A configuração da aplicação pode ser feita através de um arquivo de variáveis de ambiente `.env`, existente no próprio diretório de instalação. O conteúdo deste arquivo:

```
MODE="PROD"
HOST="0.0.0.0"
PORT=5050
RESULT_API="http://localhost:8080/api/v1/results/results"
GRAPHS_UPDATE_PERIOD=6000000
CURRENT_STATE_UPDATE_PERIOD=30000
URL_PREFIX="/"
SYNTHESIS_DIR="sintese"
NEWAVE_DIR="newave"
DECOMP_DIR="decomp"
SECRET_KEY="test"
USER="user"
PASSWORD="password"
```

O campo `MODE` configura o servidor em modo de produção (`PROD`) ou desenvolvimento (`DEV`), alterando a velocidade de resposta de alguns componentes e a interface de visualização, que recebe opções de debug.

Os campos `HOST` e `PORT` são usados para configuração do servidor http, de maneira padrão como em outras APIs. O campo `RESULT_API` deve conter o endpoint http que o visualizador usa para aquisitar resultados.

Através de `GRAPHS_UPDATE_PERIOD` e `CURRENT_STATE_UPDATE_PERIOD` é possível controlar as taxas de atualização dos gráficos e da tabela de estado atual dos casos em um estudo encadeado, para consideração de novos dados.

O campo `URL_PREFIX` permite o encadeador ser servido em um API Gateway com um prefixo customizado. Os campos `SYNTHESIS_DIR`, `NEWAVE_DIR` e `DECOMP_DIR` são diretórios para compatibilizar o acesso a resultados conforme foram gerados por outras ferramentas, como os programas `sintetizador-newave`, `sintetizador-decomp` e `sintetizador-dessem` e o `encadeador-pem`.

Os parâmetros `SECRET_KEY`, `USER` e `PASSWORD` controlam a parte de autenticação do visualizador, que é feita no esquema de usuário único, visto que esta é uma solução simples para a finalidade para a qual foi concebido, que é servir à gerência como um todo.


Atualmente as opções suportadas são:

|              Campo               |   Valores aceitos   |
| -------------------------------- | ------------------- |
| MODE                             | `str`               |
| HOST                             | `str`               |
| PORT                             | `int`               |
| RESULT_API                       | `str` (URL)         |
| GRAPHS_UPDATE_PERIOD             | `int` (ms)          |
| CURRENT_STATE_UPDATE_PERIOD      | `int` (ms)          |
| URL_PREFIX                       | `str`               |
| SYNTHESIS_DIR                    | `str`               |
| NEWAVE_DIR                       | `str`               |
| DECOMP_DIR                       | `str`               |
| SECRET_KEY                       | `str`               |
| USER                             | `str`               |
| PASSWORD                         | `str`               |

## Uso

Para executar o programa, basta interpretar o arquivo `main.py`:

```
$ source ./venv/bin/activate
$ python main.py
```

Ao iniciar a aplicação em modo `PROD`, são exibidos apenas os logs essenciais das tarefas executadas:

```
2024-01-10 20:09:20,873 INFO: Inicializando DB em sqlite:////home/pem/rotinas/visualizador-pem/data.db
2024-01-10 20:09:21,723 INFO: Serving on http://0.0.0.0:5051
2024-01-10 20:15:02,022 INFO: AUTH: False - /visualizador/encadeador/backtest-cpamp-2024
2024-01-10 20:15:02,814 INFO: Carregando TELA - backtest-cpamp-2024
2024-01-10 20:18:08,719 INFO: AUTH: False - /visualizador/login
2024-01-10 20:18:14,008 INFO: LOGIN: Sucesso. Usuario: pem - /visualizador/login
2024-01-10 20:18:14,315 INFO: AUTH: True - /visualizador/
2024-01-10 20:18:20,246 INFO: AUTH: True - /visualizador/encadeador
2024-01-10 20:18:28,719 INFO: Redirecionando TELA - backtest-cpamp-2024
2024-01-10 20:18:30,704 INFO: AUTH: True - /visualizador/encadeador/backtest-cpamp-2024
2024-01-10 20:18:31,439 INFO: Carregando TELA - backtest-cpamp-2024
2024-01-10 20:22:21,292 INFO: Redirecionando TELA - backtest-cpamp-2024
2024-01-10 21:30:48,571 INFO: AUTH: True - /visualizador/encadeador/backtest-cpamp-2024
2024-01-10 21:30:49,307 INFO: Carregando TELA - backtest-cpamp-2024
2024-01-11 01:39:24,279 INFO: AUTH: False - /visualizador/encadeador/backtest-cpamp-2024
2024-01-11 01:39:25,169 INFO: Carregando TELA - backtest-cpamp-2024
2024-01-11 01:40:02,795 INFO: Obtendo dados - ENCADEADOR (TEMPO, {'programa': 'NEWAVE'})
```