# distributed-systems-discipline

# Trabalho 1 - Sistemas Distribuídos

- Nome: João Otavio Martini Korczovei, RA: 790913
- Nome: Mateus Grota Nishimura Ferro, RA: 771043

Implementação de um chat que utiliza a arquitetura *publish-subscribe*, fazendo com que todos os usuários(inscritos) em um dado canal, recebam as mensagem(eventos) enviadas para o publicador(canal). Para o trabalho foi utilizado o RabbitMQ.

Foi implementado duas classes para a representação das lojas e fábricas, sendo que em cada classe é estabelecida a conexão com a sua respectiva queue, no caso das fábricas com a queue 'fabrica' e no caso das lojas com a queue 'reposicao'. A queue 'reposicao' é entre as lojas e o centro de distribuição, enviando mensagens para o centro de distribuição quando certos itens da loja entram no farol vermelho. Ao enviar a mensagem para o centro de distribuição, o centro de distribuição irá notificar a fábrica que fabrica aquele produto para requisitar o produto, caso o centro de distribuição não tenha o produto no estoque.

## Comandos

Comando para rodar o servidor:

    python3 server.py
Comando para rodar o cliente:

    python3 client.py

## Comandos para o chat
- **NICK** (*nome*): define nome do usuário dentro do client.py .
- **INSTOPIC** (*nome do canal*): cria um canal e junta-se a ele automaticamente.
- **MSGTOPIC** (*nome do canal*) (*mensagem*): envia uma mensagem para o canal especificado.
- **LIST** (*nome do canal*): lista todos os usuários que estão no canal especificado.
- **MYTOPICS**: lista todos os canais em que o usuário está inscrito.
- **QUIT**: usuário sai de todos os canais cadastrados.
