import socket

import exceptions
from config import *


contact_dict = {'Иван Хмурый' : "89012345678 — мобильный 02 — рабочий"}

def parse_to_get_name(message:str) -> str:
    first_string = message.split("РКСОК/1.0\r\n")[0]
    name = ' '.join(first_string.split()[1:])
    return name

def get_response_from_checkserver(message) -> str:
    message_to_checkserver = may_i + ' ' + PROTOCOL + '\n' + message
    checkserver_client = socket.create_connection((CHECK_SERVER_HOST, CHECK_SERVER_PORT))
    checkserver_client.send(message_to_checkserver.encode(ENCODING))
    checkserver_response = checkserver_client.recv(1024)
    print(f"Response from checkserver:\n{checkserver_response.decode(ENCODING)}\n...")
    return(checkserver_response.decode(ENCODING))

def perform_request(conn, name, message):
    command = message.split()[0]
    if command == "ЗОПИШИ":
        number = ' '.join(message.split("РКСОК/1.0\r\n")[1].split())
        contact_dict[name] = number
        response_text = SUCCESS + ' ' + PROTOCOL
    elif command == "ОТДОВАЙ":
        number = contact_dict.get(name)
        if number:
            response_text = RKSOK_to_english["normal"] + "\r\n" + number
        else:
            response_text = RKSOK_to_english["not_found"]
    elif command == "УДОЛИ":
        if contact_dict.pop(name, None):
            response_text = RKSOK_to_english["normal"]
        else:
            response_text = RKSOK_to_english["not_found"]
    else:
        raise exceptions.NotUnderstandException
    conn.send(response_text.encode(ENCODING))

def run_server():
	with socket.create_server((HOST, PORT)) as server:
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.listen(10)
		while True:
			try:
				print(f"Server is ready to connect on host:{HOST} and port:{PORT}...")
				iteration = 0
				conn, addr = server.accept()
				while True:
					iteration += 1
					data = conn.recv(1024)
					if not data:
						print("close connection")
						conn.close()
						break
					request_message = data.decode()
					print(f"recieved from client:\n...\n{request_message}\n...")
					name = parse_to_get_name(request_message)
					command = request_message.split()[0]
					checkserver_response = get_response_from_checkserver(request_message)
					if checkserver_response == you_can + ' ' + PROTOCOL + SEPARATOR:
						perform_request(conn, name, request_message)
					else:
						conn.send(
							(cannot + ' ' + PROTOCOL + '\r\n' + checkserver_response)
							.encode(PROTOCOL)
							)
			except KeyboardInterrupt:
				break 

if __name__ == "__main__":
    run_server()
