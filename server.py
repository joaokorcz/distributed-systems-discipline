import socket, threading
from Connection import Connection

# Os dois clientes precisam estar na mesma porta para se comunicarem
LISTENING_PORT = 3434

users = {}
topics = {}

def handleUserConnection(connection, address):
    while True:
        try:
            msg = connection.socket.recv(1024)
   
            if msg:
                if b' ' in msg:
                    command, content = msg.split(b' ', 1)

                    ## Se a intenção for colocar um nick
                    if command == b'NICK':
                        ## Se o cliente já possuir nick, impede
                        if connection.name != None:
                            connection.socket.send(b'Voce ja tem nick')
                        
                        ## Caso contrário (não possui nick)
                        else:
                            name = content.lower()

                            ## Se o nick já existir no servidor, impede
                            if name.lower() in users:
                                connection.socket.send(b'Nick ja existe')
                            ## Caso contrário (nick não existe ainda), adiciona o nome
                            else:
                                connection.name = name
                                users[name] = connection
                    
                    # Se inscrive/cria um canal com um nome
                    elif command == b'INSTOPIC':
                        topic = content.lower()
                        
                        if topic not in topics:
                            topics[topic] = [connection.name]
                            connection.topics.append(topic)
                            connection.socket.send(b'Seus topicos: ' + decodeTopics(connection.topics))
                            
                        else:
                            # Caso o nome já esteja cadastrado no tópico, impede
                            if connection.name in topics[topic]:
                                connection.socket.send(b'Nick ja existente no topico')
                                
                            # Caso o nome não esteja cadastrado no tópico, inscreve
                            else:
                                topics[topic].append(connection.name)
                                connection.topics.append(topic)
                                connection.socket.send(b'Seus topicos: ' + decodeTopics(connection.topics))
                    
                    # Envia mensagem para um canal 
                    elif command == b'MSGTOPIC':
                        if len(content.split(b' ', 1)) != 2:
                            connection.socket.send(b'Formato invalido')
                        else: 
                            topic, msg = content.split(b' ', 1)
                            topic = topic.lower()
                            
                            # Se o tópico não existe, envia mensagem de erro
                            if topic not in topics:
                                connection.socket.send(b'Topico inexistente')
                            
                            else:
                                found_topic = topics[topic]
                                # Caso a conexão exista, mas o usuário não esteja cadastrado, envia mensagem de erro
                                if connection.name not in found_topic:
                                    connection.socket.send(b'Inscricao no topico nao encontrada')
                                # Caso esteja tudo certo, envia mensagem para todos os usuários inscritos no canal
                                else:
                                    for client in found_topic:
                                        if client != connection.name:
                                            users[client].socket.send(topic + b' - ' + connection.name + b': ' + msg)

                    # Lista todos os usuários inscritos em um dado canal
                    elif command == b'LIST':
                        topic = content

                        if topic not in topics:
                            connection.socket.send(b'Topico inexistente')
                        else:
                            found_topic = topics[topic]
                            if connection.name not in found_topic:
                                connection.socket.send(b'Inscricao no topico nao encontrada')
                            else:
                                for name in found_topic:
                                    connection.socket.send(name + b'\n')

                # Lista os canais que o usuário está cadastrado
                elif msg == b'MYTOPICS':
                    connection.socket.send(b'Seus topicos: ' + decodeTopics(connection.topics))
    
                # Desinscreve o usuários de todos os canais em que ele está inscrito
                elif msg == b'QUIT':
                    removeConnection(connection.name)
                    break

            else:
                removeConnection(connection.name)
                break

        except Exception as e:
            print(f'Erro na conexão: {e}')
            removeConnection(connection.name)
            break

def decodeTopics(topics):
    decoded_topics = ''
    for index, topic in enumerate(topics):
        decoded_topics += topic.decode()
        if index != len(topics) - 1:
            decoded_topics += ', '
    return decoded_topics.encode()

def removeConnection(name):
    if name in users:
        connection = users[name]
        connection.socket.close()
        del users[name]
        for topic in connection.topics:
            print(topic, name)
            topics[topic].remove(name)

def server():    
    try:
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('0.0.0.0', LISTENING_PORT))
        socket_instance.listen(4)

        print('Servidor ON!')
        
        while True:
            socket_connection, address = socket_instance.accept()

            connection = Connection(socket_connection, address)
            
            threading.Thread(target=handleUserConnection, args=[connection, address]).start()

    except Exception as e:
        print(f'Erro ao instanciar socket: {e}')

    finally:
        if len(users) > 0:
            for name in users:
                removeConnection(name)

        socket_instance.close()

if __name__ == "__main__":
    server()
