import asyncio
import config


message = "ЗОПИШИ Иван Хмурый РКСОК/1.0\r\n89012345678 — мобильный\r\n02 — рабочий\r\n\r\n"

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        config.HOST, config.PORT)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.readuntil("\r\n\r\n".encode(config.ENCODING))
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

asyncio.run(tcp_echo_client(message))