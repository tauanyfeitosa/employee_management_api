<img width=100% src="https://capsule-render.vercel.app/api?type=waving&color=00c4cc&height=120&section=header"/>


[![Typing SVG](https://readme-typing-svg.herokuapp.com/?color=add8e6&size=35&center=true&vCenter=true&width=1000&lines=HELLO,+Bem-Vindo+ao+challenge+Tour+House!)](https://git.io/typing-svg)

<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <h3 align="center">⌨️ README</h3>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com/?lines=Está+preparado?;Vamos+lá!!!&font=Fira%20Code&center=true&width=380&height=50&duration=4000&pause=1000">
</p>
<!-- markdownlint-enable MD033 -->

# Employee Management API - Challenge Tour House

Antes de começarmos, pedimos que acessem o link abaixo para as configurações do sistema:

Clique aqui: [QuickSetup](https://github.com/tauanyfeitosa/employee_management_api/blob/master/QuickSetup.md)

Após essas configurações, vamos conhecer um pouco mais sobre o projeto em si.

# Descrição do Projeto

Este projeto foi elaborado como parte da avaliação de um processo seletivo. O projeto consiste no desenvolvimento em nível back-end de um sistema de gerenciamento de funcionários. As funcionalidades mínimas exigidas para o projeto em questão foram:

## Stacks
### Backend:
- A API deve ser desenvolvida utilizando **Python + Django**.
- O banco de dados pode ser **PostgreSQL** ou **SQLite3**.
- A API deve seguir o padrão **REST**.
- O código deve estar versionado no **Git** e armazenado em uma plataforma como **GitHub**, **BitBucket** ou **GitLab**.
- O arquivo **README.md** deve conter instruções objetivas para instalação, execução e utilização da aplicação.

## Regras de Negócio

### Acesso Restrito:
- A plataforma deve ser acessível somente por consultores através de login e senha.
  - **Nota:** Não é necessário desenvolver o endpoint de criação de usuário.

### Cadastro e Gerenciamento:
- Listar todas as pessoas e empresas cadastradas.
- Visualizar e editar os detalhes das pessoas e empresas.

### Informações de Funcionários:
- Nome completo.
- E-mail de contato.
- Telefone.
- Data de nascimento.
- Data de ingresso.
- Data de desligamento.
- Status de ativo/inativo.
- Cidade.
- Cada funcionário deve estar associado a uma empresa.

### Informações de Empresas:
- CNPJ.
- Logradouro.
- Cidade.
- País.
- Status de ativo/inativo.

### Inativação de Registros:
- Nenhum registro pode ser deletado, apenas inativado.


Alguns requisitos extras foram adicionados para um melhor aproveitamento do desafio, de maneira a demonstrar um pouco mais de conhecimentos técnicos, sejam gerais ou na própria linguagem. Estas regras a mais serão exibidas nos tópicos seguintes!

# Sobre a Arquitetura Escolhida

A arquitetura tem uma organização tem uma organização pensada na modularidade, extensibilidade e manutenabilidade; separando as responsabilidades em módulos claros. Vamos detalhar os aspectos favoráveis e como cada componente contribui para uma estrutura modular e escalável:

![image](https://github.com/user-attachments/assets/6f2eb11c-a3c2-4ca4-8684-4bdbce68db64)


## Separação de Contextos de Domínio

- A divisão entre `api` e `core` é clara. No diretório `api`, cada entidade, como `companies` e `employees`, possui sua própria estrutura de arquivos, incluindo `views.py`, `urls.py`, `apps.py`, e `admin.py`. Isso permite que cada entidade tenha seus próprios pontos de entrada na aplicação, facilitando a manutenção e expansão do sistema.
- O diretório `core` concentra arquivos comuns e funcionalidades reutilizáveis, que podem ser compartilhadas entre diferentes partes da aplicação, evitando duplicação de código.

## Estrutura Modular

- A divisão do `core` em subdiretórios como `entities`, `serializers`, `use_cases`, e `tests` visa a modularização e organização do código. Isso permite que cada parte da lógica da aplicação esteja separada de acordo com sua função, o que facilita a leitura e a compreensão do código.

## Encapsulamento de Lógica de Negócios (Use Cases)
- O uso de `use_cases` para validações e mensagens de erro sugere uma camada de lógica de negócio bem organizada. Centralizar a lógica de negócio em `use_cases` permite que as regras sejam reutilizadas e mantenham-se desacopladas de camadas específicas, como os serializers e views.
- Segue o princípio de "Separation of Concerns" (Separação de Responsabilidades), o que é ótimo para a escalabilidade e flexibilidade do sistema.

## Interação Estruturada entre Componentes

- O fluxo de funcionamento — onde o `use_case` faz as validações e fornece mensagens de erro, o `serializer` faz a serialização e chama o `use_case` no método `validate`, e a `view` chama o `serializer` — mostrou-se bem eficaz e expansível.
- O `serializer` atua como intermediário entre a `view` e o `use_case`, centralizando a lógica de validação e serialização. Isso permite que as `views` mantenham-se leves, focando apenas em receber requisições e enviar respostas.
- Essa estrutura ajuda na manutenção e na clareza do código, pois as responsabilidades são distribuídas de forma a evitar que as views ou serializers fiquem sobrecarregados.

## Uso de Generics para o Padrão REST

- O uso de `generics` facilita a implementação de `views` seguindo o padrão RESTful, proporcionando uma maneira simplificada de gerenciar operações CRUD. Isso mantém o código mais limpo e reutilizável, além de ser uma prática recomendada no Django Rest Framework (DRF).
- O uso de `generics` também melhora a consistência entre as `views`, facilitando a compreensão e manutenção do código.

## Organização do Código e Facilidade de Manutenção

- Ao adotar essa organização, notou-se uma melhora significativamente na manutenibilidade da aplicação. Cada módulo ou diretório tem uma função bem definida, o que facilita a identificação de onde implementar novas funcionalidades ou corrigir problemas existentes.


# Como Usar este Projeto? Fluxo de Funcionamento e Regras de Negócio

Abaixo, veremos o funcionamento completo da aplicação, bem como onde achar os materiais de apoio (API Collection e payloads de exemplo). Recomendo o uso do Postman para testar os endpoints da api, bem como o PyCharm como IDE para o projeto. Fiz o uso do Rancher para que o projeto fosse rodado em docker.

Assumindo que seguiu todos os passos do [QuickSetup](https://github.com/tauanyfeitosa/employee_management_api/blob/master/QuickSetup.md), você deve ter agora um projeto rodando e pronto para ser utilizado! Pois bem, vamos ao fluxo de funcionamento!
O projeto foi desenvolvido para ser um sistema para que empresas possam gerenciar seus funcionários. No entanto, pensando neste ponto, é comum pensarmos que há uma empresa acima das demais, que além de poder fazer uso do sistema para gerenciar seus próprios funcionários, também é responsável por gerenciar as empresas (mas sem acesso aos dados dos colaboradores que não sejam de sua empresa). Para deixar o DjangoAdmin livre de sobreposições (para ocasiões necessárias), o gerenciamento das empresas também é feito através de endpoints. E, embora tenha sido dito que não seria necessário um endpoint para criação de empresas (e de fato não seria), foi criado para que a própria empresa de gerenciamento pudesse ter sua interface fora do djangoAdmin.

## Create Company

A própria empresa que deseja entrar no sistema pode utilizar este endpoint para criar seu usuário, mas claro, com uma certa restrição! A model de Company é composta por um atributo chamado `is_approved` que iniciará como `False`  e impedirá a entrada de usuários não aprovados pelo administrador!
Mas, vamos para a criação de usuário!

Neste ponto, peço que baixe a collection que está localizada aqui, na raiz do projeto. Importe-a para o Postman e faça as verificações a seguir:

1. Procure pelo endpoint de `Create` na pasta `Company`

![image](https://github.com/user-attachments/assets/cf5874d1-d53b-402a-92e5-08650362c45c)

Você vai notar que já possui um payload preparado para você, basta mudar as informações conforme o necessário! Algumas validações importantes: CNPJ válido, senha conforme o padrão do django e todos os campos ali são obrigatórios!

2. Após criado, tente fazer login! Note que vc não conseguirá pois ainda não foi aprovado!
![image](https://github.com/user-attachments/assets/c2d012c1-8c5c-43cd-a89f-f4373f2da809)
![image](https://github.com/user-attachments/assets/446809a1-6f38-4eec-812a-536be78512c8)

Seu login depende tanto do is_activate quando do is_approved, ambos devem ser verdadeiros!

## Approve Company

Agora que temos um usuário diferente do createsuperuser (criado através do tutorial no [QuickSetup](https://github.com/tauanyfeitosa/employee_management_api/blob/master/QuickSetup.md)), vamos usar as credenciais do superuser para fazer login! Sobre os tokens para acesso, fique tranquilo! Você não precisará passar o token para cada endpoint toda vez, o processo foi automatizado. Peço que verifique na sua API Collection se está tudo certo com os scripts e autorizações antes de continuarmos com o endpoint!

- OLhe se o script abaixo está presente tanto no endpoint de Login quanto no de Refresh:
![image](https://github.com/user-attachments/assets/0bc63f4b-7ec6-406c-9c5d-1e98118bd617)
- Verifique se no endpoint de Approve, na aba de autorização, está setado da seguinte forma: 
![image](https://github.com/user-attachments/assets/05f31998-2726-475b-8bf2-bd5b55fb947f)

Caso não estejam configurados, basta adicionar e não precisará se preocupar mais em copiar e colar tokens ;) !

Agora, estamos prontos, basta informar na url o id da Empresa que deseja aprovar para entrar no sistema! Mas onde posso buscar o id? Utilize do endpoint `All Companies` e descubra o id, cnpj e outras informações importantes para buscas. Assim, poderá usar tranquilamente o endpoint de Approve.

![image](https://github.com/user-attachments/assets/a62ae835-7af1-4898-835d-ae7953c38ad2)

Depois de aprovado, note que seu login está liberado e pode enfim adicionar seus funcionários!

## Update Company

Se uma empresa acabou cadastrando algum dado errado, isso pode ser revertido pelo administrador. É claro que alguns dados não podem ser mudados, como o cnpj que já é validado pelo sistema na criação, logo, seria quase impossível que ele tivesse errado um ou dois números e fosse dado como válido. Não se preocupe em ter que atualizar a model inteira, todos os campos são opcionais e você pode atualizar apenas um se necessário. Mas, um ponto importante: você não pode mudar uma variável antes preenchida para uma string vazia. Caso mande sem querer com outros campos preenchidos, ela será ignorada, mas se for mandada sozinha, o sistema que retornaram uma mensagem de erro!

## Create Employee

Na sua API Collection também há um exemplo de payload que pode ser utilizada, mas atenção, existem muitas validações presentes nesse endpoint para assegurar a validade dos dados!

1. Seu funcionário não pode ter menos de 16 anos (trabalho infantil é crime, hein!)
2. Seu funcionário precisa ter um cpf que passe na validação de digitos verificadores
3. Você não pode adicionar uma data de contratação futura, apenas funcionários que trabalham atualmente para você podem ser cadastrados
4. Você não pode adicionar um funcionário (validamos isso pelo cpf) que esteja trabalhando em outra empresa (is_active = True no cadastro de outra empresa). Agora, se ele possui cadastro mas está inativo na outra empresa, pode ser adicionado normalmente!
5. Não pode haver duplicidade de email, um email está atrelado ao cpf de quem é cadastrado, logo, dois funcionários não podem possuir o mesmo email.
6. o email precisa estar em um formato válido
7. O número de celular do funcionário deve conter a quantidade válida de dígitos.

Seguindo essas validações, você conseguirá criar seu funcionário!

## Update Employees

A atualização das informações de um funcionário seguem o mesmo padrão do update de company!

## SoftDelete??

Como pedido nos próprios requisitos do projeto, o softdelete nada mais é que a inativação de um funcionário de uma empresa ou da propria empresa pelo superuser, desse modo, fazemos uma deleção que mantém seus dados. Para esta deleção, não é necessário payload, apenas o id do referido a ser excluido.

## O que é Filtered?

O Filtered (tanto para company quanto para employee) é um get all bem mais flexível, aceitando filtros em sua url (e com filtro, é realmente qualquer filtro). Em relação a funcionários, já informamos que não há como ter acesso a funcionários de outras empresas, então o filtro vai se restringir aos seus contratados, mas, seja criativo! use desde o is_active até um cpf ou cnpj, junte filtros em uma unica url e foque ainda mais sua busca, é justamente para isso que ele é útil!

## Get by Id

Notou que os endpoints acima mal mostram as informações dos modelos? Esse detalhamento ficou a cargo do get by is, assim poluimos menos a resposta e temos informações importantes apenas dos objetos de nosso interesse.

# E aí, rodou?

Com todos os endpoints apresentados, espero que tenha se divertido testando esta aplicação! Qualquer dúvida, contribuição ou feedback, pode entrar em contato comigo! Meus contatos estão logo abaixo ;)


# Autores

|<a href="https://www.linkedin.com/in/tauanyfeitosa/" target="_blank">**Tauany Feitosa**</a> | 
|:-----------------------------------------------------------------------------------------:|
| <a href="https://github.com/tauanyfeitosa" target="_blank">`github.com/tauanyfeitosa`</a>
|<a href="mailto:tauanysanttos13@gmail.com"><img src="https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=red" target="_blank"></a>     |





