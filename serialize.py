def main():

    with open("./partially_signed_tx/tx.psbt", "rb") as f:
        psbt_bytes = f.read()

    # Convert the raw PSBT bytes to hex
    psbt_hex = psbt_bytes.hex()

    # Add 0x for the API:
    psbt_hex_prefixed = "0x" + psbt_hex

    print(psbt_hex_prefixed)


if __name__ == "__main__":
    main()
