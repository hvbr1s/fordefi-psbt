# Fordefi PSBT Transaction Creator

A Python script for creating and submitting Bitcoin PSBT (Partially Signed Bitcoin Transaction) transactions to the Fordefi API.

## Prerequisites

- Python 3.x
- Fordefi BTC Vault with a Taproot address
- Fordefi API User Token and API Signer (setup instructions can be found [here](https://docs.fordefi.com/developers/program-overview))

## Setup

1. Install `uv` package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Set up the project and install dependencies:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   uv sync
   ```

3. Configure environment variables:
   Create a `.env` file in the root directory with the following:
   ```plaintext
   FORDEFI_API_USER_TOKEN="your_token"
   FORDEFI_BTC_VAULT_ID="your_vault_id"
   FORDEFI_BTC_VAULT_TAPROOT_ADDRESS="taproot_address_from_btc_vault"
   ```
4. Place your API Signer's `.pem` private key file in a `/secret` directory in the root folder.

5. Start the Fordefi API Signer:
   ```bash
   docker run --rm --log-driver local --mount source=vol,destination=/storage -it fordefi.jfrog.io/fordefi/api-signer:latest
   ```
   Then select "Run signer" in the Docker container.

## Usage

```bash
python create_tx.py
```

The script:
1. Processes raw PSBT data
2. Constructs an API request
3. Signs the payload with your Fordefi API Signer
4. Submits the transaction to Fordefi's API for processing onchain