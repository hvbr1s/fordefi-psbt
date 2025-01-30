def serialize(psbt_bytes):
    """
    Takes raw PSBT bytes and returns a JSON dict
    with the field 'data' set to '0x' + hex string.
    Ensures the PSBT starts with the magic bytes '70736274ff'
    """
    # Check if the data already starts with PSBT magic bytes
    psbt_hex = psbt_bytes.hex()
    psbt_magic = "70736274ff"
    
    # If the data doesn't start with PSBT magic bytes, add them
    if not psbt_hex.startswith(psbt_magic):
        psbt_hex = psbt_magic + psbt_hex
    
    # Add '0x' prefix for Fordefi API
    psbt_hex_prefixed = "0x" + psbt_hex

    json_data = {"data": psbt_hex_prefixed}
    print(f"Serialized PSBT: {json_data}")

    return json_data