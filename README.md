# Descrição
Sistema de controle de estoque para papelarias feito com python, django e bootstrap

# "Rodando" o projeto
## Instale as dependências
``` console
$ pip install Django==2.2.6 django-crispy-forms==1.14.0 fpdf
```

## Migrações e conta administradora
``` console
$ python manage.py makemigrations
$ python manage.py makemigrations estoque
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

## Adicionando a loja central
- Visite a página admin do Django localhost:port/admin (http://localhost:8000/admin - padrão) e insira as informações do admin criado (createsuperuser)
- Na seção ESTOQUE, selecione Adicionar na linha/opção Empresas
- Em Usuário selecione a conta admin criada
- Desmarque a opção Filial, insira um endereço e salve
- Selecione ENCERRAR SESSÃO (canto superior direito)
