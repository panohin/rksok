import asyncio
import config



def check_message(message: dict):
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
    
