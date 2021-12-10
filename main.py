import asyncio
import config
import funcs

from config import Commands

async def handle_echo(reader, writer):
    data = await reader.readuntil(config.SEPARATOR.encode(config.ENCODING))
    
    message_as_string = data.decode()
    message = funcs.parse_raw_message(data.decode())
    addr = writer.get_extra_info('peername')
    
    print(f"Received {message_as_string!r} from {addr!r}")

    check_message = funcs.check_message(message)    
    if check_message:  
        response_from_checkserver = await funcs.send_to_checkserver(message_as_string)
        parsed_checkserver_response = funcs.parse_raw_message(response_from_checkserver.decode()) 
        check_checkserver_responce = funcs.check_message(parsed_checkserver_response)
        if check_checkserver_responce:
            # обращаемся к данным
            #writer.write(config.you_can.encode(config.ENCODING))
            if message['request_verb'] == Commands.insert: await funcs.insert_data(message)
            if message['request_verb'] == Commands.get: await funcs.get_data(message)
            if message['request_verb'] == Commands.delete: await funcs.delete_data(message)
            
        else:
            # 
            writer.write("Ошибка".encode(config.ENCODING))
            
    else:
        writer.write((config.not_understand_response + " " + config.PROTOCOL).encode())
    

    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_echo, config.HOST, config.PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())