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
FORDEFI_BTC_VAULT_TAPROOT_ADDRESS = os.getenv("FORDEFI_BTC_VAULT_TAPROOT_ADDRESS")
PATH = "/api/v1/transactions"

def main():

    if not FORDEFI_API_USER_TOKEN:
        print("Error: FORDEFI_API_TOKEN environment variable is not set")
        return
    
    # Process raw PSBT data
    psbt_data = "0x70736274...."
    # remove the leading "0x" if present
    if psbt_data.startswith("0x"):
        psbt_data = psbt_data[2:]

    # decode to raw bytes
    raw_psbt_bytes = bytes.fromhex(psbt_data)
    request_json = construct_request(FORDEFI_BTC_VAULT_ID, FORDEFI_BTC_VAULT_TAPROOT_ADDRESS, raw_psbt_bytes)

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