# Descrição
Sistema de controle de estoque para papelarias feito com python, django e bootstrap.

# Executando o projeto
## Dependências
``` console
~$ pip install Django==2.2.6 django-crispy-forms==1.14.0 fpdf
```

## Migrações e conta administradora
### Migrações
``` console
~$ python manage.py makemigrations
~$ python manage.py makemigrations estoque
~$ python manage.py migrate
```

### Criando uma conta administradora
``` console
~$ python manage.py createsuperuser
```

### Executando o servidor
```
~$ python manage.py runserver
```

## Adicionando a loja central
1. Visite a página admin do Django localhost:port/admin (http://localhost:8000/admin - padrão) e insira as informações do admin criado (createsuperuser)
2. Na seção ESTOQUE, selecione Adicionar na linha/opção Empresas
3. Em Usuário selecione a conta admin criada
4. Desmarque a opção Filial, insira um endereço e salve
5. Selecione ENCERRAR SESSÃO (canto superior direito)
