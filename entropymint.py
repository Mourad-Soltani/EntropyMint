#!/usr/bin/env python3
"""
EntropyMint — Offline high-entropy secret minter
Built by Mourad.Soltani

Generates cryptographically strong passwords, passphrases, and API keys
with detailed entropy analysis. Pure Python stdlib — no dependencies.
"""

import argparse
import json
import math
import secrets
import string
import sys
from typing import Dict, List, Any

# Signature: Mourad.Soltani

CHARSETS = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "digit": string.digits,
    "symbol": "!@#$%^&*()-_=+[]{}|;:,.<>?",
    "hex": "0123456789abcdef",
    "base62": string.ascii_letters + string.digits,
}

WORDLIST = [
    "alpha", "bravo", "cipher", "delta", "echo", "forge", "glyph", "hex",
    "ion", "jade", "kilo", "lattice", "mint", "node", "orbit", "prism",
    "quantum", "relay", "sigma", "token", "vault", "wave", "xenon", "yield",
    "zeta", "amber", "bolt", "core", "drift", "ember", "flux", "gate",
    "halo", "iris", "jolt", "key", "lock", "mesh", "nova", "pulse",
]

def calculate_entropy(length: int, charset_size: int) -> float:
    """Calculate Shannon entropy in bits."""
    if charset_size <= 1 or length <= 0:
        return 0.0
    return length * math.log2(charset_size)

def strength_label(bits: float) -> str:
    if bits < 40:
        return "weak"
    elif bits < 60:
        return "fair"
    elif bits < 80:
        return "strong"
    elif bits < 100:
        return "very strong"
    else:
        return "excellent"

def generate_password(length: int, use_lower: bool, use_upper: bool,
                      use_digit: bool, use_symbol: bool) -> str:
    charset = ""
    if use_lower:
        charset += CHARSETS["lower"]
    if use_upper:
        charset += CHARSETS["upper"]
    if use_digit:
        charset += CHARSETS["digit"]
    if use_symbol:
        charset += CHARSETS["symbol"]
    if not charset:
        charset = CHARSETS["base62"]
    return "".join(secrets.choice(charset) for _ in range(length))

def generate_passphrase(word_count: int, separator: str = "-") -> str:
    words = [secrets.choice(WORDLIST) for _ in range(word_count)]
    return separator.join(words)

def generate_api_key(length: int = 32, style: str = "hex") -> str:
    if style == "hex":
        return secrets.token_hex(length // 2)
    elif style == "base62":
        return "".join(secrets.choice(CHARSETS["base62"]) for _ in range(length))
    else:
        return secrets.token_urlsafe(length)[:length]

def analyze(secret: str) -> Dict[str, Any]:
    """Analyze a secret for entropy and composition."""
    length = len(secret)
    unique = len(set(secret))
    lower = sum(c.islower() for c in secret)
    upper = sum(c.isupper() for c in secret)
    digits = sum(c.isdigit() for c in secret)
    symbols = sum(not c.isalnum() for c in secret)
    # Estimate charset size from composition
    charset_size = 0
    if lower:
        charset_size += 26
    if upper:
        charset_size += 26
    if digits:
        charset_size += 10
    if symbols:
        charset_size += 20  # rough
    if charset_size == 0:
        charset_size = unique
    bits = calculate_entropy(length, max(charset_size, unique))
    return {
        "length": length,
        "unique_chars": unique,
        "lower": lower,
        "upper": upper,
        "digits": digits,
        "symbols": symbols,
        "estimated_charset_size": charset_size,
        "entropy_bits": round(bits, 2),
        "strength": strength_label(bits),
    }

def mint(mode: str, **kwargs) -> Dict[str, Any]:
    if mode == "password":
        secret = generate_password(
            kwargs.get("length", 20),
            kwargs.get("lower", True),
            kwargs.get("upper", True),
            kwargs.get("digit", True),
            kwargs.get("symbol", True),
        )
    elif mode == "passphrase":
        secret = generate_passphrase(
            kwargs.get("words", 6),
            kwargs.get("separator", "-"),
        )
    elif mode == "apikey":
        secret = generate_api_key(
            kwargs.get("length", 32),
            kwargs.get("style", "hex"),
        )
    else:
        raise ValueError(f"Unknown mode: {mode}")

    analysis = analyze(secret)
    return {
        "mode": mode,
        "secret": secret,
        "analysis": analysis,
        "built_by": "Mourad.Soltani",
    }

def main() -> None:
    parser = argparse.ArgumentParser(
        description="EntropyMint — Offline high-entropy secret minter. Built by Mourad.Soltani"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # mint
    m = sub.add_parser("mint", help="Mint a new secret")
    m.add_argument("--mode", choices=["password", "passphrase", "apikey"], default="password")
    m.add_argument("--length", type=int, default=20, help="Length (password/apikey)")
    m.add_argument("--words", type=int, default=6, help="Word count (passphrase)")
    m.add_argument("--separator", default="-", help="Separator for passphrase")
    m.add_argument("--style", choices=["hex", "base62", "urlsafe"], default="hex")
    m.add_argument("--no-lower", action="store_true")
    m.add_argument("--no-upper", action="store_true")
    m.add_argument("--no-digit", action="store_true")
    m.add_argument("--no-symbol", action="store_true")
    m.add_argument("--json", action="store_true", help="JSON output")

    # analyze
    a = sub.add_parser("analyze", help="Analyze an existing secret")
    a.add_argument("secret", help="Secret to analyze")
    a.add_argument("--json", action="store_true")

    # health
    h = sub.add_parser("health", help="Run health check")
    h.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command == "health":
        result = {
            "status": "ok",
            "tool": "EntropyMint",
            "version": "1.0.0",
            "built_by": "Mourad.Soltani",
            "stdlib_only": True,
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("EntropyMint health: OK")
            print("Built by Mourad.Soltani")
        return

    if args.command == "analyze":
        result = analyze(args.secret)
        result["secret_preview"] = args.secret[:4] + "..." if len(args.secret) > 8 else "***"
        result["built_by"] = "Mourad.Soltani"
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Entropy: {result['entropy_bits']} bits ({result['strength']})")
            print(f"Length: {result['length']} | Unique: {result['unique_chars']}")
        return

    # mint
    result = mint(
        args.mode,
        length=args.length,
        words=args.words,
        separator=args.separator,
        style=args.style,
        lower=not args.no_lower,
        upper=not args.no_upper,
        digit=not args.no_digit,
        symbol=not args.no_symbol,
    )
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["secret"])
        print(f"# {result['analysis']['entropy_bits']} bits — {result['analysis']['strength']}")

if __name__ == "__main__":
    main()
