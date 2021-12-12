import asyncio
import aiofiles
import config





def check_message(message: dict) -> str:
    '''Check parsed message (dict) on accordance by request_verb,
        protocol_name and lenght of name.
        Returns request_verb (str).'''
    if message["request_verb"] not in config.command_verbs\
        or message["protocol_name"] != config.PROTOCOL \
            or len(message['name']) > 30:\
        return None
    return message["request_verb"]

async def send_to_checkserver(message):
    reader, writer = await asyncio.open_connection(
            config.CHECK_SERVER_HOST, config.CHECK_SERVER_PORT)
        
    request_to_checkserver = config.may_i + " " + config.PROTOCOL + "\n" + message
    writer.write(request_to_checkserver.encode(config.ENCODING))
    await writer.drain()
    
    response_from_checkserver = await reader.readuntil(config.SEPARATOR.encode(config.ENCODING))
    
    writer.close()
    
    return response_from_checkserver

def parse_raw_message(message: str) -> dict:
    
    parsed_message = message.split("\r\n")
    
    first_string = parsed_message[0].split(' ')
    request_verb, name, protocol_name = first_string[0], (' ').join(first_string[1:-1]), first_string[-1]
    data = ' '.join([i for i in parsed_message[1:] if i != ""])

    parsed_message = {
        "request_verb" : request_verb,
        "name" : name,
        "protocol_name" : protocol_name,
        "data" : data
    }
    
    return parsed_message

async def get_data(message: dict) -> str:
    '''Get data from phonebook'''
    async with aiofiles.open(config.file_name, mode='r') as f:
        contents = await f.read()
        contents = contents.split("\n")
        for elem in contents:
            try:
                print(f"{elem=}, {message['name']=}")
                name, data = elem.split("|")[0], elem.split("|")[1]
                if name == message['name']:
                    return data
            except IndexError:
                pass
        return config.NO_DATA
        
async def insert_data(message: dict) -> None:
    '''Add new data to phonebook'''
    async with aiofiles.open(config.file_name, mode='a') as f:
        data = message['name'] + "|" + message['data'] + "\n"
        await f.writelines(data)

async def delete_data(message: dict) -> None:
    '''Delete data from phonebook'''
    async with aiofiles.open(config.file_name, mode='r') as f:
        contents = await f.read()
        contents = contents.split("\n")
    async with aiofiles.open(config.file_name, mode='w') as f:   
        for elem in contents:
            try:
                name = elem.split("|")[0]
                if name != message['name']:
                    data = elem + "\n"
                    await f.write(data)
            except IndexError:
                pass
        

