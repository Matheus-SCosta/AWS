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
 _____________                       ___________                        ____________                          _____________
|             |                     |           |                      |            |                        |             |
|             |   publish message   |           | activate the trigger |            | starting/stopping EC2  |             |
| EC2 JENKINS | ------------------> |  AWS SNS  | -------------------> | AWS LAMBDA | ---------------------> |  EC2 TESTE  |
|             |                     |           |                      |            |                        |             |  
|_____________|                     |___________|                      |____________|                        |_____________|
```

A idéa do projeto é fazer com que a EC2 JENKINS consiga publicar uma mensagem em um tópico SNS, que por sua vez será um gatilho para uma função LAMBDA que será responsável por rodar uma aplicação Python que irá ligar e desligar a EC2 TESTE.



## CONFIGURAÇÃO

#### CRIAÇÃO TÓPICO SNS:
Pressumindo que já temos uma conta AWS criada e com um usuário criado com permissões suficientes para conseguirmos realizar a criação de recursos. Vamos criar um tópico no AWS SNS para que seja possível publicar mensagens de notificação. Para criar um tópico basta seguir a documentação https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html#step-create-queue ou então basta selecionar as seguinte opções: 
Fazer login no console do Amazon SNS => No painel de navegação esquerdo, escolha Tópicos => Na página Tópicos , escolha Criar tópico => Por padrão, o console cria um tópico FIFO. Escolha Padrão => Na seção Detalhes, insira um Nome para o tópico => Role até o final do formulário e escolha Criar tópico.
A partir de agora já conseguimos publicar mensagens nesse tópico para o a nossa função LAMBDA receba as notificações.

#### CRIAÇÃO FUNÇÃO LAMBDA:
Para criar uma função LAMBDA basta seguir a documentação https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html ou então seguir os passos: Abra a página Funções do console Lambda => Escolha Criar função => Em Informações básicas, faça o seguinte => Para Nome da função, insira my-function => Para Runtime, confirme se Node.js 14.x está selecionado. Observe que o Lambda fornece tempos de execução para .NET (PowerShell, C#), Go, Java, Node.js, Python e Ruby, porém para o nosso caso vamos utilizar Pyhton => Escolha Criar função.
A partir do momento que temos a função LAMBDA e o tópico SNS criados, é necessário adicionar o tópico SNS como gatilho para a função LAMBDA. Para isso no console lambda, clique na função criada e vá em **adicionar gatilhos**, selecione **SNS** e o tópico SNS criado. A partir desse momento, qualquer mensagem publicada nesse tópico chegará na função LAMBDA e servirá como gatilho.

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


#### CRIAÇÃO POLICIES E ROLE IAM PARA A EC2 DO JENKINS: 

É necessário também a criação de uma role IAM para a máquina do Jenkins conseguir dá comandos da EC2 de testes. Para isso também pode-se usar um usuário de serviço que tenha **access_key_id** e **secret_access_key**, mas optei por criar uma role. Para a criação da Role, você pode criar uma role com alguma policie para ter acesso full a EC2. Para criar uma role vá no console do IAM => ROLES => CREATE ROLE. Após a criação da ROLE foi necessário attacha-la na máquina do Jenkins.


#### FUNCIONAMENTO:

Agora já com tudo configurado, vou explicar como será o funcionamento do processo.

* Primeiramente vamos supor que já existem 3 imagens docker criadas, 2 serão do nosso projeto, sendo 1 será para desligar a máquina de testes e a outra para ligar. (Os arquivos de build do docker se encontram nesse repositório) e a 3º imagem é a imagem já usada para a realização de testes (imagem fora do escorpo desse projeto).
*  Partindo do principio que a EC2 TESTE está desligada o Jenkinsfile (EC2 JENKINS) irá criar 3 containers, o primeiro container será o de start da EC2 TESTE (que terá nossa imagem da pasta "start_valida"). Esse container será responsável por rodar um script python, que terá o seguinte conteúdo:

```
import boto3
import os
import random
sns = boto3.resource('sns', region_name='us-east-2')
topic_arn = sns.PlatformEndpoint('arn:aws:sns:us-east-2:398963803929:Start_Valida')



def publish_message(topic_arn, message): 
    response = topic_arn.publish(Message=message)
    message_id = response['MessageId']
    print(response, message_id)

if __name__ == "__main__":
    publish_message(topic_arn, "Starting Server Valida")
```
Esse script irá publicar a mensagem "Starting Server Valida" no tópico SNS Start_Valida.


*  Essa mensagem publicada será o gatilho para a função LAMBDA, cujo irá rodar uma aplicação em python, que terá o seguinte cõdigo:

```
from __future__ import print_function
import json
print('Loading function')
import boto3
import os
import sys

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print(event)
    print(context)
    message = event['Records'][0]['Sns']['Message']
    if message == "Stopping Server Valida":
        print("Stopping Server Valida")
        stop_ec2(instances = ['i-032398d6054a962e1'])
    elif message == 'Starting Server Valida':
        print("Starting Server Valida")
        start_ec2(instances = ['i-032398d6054a962e1'])
    else:
        print("Invalid message")
        sys.exit()
    return message
    
    
def start_ec2(instances):
    print(f"Instance Starting {instances}")
    ec2 = boto3.client('ec2', region_name='us-east-2')
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))


def stop_ec2(instances):
    print(f"Instance Stopping {instances}")
    ec2 = boto3.client('ec2', region_name='us-east-2')
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
    
```

Essa aplicação será responsável por verificar qual a mensagem que foi publicada, Nesse caso foi publicada a mensagem 'Starting Server Valida', então dessa forma irá executar a função start_ec2, que irá ligar a EC2_TESTE i-032398d6054a962e1.

*  O segundo container será o container que vai realizar os testes (essa imagem já existe). Esse container irá executar todos os testes que precisam ser feitos.
*  O terceiro container será o container responsável por dá o stop na EC2 TESTE. (que terá nossa imagem da pasta "stop_valida"). Esse container será responsável por rodar um script python, que terá o seguinte conteúdo:


```
import boto3
import os
import random

sns = boto3.resource('sns', region_name='us-east-2')
topic_arn = sns.PlatformEndpoint('arn:aws:sns:us-east-2:398963803929:Stop_valida')


def test_app():
    while True:
        number = random.randint(0, 10)
        if number == 0:
            print('Build Sucess')
            publish_message(topic_arn, "Stopping Server Valida")
            break
        print('Build Failed')
        os.system("sleep 30")


def publish_message(topic_arn, message): 
    response = topic_arn.publish(Message=message)
    message_id = response['MessageId']
    print(response, message_id)


if __name__ == "__main__":
    test_app()
```

Esse script irá publicar uma mensagem 'Stopping Server Valida' para o tópico Stop_valida.

*  Essa mensagem publicada será um novo gatilho para a função LAMBDA, cujo dessa vez verificará que a mensagem é diferente 'Stopping Server Valida', e vai executar a função stop_ec2, desligando a ec2.
