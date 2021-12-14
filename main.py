import asyncio
from os import write
import config
import funcs

from config import Commands

'''
ПРОВЕРЬ ОТВЕТЫ, КОТОРЫЕ ПОЛУЧАЕТ ТЕСТОВЫЙ КЛИЕНТ
ОН ИХ НЕ МОЖЕТ ПОНЯТЬ!

'''

async def rksok_protocol(reader, writer):
    data = await reader.readuntil(config.SEPARATOR.encode(config.ENCODING))
    message_as_string = data.decode()
    message = funcs.parse_raw_message(message_as_string)
    addr = writer.get_extra_info('peername')
    print(f"Received {message_as_string!r} from {addr!r}")
      
    if funcs.check_message(message):  
        response_from_checkserver = await funcs.send_to_checkserver(message_as_string)
        parsed_checkserver_response = funcs.parse_raw_message(response_from_checkserver.decode()) 
        
        if parsed_checkserver_response['request_verb'] == config.you_can:
            try:
                if message['request_verb'] == Commands.insert:
                    await funcs.insert_data(message)
                    writer.write(f"{config.SUCCES} + ' ' + {config.PROTOCOL}".encode(config.ENCODING))
                if message['request_verb'] == Commands.get:
                    data = await funcs.get_data(message)
                    if data == config.NO_DATA:
                        responce = f"{config.NO_DATA} + ' ' + {config.PROTOCOL}"
                        writer.write(responce.encode(config.ENCODING))
                    else:
                        responce = f"{config.SUCCES} + ' ' + {config.PROTOCOL} + '\n' + {data}"
                        writer.write(responce.encode(config.ENCODING))
                if message['request_verb'] == Commands.delete:
                    result = await funcs.delete_data(message)
                    if result == config.NO_DATA:
                        responce = f"{config.NO_DATA} + ' ' + {config.PROTOCOL}"
                        writer.write(responce.encode(config.ENCODING))
                    else:
                        writer.write(f"{config.SUCCES} + ' ' + {config.PROTOCOL}".encode(config.ENCODING))
            except Exception as e:
                    print(e.message, e.args)         
        else:
           responce = f"{config.cannot} + ' ' + {config.PROTOCOL} + '\n' + {parsed_checkserver_response['data']}"
           writer.write(responce.encode(config.ENCODING))
            
    else:
        writer.write((config.not_understand_response + " " + config.PROTOCOL).encode())
    
    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        rksok_protocol, config.HOST, config.PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())