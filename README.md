# Descrição
Sistema de controle de estoque para papelarias feito com python, django e bootstrap.

# Executando o projeto
## 1. Instale as Dependências
``` console
~$ pip install Django==2.2.6 django-crispy-forms==1.14.0 fpdf
```

## 2. Faça as migrações
``` console
~$ python manage.py makemigrations
~$ python manage.py makemigrations estoque
~$ python manage.py migrate
```

## 3. Crie uma conta administradora
``` console
~$ python manage.py createsuperuser
```

## 4. Execute o servidor
``` console
~$ python manage.py runserver
```

## 5. Adicione uma loja central/distribuidora
1. Visite a página admin do Django em localhost:port/admin (porta padrão: `http://localhost:8000/admin`) e insira as informações do administrador criado com o comando createsuperuser
2. Na seção ESTOQUE, selecione Adicionar na linha/opção Empresas
3. Em Usuário selecione a conta admin criada
4. Desmarque a opção Filial, insira um endereço e salve
5. Selecione ENCERRAR SESSÃO (canto superior direito)
