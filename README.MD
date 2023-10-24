# Flask-restx-RAWG
Projeto de API para acesso de dados da API RAWG com cadastro de favoritos e cadastro de usuários

### Instalação
#### Clona repositório
```git clone https://github.com/AyrtonMoises/flask-restx-rawg.git```

### Criação de ambiente virtual
```python -m venv venv```

### Ativar ambiente virtual
##### Linux
```source venv/bin/activate```

##### Windows
```venv/scripts/activate```

#### Instalação de pacotes
```pip install -r requirements.txt```

#### Defina as variaveis de ambiente
Criar arquivo .env baseado no arquivo de exemplo '.env.sample'

#### Executar projeto
``` flask run ```

#### Acesso da api
[http://localhost:5000/doc]

#### Testes
```python -m pytest```

##### Criar usuário administrativo
``` flask create-user-admin admin admin admin@example.com ```

##### Cria configuração de migração
```flask db init``` 
##### Cria migrações baseado nas alterações dos models
```flask db migrate -m "Descrição da migração"``` 
##### Aplica migrações
```flask db upgrade``` 
