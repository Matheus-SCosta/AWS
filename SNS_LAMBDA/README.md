# PROJETO COM AWS SNS E AWS LAMBDA

#### A idéia inicial desse pequeno e simples projeto seria para um ambiente real onde possuo uma máquina do jenkins que tem um Jenkinsfile que roda um JOB de testes. Porém esse JOB roda em uma outra máquina EC2 que é utilizada apenas para esses testes periódicos. 
#### O que queremos resolver aqui é a seguinte situação: Essa máquina que roda os testes fica ligada 24/7, ou seja a todo momento. Com isso ela utiliza recursos e acarreta custos de forma desnecessária, pois ela fica em funcionamento 24/7 para ser usada periódicamente em alguns momento do dia. Por tanto vou apresentar uma solução dentra várias possíveis, utilizando serviços da AWS, como SNS e LAMBDA. 

#### Vale lembrar que os servidores do jenkins e da máquina de testes são EC2 e estão na mesma conta da AWS, durante a explicação será mencionado outros serviços da AWS, como IAM e também algumas ferramentas DevOps como Docker.


Bom, vou começar primeiramente explicando de forma introdutória alguns serviços, tais como:

#### AWS SNS:
O AWS SNS é um serviço de notificaçâo, onde encaminha notificações A2A (Aplication-to-Aplication) e A2P (Aplication-to-person).

#### AWS LAMBDA:
O AWS LAMBDA é um serviço Serveless fornecido pela Amazon. Nele é possível ter aplicações rodando sem possuir e gerenciar um servidor.

#### AWS IAM:
O AWS IAM é um serviço de gerenciamento de usuário e grupos. Nele é possível gerenciar permissões para usuários e serviços AWS.

#### AWS EC2:
O AWS EC2 são os servidores virtuais da Amazon.



## IDÉIA DO PROJETO
```
 _____________                    ___________                     ____________               
|             |                  |           |                   |            |
|             |                  |           |                   |            |   
| JENKINS EC2 |                  |  AWS SNS  |                   | AWS LAMBDA |
|             |                  |           |                   |            |
|_____________|                  |___________|                   |____________|
```





## CONFIGURAÇÃO

#### CRIAÇÃO TÓPICO SNS:
Pressumindo que já temos uma conta AWS criada e com um usuário criado com permissões suficientes para conseguirmos realizar a criação de recursos. Vamos criar um tópico no AWS SNS para que seja possível publicar mensagens de notificação. Para criar um tópico basta seguir a documentação https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html#step-create-queue ou então basta selecionar as seguinte opções: 
Fazer login no console do Amazon SNS => No painel de navegação esquerdo, escolha Tópicos => Na página Tópicos , escolha Criar tópico => Por padrão, o console cria um tópico FIFO. Escolha Padrão => Na seção Detalhes, insira um Nome para o tópico => Role até o final do formulário e escolha Criar tópico.
A partir de agora já conseguimos publicar mensagens nesse tópico para o a nossa função LAMBDA receba as notificações.

#### CRIAÇÃO FUNÇÃO LAMBDA:
Para criar uma função LAMBDA basta seguir a documentação https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html ou então seguir os passos: Abra a página Funções do console Lambda => Escolha Criar função => Em Informações básicas, faça o seguinte => Para Nome da função, insira my-function => Para Runtime, confirme se Node.js 14.x está selecionado. Observe que o Lambda fornece tempos de execução para .NET (PowerShell, C#), Go, Java, Node.js, Python e Ruby, porém para o nosso caso vamos utilizar Pyhton => Escolha Criar função.

#### CRIAÇÃO POLICIES E ROLE IAM PARA A FUNÇÃO LAMBDA:
Com a função lambda já criada precisamos criar uma role IAM para que o LAMBDA consiga ter permissão para dá comandos em recursos AWS. No nosso caso é necessário por exemplo permissão para ligar e desligar EC2, dentre outras. Geralmente ao criamos uma função LAMBDA vocẽ pode criar uma role com funções básicas para o lambda, caso essa role já exista seria necessário apenas criar uma policie e attachar na role já criada para a função LAMBDA. Então dessa forma vamos criar uma policie com permissão para ligar e desligar EC2 e para criar basta ir no console do IAM => POLICIES => CREATE POLICIES e colocar o json abaixo e criar a policie.   

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Start*",
                "ec2:Stop*"
            ],
            "Resource": "*"
        }
    ]
}
```

Ao concluir a criação da policie attach a role usada pela função LAMBDA.


#### CRIAÇÃO POLICIES E ROLE IAM PARA A EC2 DO JENKINS 

É necessário também a criação de uma role IAM para a máquina do Jenkins conseguir dá comandos da EC2 de testes. Para isso também pode-se usar um usuário de serviço que tenha **access_key_id** e **secret_access_key**, mas optei por criar uma role. Para a criação da Role, você pode criar uma role com alguma policie para ter acesso full a EC2. Para criar uma role vá no console do IAM => ROLES => CREATE ROLE. Após a criação da ROLE foi necessário attacha-la na máquina do Jenkins.