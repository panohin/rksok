import asyncio
import config
import funcs

async def handle_echo(reader, writer):
    data = await reader.readuntil(config.SEPARATOR.encode(config.ENCODING))
    
    message_as_string = data.decode()
    message = funcs.parse_raw_message(data.decode())
    addr = writer.get_extra_info('peername')
    
    print(f"Received {message_as_string!r} from {addr!r}")
    
    if funcs.check_message(message):
        response_from_checkserver = await funcs.send_to_checkserver(message_as_string)
        print(funcs.parse_raw_message(response_from_checkserver.decode())) 
                       
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