# PROJETO COM AMAZON SNS E AMAZON LAMBDA

#### A idéia inicial desse pequeno e simples projeto seria para um ambiente real onde possuo uma máquina do jenkins que tem um Jenkinsfile que roda um JOB de testes. Porém esse JOB roda em uma outra máquina EC2 que é utilizada apenas para esses testes periódicos. 
### O que queremos resolver aqui é a seguinte situação: Essa máquina que roda os testes fica ligada 24/7, ou seja a todo momento. Com isso ela utiliza recursos e acarreta custos de forma desnecessária, pois ela fica em funcionamento 24/7 para ser usada periódicamente em alguns momento do dia. Por tanto vou apresentar uma solução dentra várias possíveis, utilizando serviços da Amazon, como SNS e LAMBDA. 

#### Vale lembrar que os servidores do jenkins e da máquina de testes são EC2 e estão na mesma conta da AMAZON.