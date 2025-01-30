
from request_builder.serialize_psbt_tx import serialize

def construct_request(vault_id, taproot_address, raw_psbt_bytes):
    
    data = serialize(raw_psbt_bytes)
    pstx = data["data"]
    print(f"Partially signed transaction -> {pstx[:12]}...{pstx[-12:]}")

    print(f'Preparing transaction from Vault {vault_id}')

    request_json = {
            "vault_id": vault_id,
            "note": "string",
            "signer_type": "api_signer",
            "sign_mode": "auto",
            "type": "utxo_transaction",
            "details": {
                "type": "utxo_partially_signed_bitcoin_transaction",
                "psbt_raw_data": pstx,
                "auto_finalize": True,
                "sender": { # The address that will sign the inputs
                    "address": taproot_address, # Must be from a Fordefi Vault
                    "address_type": "taproot", # Must be Taproot
                    "chain": {
                        "chain_type": "utxo",
                        "unique_id": "bitcoin_mainnet"
                    },
                },
                "inputs": [ # OPTIONAL array describing how each input will be signed
                    {
                        "index": 0,
                        "signer_identity":{
                            "type": "address",
                            "address": taproot_address
                        }
                    }
                    # OPTIONAL -> add more inputs here as needed
                ],
                "push_mode": "auto"
            }
    }
    return request_json