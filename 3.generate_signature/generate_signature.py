MESSAGE = ""
PRIVATE_KEY = ""
TOKEN = ""
def generate_signature(message,private_key):
    message_hash = encode_defunct(text=message)
    signed_message = Account.sign_message(message_hash, private_key)
    signature = signed_message.signature.hex()
    signature_id = f'0x{signature}'
    return signature_id

generate_signature(MESSAGE,PRIVATE_KEY)


