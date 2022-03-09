# PROJETO COM AWS SNS E AWS LAMBDA

#### A idéia inicial desse pequeno e simples projeto seria para um ambiente real onde possuo uma máquina do jenkins que tem um Jenkinsfile que roda um JOB de testes. Porém esse JOB roda em uma outra máquina EC2 que é utilizada apenas para esses testes periódicos. 
#### O que queremos resolver aqui é a seguinte situação: Essa máquina que roda os testes fica ligada 24/7, ou seja a todo momento. Com isso ela utiliza recursos e acarreta custos de forma desnecessária, pois ela fica em funcionamento 24/7 para ser usada periódicamente em alguns momento do dia. Por tanto vou apresentar uma solução dentra várias possíveis, utilizando serviços da AwS, como SNS e LAMBDA. 

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

