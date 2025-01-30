def serialize(psbt_bytes):
    """
    Takes raw PSBT bytes and returns a JSON dict
    with the field 'data' set to '0x' + hex string.
    """
    # Convert the raw PSBT bytes to a hex string
    psbt_hex = psbt_bytes.hex()
    
    # Add '0x' to avoid error with the Fordefi API
    psbt_hex_prefixed = "0x" + psbt_hex

    json_data = {"data": psbt_hex_prefixed}
    print(json_data)

    return json_data