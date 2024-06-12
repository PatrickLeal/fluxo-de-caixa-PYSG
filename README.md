# App Fluxo de Caixa simples com o padrão MVC

Desenvolvido com a boblioteca **PySimpleGUI**
## Tecnologias:
  * Python
  * SQLite
## Estrutura dos diretórios
```
my_project/
├── src/
│   ├── controllers/
│   │   ├── categoria_register_controller.py
│   │   └── movimentacao_register_controller.py
│   ├── models/
│   │   ├── categorias.py
│   │   └── movimentacao.py
|   |
│   ├── services/
|   |   ├── conexao_database.py
|   |   └── FX_CAIXA.db
│   └── views/
│       ├── categoria_register_view.py
│       └── movimentacao_register_view.py/
├── process_handle.py
└── run.py
```
## Imagens do app
<div style="display: inline_block" align="left"><br>
 <img width="500" height="400" src="https://github.com/PatrickLeal/fluxo-de-caixa-PYSG/blob/main/src/images/tela-movimentacoes.jpg" alt="movimentacoes"/>
 <img width="300" height="400" src="https://github.com/PatrickLeal/fluxo-de-caixa-PYSG/blob/main/src/images/tela-categorias.jpg" alt="categorias"/>
</div>

## Instalando dependências:
```
pip install -r requirements.txt
 ```

## Rodando o app:
``` 
python run.py
```
