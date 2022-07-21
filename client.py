import socket, threading

SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 3434

def handle_messages(connection):
    while True:
        try:
            msg = connection.recv(1024)

            if msg:
                print(msg.decode())
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Erro ao receber mensagem: {e}')
            connection.close()
            break

def client():
    try:
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        print('Conectado')

        while True:
            text = input()

            if text == 'sair':
                socket_instance.close()

            socket_instance.send(text.encode())

        socket_instance.close()

    except Exception as e:
        print(f'Erro na conexão {e}')
        socket_instance.close()

if __name__ == "__main__":
    client()