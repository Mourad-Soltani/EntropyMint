# EntropyMint

Offline high-entropy secret minter. Generate cryptographically strong passwords, passphrases, and API keys with detailed entropy analysis. Pure Python stdlib — no dependencies, fully offline.

**Built by Mourad.Soltani**

## Features

- Mint passwords, Diceware-style passphrases, or API keys
- Shannon entropy calculation and strength labeling
- JSON output for scripting and automation
- Analyze existing secrets
- Zero dependencies (Python 3.8+)
- Health check endpoint for CI

## Quick Start

```bash
python3 entropymint.py health
python3 entropymint.py mint --mode password --length 24
python3 entropymint.py mint --mode passphrase --words 6 --json
python3 entropymint.py analyze "MySecret123!" --json
```

## Requirements

- Python 3.8 or newer
- No external packages

## License

MIT — see LICENSE
