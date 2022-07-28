# distributed-systems-discipline

# Trabalho 1 - Sistemas Distribuídos
Implementação de um chat que utiliza a arquitetura *publish-subscribe*, fazendo com que todos os usuários(inscritos) em um dado canal, recebam as mensagem(eventos) enviadas para o publicador(canal)

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
