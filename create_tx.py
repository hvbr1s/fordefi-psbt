from email.headerregistry import Address
import os
import datetime
import json
import requests
from api_requests.broacast import broadcast_tx
from signing.signer import sign


with open("./serialized.json", "r") as f:
    data = json.load(f)
pstx = data["data"]
print(f"Partially signed transaction -> {pstx}")

# Simple transfer
request_json = {
        "vault_id": "56d51e5d-507b-4f3c-b0ac-bf0e3352fa67",
        "note": "string",
        "signer_type": "api_signer",
        "sign_mode": "triggered",
        "type": "utxo_transaction",
        "details": {
            "type": "utxo_partially_signed_bitcoin_transaction",
            "psbt_raw_data": pstx,
            "auto_finalize": True,
            "sender": {
                "address": "bc1pvustretgfqeuqmtfkjjymt93p3jlkwzzqk5j6j5ewdym9c8fwucshpt5kw",
                "address_type": "taproot",
                "chain": {
                    "chain_type": "utxo",
                    "unique_id": "bitcoin_mainnet"
                }
            },
            "inputs": [
                {
                    "index": 0,
                    "signer_identity": {
                        "type": "address",
                        "address": "bc1qv9hnve34the4933d6zphhqyt3j52sh39d8h88ea5reqj3m53vzaqpxcz3x"  
                    }
                }
            ],
            "push_mode": "auto"
        }
}

access_token = os.getenv("FORDEFI_API_TOKEN")
path = "/api/v1/transactions"
request_body = json.dumps(request_json)
timestamp = datetime.datetime.now().strftime("%s")
payload = f"{path}|{timestamp}|{request_body}"


def ping(path, access_token):

    signature = sign(payload=payload)

    try:    
        resp_tx = broadcast_tx(path, access_token, signature, timestamp, request_body)
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

def main():
    if not access_token:
        print("Error: FORDEFI_API_TOKEN environment variable is not set")
        return
        
    try:
        response = ping(path, access_token)
        print(json.dumps(response.json(), indent=2))
        data = response.json()

        # Save data to a JSON file (RECOMMENDED TO RUN ONCE TO HAVE A GOOD VIEW OF THE OBJECT RETURNED BY THE API)
        with open('response_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=2)
        print("Data has been saved to 'response_data.json'")

    except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()