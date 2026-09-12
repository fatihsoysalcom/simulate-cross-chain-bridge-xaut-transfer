# Simulate Cross Chain Bridge XAUT Transfer

This example simulates a simplified cross-chain bridge for a token like Tether Gold (XAUT). It demonstrates how assets are 'locked' on one blockchain (e.g., Ethereum) and 'minted' as a wrapped token (wXAUT) on another (e.g., Solana), and vice-versa. Crucially, it includes a `verify_bridge_integrity` function to illustrate the importance of maintaining invariant properties (total supply) for bridge security, highlighting a key aspect of risk assessment.

## Language

`python`

## How to Run

Save the code as `main.py`.
Run from your terminal: `python main.py`

## Original Article

This example accompanies the Turkish article: [Çapraz Zincir Köprü Risk Değerlendirmesi: Tether Gold Özelinde Derinlemesine Bir Bakış](https://fatihsoysal.com/blog/capraz-zincir-kopru-risk-degerlendirmesi-tether-gold-ozelinde-derinlemesine-bir-bakis/).

## License

MIT — see [LICENSE](LICENSE).
