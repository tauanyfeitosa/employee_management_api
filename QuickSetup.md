<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=00c4cc&height=120&section=header"/>


[![Typing SVG](https://readme-typing-svg.herokuapp.com/?color=add8e6&size=35&center=true&vCenter=true&width=1000&lines=HELLO,+Bem-Vindo,+caro+usuário!;Aqui+tem+um+guia+com+tudo+que+precisa+saber!!!;Fique+tranquilo+e+relaxe!+É+super+simples!)](https://git.io/typing-svg)

<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <h3 align="center">⌨️ Quick Setup</h3>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com/?lines=Está+preparado?;Vamos+lá!!!&font=Fira%20Code&center=true&width=380&height=50&duration=4000&pause=1000">
</p>
<!-- markdownlint-enable MD033 -->

# ⚡ ATENÇÃO!!!

Antes de tudo, é bom lembrar com estar por dentro sobre as tecnologias que estamos usando e nossos desafios. Se encontrar algum problema para configuração, entre em contato!

## Mergulhando no Projeto

- Pré Requisitos:
1. Python 3.10
2. Docker

### Passo 1: Clonando o sistema

Para obter uma cópia local do código fonte, você precisará clonar o repositório. Siga estas etapas:

1. Abra o terminal (no macOS e no Linux) ou o prompt de comando/PowerShell (no Windows).
2. Navegue até o diretório onde você deseja que o repositório seja clonado.
3. Digite o seguinte comando e pressione Enter:

```bash
git clone https://github.com/tauanyfeitosa/employee_management_api
```
### Passo 2: Crie seu ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Passo 3: Instale as dependências

```bash
pip install -r requirements.txt
```

### Configure suas variáveis de ambiente

Essas variáveis são necessárias para o banco.

1. Crie um arquivo `.env` na raiz do projeto
2. Copie o que está no arquivo `.envsample` e mude as váriáveis passíveis de mudança (user e senha)

### Passo 4: Subindo o Docker

Abra seu Rancher ou Docker Desktop e rode o comando abaixo no terminal do projeto:

```bash
docker-compose up -d --build
```

### Passo 5: Acesse o bash do conteiner web

Ainda no terminal do projeto, coloque o comando abaixo:

```bash
docker exec web bash
```

### Passo 6: Rode as migrations:

Dentro do bash, rode o comando abaixo

```bash
python manage.py migrate
```

Você agora está pronto para iniciar sua aplicação!!!

Recomendo que crie o superuser antes de iniciar o sistema. Use o comando 

```bash
python manage.py createsuperuser
```

Informe um cnpj válido, pois há validação na criação!!! Guarde seus dados de login e senha



