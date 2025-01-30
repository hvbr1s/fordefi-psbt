def serialize():

    with open("./partially_signed_tx/tx.psbt", "rb") as f:
        psbt_bytes = f.read()

    # Convert the raw PSBT bytes to hex
    psbt_hex = psbt_bytes.hex()

    # Add 0x for the API:
    psbt_hex_prefixed = "0x" + psbt_hex

    json_data = {"data": psbt_hex_prefixed}

    return json_data
