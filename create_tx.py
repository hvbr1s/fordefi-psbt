import os
import datetime
import json
import requests
from dotenv import load_dotenv
from api_requests.push_to_api import make_api_request
from request_builder.construct_request import construct_request
from signing.signer import sign

load_dotenv()
FORDEFI_API_USER_TOKEN = os.getenv("FORDEFI_API_USER_TOKEN")
FORDEFI_BTC_VAULT_ID = os.getenv("FORDEFI_BTC_VAULT_ID")
PATH = "/api/v1/transactions"

def main():

    if not FORDEFI_API_USER_TOKEN:
        print("Error: FORDEFI_API_TOKEN environment variable is not set")
        return
    
    # Process raw PSBT data
    psbt_hex_string = "0x70736274ff0100fd210102000000035ee8d5074d3048f08d3049f2427ecd2b6d901b4c4803e088d473067bf9d6cc870000000000ffffffffca09004c61ecf4f887297b1f2534c1c10f269aa1225efb7ace76509be0a0359c0000000000ffffffff940be7a6defc254e1267efac11ab07fa49a4d16ffa3a16172631440b039bec180100000000ffffffff05220200000000000016001409d54197cd32c04a9d42fd91ccc3fe5d436030d62202000000000000160014fb447b8b16c9e9942fb194335246a868129bbf2a2202000000000000160014c6b1b5e55035a6e8401f96baf772da8e4cd05d0a9d42000000000000160014c6b1b5e55035a6e8401f96baf772da8e4cd05d0a0000000000000000176a5d14160200daa0348a05b886d302000000c08db70101000000000001012b102700000000000022512021e6eb46e8890ea103c84cb02633e3d81d05ad28aca8fd4ee8418f7b05d393b30001012b10270000000000002251207815defe511e97e09f5f81d31e782207b4060aa211e60e1ace7b9986f584faf80001011f2202000000000000160014c6b1b5e55035a6e8401f96baf772da8e4cd05d0a2202023269ff874a3c4575cafe68d65ae313b999af5b4c2f937b1db46cb43bb6cf18e2483045022100ef7b5817827a5e54cf82a0885991fda930b5f17aa616898c74fdb83673459d790220586194a0cd46d4e5a68744a2fa17c55623b3b4dfa77beef5180fe0aea56e7ede01000000000000"
    # remove the leading "0x" if present
    if psbt_hex_string.startswith("0x"):
        psbt_hex_string = psbt_hex_string[2:]

    # decode to raw bytes
    raw_psbt_bytes = bytes.fromhex(psbt_hex_string)
    request_json = construct_request(FORDEFI_BTC_VAULT_ID, raw_psbt_bytes)

    request_body = json.dumps(request_json)
    timestamp = datetime.datetime.now().strftime("%s")
    payload = f"{PATH}|{timestamp}|{request_body}"
        
    signature = sign(payload=payload)

    try: 
        method = "post"   
        resp_tx = make_api_request(PATH, FORDEFI_API_USER_TOKEN, signature, timestamp, request_body, method=method)
        resp_tx.raise_for_status()
        return resp_tx
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP error occurred: {str(e)}"
        if resp_tx.text:
            try:
                error_detail = resp_tx.json()
                error_message += f"\nError details: {error_detail}"
            except json.JSONDecodeError:
                error_message += f"\nRaw response: {resp_tx.text}"
        raise RuntimeError(error_message)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Network error occurred: {str(e)}")

    except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()