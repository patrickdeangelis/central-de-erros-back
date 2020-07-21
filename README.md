# Central de Erros - Backend
Aplicativo destinado a ser o projeto prático da Aceleração de Python da Codenation, patrocinada pela Stone.

[![Build Status](https://travis-ci.com/patrickdeangelis/central-de-erros-back.svg?branch=master)](https://travis-ci.com/patrickdeangelis/central-de-erros-back)

## Demonstração
* backend: https://error-center-logs.herokuapp.com/
* frontend: https://logs-central.netlify.app/
 
## Repositório frontend
* link: https://github.com/patrickdeangelis/central-de-erros-front

## Como testar localmente?
1. Clone o repositório
2. Crie um virtualenv com Python 3.6+
3. Ative o seu virtualenv
4. Instale as dependecias
5. Configure a instancia com o .env
6. Execute os testes

```console
git clone https://github.com/patrickdeangelis/central-de-erros-back.git
cd central-de-erros-back
python -m venv .venv
source .venv/bin/activate
pip install -r requiriments-dev.txt
cp env-sample.env .env
python manage.py test
```

## como fazer o deploy?
1. Crie uma instância no heroku
2. Envie as configurações para o heroku
3. Defina uma SECRET_KEY segura para a instância
4. Defina DEBUG=False
5. Configure o serviço de email
6. envie o código para o heroku

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=seu_secret_key
heroku config:set DEBUG=False
# configura o email
git push heroku master --force
```      
