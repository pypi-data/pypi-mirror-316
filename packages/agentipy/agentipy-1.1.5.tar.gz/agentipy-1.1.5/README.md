# Solana Agent Kit

A powerful toolkit for interacting with the Solana blockchain, providing easy-to-use functions for token operations, and trading. Now integrated with LangChain for enhanced functionality.

## Features

- 🪙 Token Operations

  - Deploy new SPL tokens
  - Transfer SOL and SPL tokens
  - Check token balances
  - Stake SOL

- 💱 Trading

  - Integrated Jupiter Exchange support
  - Token swaps with customizable slippage
  - Direct routing options

- 🏦 Yield Farming

  - Lend idle assets to earn interest with Lulo

- 🔗 LangChain Integration
  - Utilize LangChain tools for enhanced blockchain interactions
  - Access a suite of tools for balance checks, transfers, token deployments, and more

## Installation

```bash
pip install agentipy
```

## Quick Start

```python
from solana_agent_kit import SolanaAgentKit, create_solana_tools

# Initialize with private key and optional RPC URL
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

# Create LangChain tools
tools = create_solana_tools(agent)
```

## Usage Examples

### Deploy a New Token

```python
from solana_agent_kit import deploy_token

result = deploy_token(
    agent,
    decimals=9,  # decimals
    initial_supply=1000000  # initial supply
)

print("Token Mint Address:", result["mint"].to_base58())
```

### Create NFT Collection

```python
from solana_agent_kit import deploy_collection

collection = deploy_collection(agent, {
    "name": "My NFT Collection",
    "uri": "https://arweave.net/metadata.json",
    "royalty_basis_points": 500,  # 5%
    "creators": [
        {
            "address": "creator-wallet-address",
            "percentage": 100,
        },
    ],
})
```

### Swap Tokens

```python
from solana_agent_kit import trade
from solana.publickey import PublicKey

signature = trade(
    agent,
    output_mint=PublicKey("target-token-mint"),
    input_amount=100,  # amount
    input_mint=PublicKey("source-token-mint"),
    slippage_bps=300  # 3% slippage
)
```

### Lend Tokens

```python
from solana_agent_kit import lend_asset

signature = lend_asset(
    agent,
    amount=100  # amount
)
```

### Stake SOL

```python
from solana_agent_kit import stake_with_jup

signature = stake_with_jup(
    agent,
    amount=1  # amount in SOL
)
```

### Fetch Token Price

```python
from solana_agent_kit import fetch_price

price = fetch_price(
    agent,
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"  # Token mint address
)

print("Price in USDC:", price)
```

### Send an SPL Token Airdrop via ZK Compression

```python
from solana_agent_kit import send_compressed_airdrop, get_airdrop_cost_estimate
from solana.publickey import PublicKey

print(
    "~Airdrop cost estimate:",
    get_airdrop_cost_estimate(
        recipients=1000,  # recipients
        priority_fee_in_lamports=30000  # priority fee in lamports
    )
)

signature = send_compressed_airdrop(
    agent,
    mint_address=PublicKey("JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"),  # mint
    amount_per_recipient=42,  # amount per recipient
    recipients=[
        PublicKey("1nc1nerator11111111111111111111111111111111"),
        # ... add more recipients
    ],
    priority_fee_in_lamports=30000  # priority fee in lamports
)
```

## API Reference

### Core Functions

#### `deploy_token(agent, decimals?, name, uri, symbol, initial_supply?)`

Deploy a new SPL token with optional initial supply. If not specified, decimals default to 9.

#### `deploy_collection(agent, options)`

Create a new NFT collection with customizable metadata and royalties.

#### `mint_collection_nft(agent, collection_mint, metadata, recipient?)`

Mint a new NFT as part of an existing collection.

#### `transfer(agent, to, amount, mint?)`

Transfer SOL or SPL tokens to a recipient.

#### `trade(agent, output_mint, input_amount, input_mint?, slippage_bps?)`

Swap tokens using Jupiter Exchange integration.

#### `get_balance(agent, token_address)`

Check SOL or token balance for the agent's wallet.

#### `lend_asset(agent, asset_mint, amount)`

Lend idle assets to earn interest with Lulo.

#### `stake_with_jup(agent, amount)`

Stake SOL with Jupiter to earn rewards.

#### `send_compressed_airdrop(agent, mint_address, amount, recipients, priority_fee_in_lamports?, should_log?)`

Send an SPL token airdrop to many recipients at low cost via ZK Compression.

## Dependencies

The toolkit relies on several key Solana and Metaplex libraries:

- solana-py
- spl-token-py
- metaplex-foundation
- lightprotocol

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

ISC License

## Security

This toolkit handles private keys and transactions. Always ensure you're using it in a secure environment and never share your private keys.
