# Solana Agent Kit

A powerful toolkit for interacting with the Solana blockchain, providing easy-to-use functions for token operations, and trading. Now integrated with LangChain for enhanced functionality.

## Features

- 🪙 Token Operations

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
from agentipy import SolanaAgentKit, create_solana_tools

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

### Fetch price of a token

```python
from agentipy import SolanaAgentKit

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

    # Get balance
    balance =  await agent.fetch_price("FKMKctiJnbZKL16pCmR7ig6bvjcMJffuUMjB97YD7LJs")
    print(f"Price: {balance} SOL")

# Run the async function
import asyncio
asyncio.run(main())

```

### Swap Tokens

```python
from agentipy import SolanaAgentKit

from solders.pubkey import Pubkey

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

signature = await agent.trade(
    agent,
    output_mint=Pubkey.from_string("target-token-mint"),
    input_amount=100,  # amount
    input_mint=Pubkey.from_string("source-token-mint"),
    slippage_bps=300  # 3% slippage
)

import asyncio
asyncio.run(main())
```

### Lend Tokens

```python
from agentipy import SolanaAgentKit

from solders.pubkey import Pubkey

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)
signature = await agent.lend_assets(
    amount=100  # amount
)

import asyncio
asyncio.run(main())
```

### Stake SOL

```python
from agentipy import SolanaAgentKit

from solders.pubkey import Pubkey

async def main():
agent = SolanaAgentKit(
    "your-wallet-private-key-as-base58",
    "https://api.mainnet-beta.solana.com",
    "your-openai-api-key"
)

signature = await agent.stake(
    amount=1  # amount in SOL
)

import asyncio
asyncio.run(main())
```

## API Reference

### Core Functions

#### `transfer(agent, to, amount, mint?)`

Transfer SOL or SPL tokens to a recipient.

#### `trade(agent, output_mint, input_amount, input_mint?, slippage_bps?)`

Swap tokens using Jupiter Exchange integration.

#### `get_balance(agent, token_address)`

Check SOL or token balance for the agent's wallet.

#### `lend_asset(agent, asset_mint, amount)`

Lend idle assets to earn interest with Lulo.

#### `stake(agent, amount)`

Stake SOL with Jupiter to earn rewards.

## Dependencies

The toolkit relies on several key Solana and Metaplex libraries:

- solana-py
- spl-token-py

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

ISC License

## Security

This toolkit handles private keys and transactions. Always ensure you're using it in a secure environment and never share your private keys.
