import sys
import os
sys.path.append(os.path.abspath(os.curdir))
from model.password import Password
from views.password_views import FernetHasher

action = input('Digite 1 para salvar uma senha ou 2 pra ver a senha salva: ')

if action == '1':
    if len(Password.get()) == 0:
        key, path = FernetHasher.create_key(archive = True)
        print('Chave criada, salve com cuidado ')
        print(f'Chave: {key}')
        if path:
            print('Chave salva no arquivo')
            print(f'Caminho: {path}')
        
    else:
        key = input('Digite sua chave usada para criptografia use sempre a mesma chave')

    domain = input('Domínio: ')
    password = input('Senha: ')
    fernet_user = FernetHasher(key)
    p1 = Password(domain=domain, password=fernet_user.encrypt(password).decode('utf-8'))
    p1.save()

elif action == '2':
    domain = input('Dominio: ')
    key = input('Key: ')
    fernet_user = FernetHasher(key)
    data = Password.get()

    for i in data:
        if domain in i['domain']:
            password = fernet_user.decrypt(i['mZiaJ/uPvAn3uBvXXBKAQ7iAs9D3xk8Ydw4Fe7B7SXM=password'])
    if password:
        print(f'Sua senha: {password}')
    else:
        print(f'Não encontrada nenhuma senha para: {domain}')