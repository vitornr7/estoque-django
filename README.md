# Descrição
Sistema de controle de estoque para papelarias feito com python, django e bootstrap.

# Executando o projeto
## Instale as Dependências
``` console
~$ pip install Django==2.2.6 django-crispy-forms==1.14.0 fpdf
```

## Faça as migrações
``` console
~$ python manage.py makemigrations
~$ python manage.py makemigrations estoque
~$ python manage.py migrate
```

## Crie uma conta administradora
``` console
~$ python manage.py createsuperuser
```

## Execute o servidor
``` console
~$ python manage.py runserver
```

## Adicione uma loja central
1. Visite a página admin do Django localhost:port/admin (http://localhost:8000/admin - padrão) e insira as informações do admin criado (createsuperuser)
2. Na seção ESTOQUE, selecione Adicionar na linha/opção Empresas
3. Em Usuário selecione a conta admin criada
4. Desmarque a opção Filial, insira um endereço e salve
5. Selecione ENCERRAR SESSÃO (canto superior direito)
