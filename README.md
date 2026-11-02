# KROMT RPC Health Checker

**Latency and health probe for public JSON-RPC endpoints.**

Part of the public tooling suite for [KROMT](https://kromt.xyz).

- Website: https://kromt.xyz  
- GitHub: https://github.com/kromtxyz  

---

## What it does

Quickly checks whether common public RPCs (and any extra ones you supply) are reachable and how fast they respond.

- Measures round-trip latency for `eth_blockNumber`
- Reports latest block number when healthy
- Includes Robinhood Chain + major L2s by default

Useful before relying on a public endpoint for trading or agent operations.

## Requirements

- Python 3.9+
- `requests`, `click`, `rich`

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Check built-in public endpoints
python kromt_rpccheck.py

# Add your own RPCs
python kromt_rpccheck.py --rpc https://my.public.rpc --rpc https://another.rpc

# Only custom RPCs
python kromt_rpccheck.py --no-defaults --rpc https://...
```

## Security Notes

- Only sends a simple `eth_blockNumber` request.
- No private keys, no accounts, no credentials.
- Safe to run frequently.

## License

MIT — see [LICENSE](LICENSE)

---

**KROMT** · Non-custodial AI trading agent  
https://kromt.xyz · https://github.com/kromtxyz
