
from request_builder.serialize_psbt_tx import serialize

def construct_request(vault_id, raw_psbt_bytes):
    
    data = serialize(raw_psbt_bytes)
    pstx = data["data"]
    print(f"Partially signed transaction -> {pstx[:8]}...{pstx[-8:]}")

    print(f'Preparing transaction from Vault {vault_id}')

    # Simple transfer
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