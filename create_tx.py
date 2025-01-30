import os
import datetime
import json
import requests
from api_requests.push_to_api import make_api_request
from request_builder.serialize_psbt_tx import serialize
from signing.signer import sign

def construct_request():
    
    data = serialize()
    pstx = data["data"]
    print(f"Partially signed transaction -> {pstx[:8]}...{pstx[-8:]}")

    # Simple transfer
    request_json = {
            "vault_id": "56d51e5d-507b-4f3c-b0ac-bf0e3352fa67",
            "note": "string",
            "signer_type": "api_signer",
            "sign_mode": "auto",
            "type": "utxo_transaction",
            "details": {
                "type": "utxo_partially_signed_bitcoin_transaction",
                "psbt_raw_data": pstx,
                "auto_finalize": True,
                "sender": { # The signing address
                    "address": "bc1pvustretgfqeuqmtfkjjymt93p3jlkwzzqk5j6j5ewdym9c8fwucshpt5kw", # Must be a Fordefi Vault
                    "address_type": "taproot", # Must be Taproot address
                    "chain": {
                        "chain_type": "utxo",
                        "unique_id": "bitcoin_mainnet"
                    },
                },
                "inputs": [ # OPTIONAL
                    {
                    "index": 0,
                    "signer_identity":{
                        "type": "address",
                        "address": "bc1pvustretgfqeuqmtfkjjymt93p3jlkwzzqk5j6j5ewdym9c8fwucshpt5kw"
                    }
                    }
                ],
                "push_mode": "auto"
            }
    }
    return request_json


FORDEFI_API_USER_TOKEN = os.getenv("FORDEFI_API_USER_TOKEN")
PATH = "/api/v1/transactions"

def main():

    if not FORDEFI_API_USER_TOKEN:
        print("Error: FORDEFI_API_TOKEN environment variable is not set")
        return
    
    request_json = construct_request()

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