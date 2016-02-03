# [Atados API](http://www.atados.com.br)
[![Codeship](https://www.codeship.io/projects/139f1dd0-a88e-0131-806c-1a66b7fb6c8b/status)](https://codeship.io/projects/19157)
[![Dependency Status](https://gemnasium.com/atados/api.svg)](https://gemnasium.com/atados/api)


A ideia é simples: uma rede social na qual pessoas predispostas a praticar o bem encontram oportunidades de voluntariado.

Nosso principal objetivo é ampliar o senso de comunidade na sociedade, levando cada vez mais pessoas a entrar nessa corrente de gente boa. Afinal, tudo o que você faz bem, pode fazer bem a alguém.


## Por que colaborar com o projeto?

Porque você quer viver em uma sociedade melhor!

Porque colaborando com o Atados você estará ajudando todas as causas! Sejam elas lutar pelo direito dos animais, pelo meio ambiente, por educação de qualidade, por mais respeito aos direitos humanos entre outras. Isso mesmo!
Você vai contribuir com o trabalho de diversas ONGs que juntas apoiam todas as causas!

Já que você está aqui, provavelmente você é alguém envolvido com tecnologia.
Suas habilidades são muito valiosas para a sociedade. Colaborar com o Atados é uma forma de contribuir para o desenvolvimento coletivo fazendo algo que você faz muito bem!


## Requerimentos

- python > 2.7.10
- pip
- ElasticSearch
  -> Porta default: 9200
- PostgreSQL > 9.0.x

---

## Como rodar o projeto

O primeiro passo é clonar o projeto para sua máquina:

`git clone https://github.com/atados/api.git atados-api && cd atados-api`


## Configurações

O arquivo `environment.sh` gerencias as variáveis de ambiente da aplicação, altere esse arquivo para definir suas credenciais do banco de dados, host do ElasticSearch, etc.
Use o comando: `make generate_config`  para gerar este arquivo e em seguida altere com os dados necessário para executar a aplicação.

---

### Setup: Ubuntu
    apt-get install python-dev # Ubuntu
    sudo apt-get install postgresql-server-dev-9.3 # para build do psycopg2
    sudo apt-get install python-psycopg2

##### Setup PostgreSQL:

[PostgreSQL Setup - Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)

---

### Setup: OSX

Por default, o Python vem instalado junto com o sistema, somente sendo necessário instalar o `pip`, execute:

`sudo easy_install pip`
`make install && make run`

Caso algum erro aconteça, tente executar separadamente:

`[sudo] make install # erros de permissão`

`[sudo] pip install -r requirements.txt --ignore-installed`

 Se os erros continuarem acontecendo, uma sugestão é reinstalar o Python(o que vai corrigir as permissões das pastas), e executar o `make` novamente:

```
$ brew reinstall python
$ python --version
>> Python 2.7.10

$ make install && make run
```

#### Setup PostgreSQL

`brew install postgres` (ou  [Setup PostgreSQL OSX](http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/))

---

### Setup Database

[TODO]

-> make db
-> Seed ?

---

### Setup ElasticSearch

Simplesmente rode o processo do ElasticSearch:

`elasticsearch -d # d = daemon`

Para gerar novamente todos os indexes no ElasticSearch:

`make rebuild_index`

---

### Atualizando a versão do Python (OSX)

**Disclaimer:** Este procedimento não é necessário ou obrigatório, e atualmente também não é recomendado por questões de compatibilidade das dependências do projeto, porém você pode tentar por sua conta e risco: `:O`

---

Caso você deseje utilizar versões mais recentes do Python( > 3), execute:

`$ brew install python3`

```
$ python3 --version
>> Python 3.5.0
```

Em seguida crie os alias:

**Alias temporario**:
_(somente para a sessão aberta no terminal)_

`alias python=python3 && alias pip=pip3 `

**Alias permanente:**
_(caution: isso pode ter efeitos colaterais não desejado em seu ambiente de desenvolvimento, tenha certeza do que está fazendo)_

```
$ echo "alias python=python3\nalias pip=pip3" >> ~/.bash_profile
$ source ~/.bash_profile
```

**obs:** se você utilizar o [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) execute:

```
$ echo "alias python=python3\nalias pip=pip3" >> ~/.zshrc
$ source ~/.zshrc
```

Verifique a versão atual da instalação do `Python` e `pip`:

```
$ python --version
Python 3.5.0

$ pip --version
pip 8.0.2 from /usr/local/lib/python3.5/site-packages (python 3.5)
```

Caso prefera não criar os alias, uma alternativa é utilizar o comando make no formato:

```
sed -i "Makefile.backup" 's/@python/@python3/g' "Makefile"
sed -i "Makefile2.backup" 's/@pip/@pip3/g' "Makefile"

make install && make run
```
---

## License

MIT License (See LICENSE file).


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/atados/api/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

