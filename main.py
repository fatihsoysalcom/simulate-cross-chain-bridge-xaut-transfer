class Chain:
    """Represents a blockchain with its own token balances and locked assets."""
    def __init__(self, name: str):
        self.name = name
        self.balances = {}
        self.locked_assets = {} # assets locked on this chain for bridging out

    def add_token(self, token_symbol: str, amount: int):
        self.balances[token_symbol] = self.balances.get(token_symbol, 0) + amount

    def remove_token(self, token_symbol: str, amount: int):
        if self.balances.get(token_symbol, 0) < amount:
            raise ValueError(f"Insufficient {token_symbol} on {self.name}")
        self.balances[token_symbol] -= amount

    def lock_asset(self, token_symbol: str, amount: int):
        self.remove_token(token_symbol, amount)
        self.locked_assets[token_symbol] = self.locked_assets.get(token_symbol, 0) + amount
        print(f"  [{self.name}] Locked {amount} {token_symbol}. Current locked: {self.locked_assets[token_symbol]}")

    def unlock_asset(self, token_symbol: str, amount: int):
        if self.locked_assets.get(token_symbol, 0) < amount:
            raise ValueError(f"Insufficient locked {token_symbol} on {self.name} to unlock")
        self.locked_assets[token_symbol] -= amount
        self.add_token(token_symbol, amount)
        print(f"  [{self.name}] Unlocked {amount} {token_symbol}. Current locked: {self.locked_assets[token_symbol]}")

    def __str__(self):
        return f"Chain '{self.name}': Balances={self.balances}, Locked={self.locked_assets}"

class CrossChainBridge:
    """
    Simulates a simplified cross-chain bridge mechanism for Tether Gold (XAUT).
    It manages the transfer of XAUT between two simulated chains (e.g., Ethereum and Solana)
    by locking original XAUT on one chain and minting 'wrapped XAUT' on the other.
    """
    def __init__(self, initial_xaut_supply_eth: int):
        self.chains = {
            "Ethereum": Chain("Ethereum"),
            "Solana": Chain("Solana")
        }
        self.chains["Ethereum"].add_token("XAUT", initial_xaut_supply_eth)
        # Wrapped XAUT (wXAUT) is minted on Solana
        self.initial_total_supply_xaut = initial_xaut_supply_eth
        print(f"Bridge initialized with total XAUT supply: {self.initial_total_supply_xaut}")
        self.print_status()

    def print_status(self):
        print("\n--- Current Bridge State ---")
        for chain_name, chain in self.chains.items():
            print(chain)
        print("----------------------------")

    def transfer_xaut(self, from_chain_name: str, to_chain_name: str, amount: int):
        """
        Simulates transferring XAUT from 'from_chain' to 'to_chain'.
        This involves locking XAUT on the 'from_chain' and minting wXAUT on the 'to_chain'.
        """
        print(f"\n--- Initiating XAUT transfer: {amount} from {from_chain_name} to {to_chain_name} ---")
        from_chain = self.chains[from_chain_name]
        to_chain = self.chains[to_chain_name]

        # Step 1: Lock XAUT on the source chain (e.g., Ethereum).
        # This simulates XAUT being held in a bridge contract.
        from_chain.lock_asset("XAUT", amount)

        # Step 2: Mint wrapped XAUT (wXAUT) on the destination chain (e.g., Solana).
        # This wXAUT represents the locked XAUT on the source chain.
        to_chain.add_token("wXAUT", amount)
        print(f"  [{to_chain_name}] Minted {amount} wXAUT. Current balance: {to_chain.balances.get('wXAUT', 0)}")
        
        print(f"Transfer of {amount} XAUT completed from {from_chain_name} to {to_chain_name}.")
        self.print_status()
        self.verify_bridge_integrity()

    def reverse_transfer_xaut(self, from_chain_name: str, to_chain_name: str, amount: int):
        """
        Simulates transferring XAUT back from 'from_chain' (as wXAUT) to 'to_chain' (as original XAUT).
        This involves burning wXAUT on the 'from_chain' and unlocking XAUT on the 'to_chain'.
        """
        print(f"\n--- Initiating Reverse XAUT transfer: {amount} from {from_chain_name} (wXAUT) to {to_chain_name} (XAUT) ---")
        from_chain = self.chains[from_chain_name]
        to_chain = self.chains[to_chain_name]

        # Step 1: Burn wXAUT on the source chain (e.g., Solana).
        # This reduces the supply of wrapped tokens.
        from_chain.remove_token("wXAUT", amount)
        print(f"  [{from_chain_name}] Burned {amount} wXAUT. Current balance: {from_chain.balances.get('wXAUT', 0)}")

        # Step 2: Unlock original XAUT on the destination chain (e.g., Ethereum).
        # This releases the XAUT from the bridge contract.
        to_chain.unlock_asset("XAUT", amount)

        print(f"Reverse transfer of {amount} XAUT completed from {from_chain_name} to {to_chain_name}.")
        self.print_status()
        self.verify_bridge_integrity()

    def verify_bridge_integrity(self):
        """
        Performs a simplified integrity check, demonstrating a core aspect of bridge risk assessment.
        The total sum of original XAUT (unlocked + locked on Ethereum)
        plus wrapped XAUT (on Solana) should equal the initial total supply.
        Any deviation indicates a potential bridge vulnerability or exploit.
        """
        print("\n--- Verifying Bridge Integrity ---")
        eth_chain = self.chains["Ethereum"]
        sol_chain = self.chains["Solana"]

        # Total XAUT on Ethereum (unlocked + locked in bridge)
        current_xaut_eth = eth_chain.balances.get("XAUT", 0) + eth_chain.locked_assets.get("XAUT", 0)
        # Total wXAUT on Solana
        current_wxaut_sol = sol_chain.balances.get("wXAUT", 0)

        total_current_supply = current_xaut_eth + current_wxaut_sol

        if total_current_supply == self.initial_total_supply_xaut:
            print(f"  [INTEGRITY OK] Total XAUT (original + wrapped) = {total_current_supply}. Matches initial supply.")
        else:
            # This scenario represents a critical security risk, like a bridge exploit
            # where tokens are double-minted or lost.
            print(f"  [INTEGRITY COMPROMISED!] Total XAUT (original + wrapped) = {total_current_supply}. Expected: {self.initial_total_supply_xaut}.")
            print("  This indicates a potential bridge vulnerability or exploit (e.g., double minting or lost assets).")
        print("----------------------------------")


if __name__ == "__main__":
    # Initial setup: 1000 XAUT tokens exist on the Ethereum chain.
    initial_supply = 1000
    bridge = CrossChainBridge(initial_supply)

    # Scenario 1: Transfer 300 XAUT from Ethereum to Solana
    bridge.transfer_xaut("Ethereum", "Solana", 300)

    # Scenario 2: Transfer another 200 XAUT from Ethereum to Solana
    bridge.transfer_xaut("Ethereum", "Solana", 200)

    # Scenario 3: Transfer 150 XAUT back from Solana to Ethereum
    bridge.reverse_transfer_xaut("Solana", "Ethereum", 150)

    # --- Demonstrating a hypothetical bridge flaw (for educational purposes) ---
    # Imagine a scenario where the bridge *incorrectly* mints extra wXAUT without locking corresponding XAUT.
    print("\n--- SIMULATING A BRIDGE FLAW: Incorrectly minting extra wXAUT ---")
    # Directly manipulate the balance to simulate a flaw, bypassing proper bridge logic
    bridge.chains["Solana"].add_token("wXAUT", 50) 
    print("  [FLAW INJECTED] 50 extra wXAUT minted on Solana without corresponding lock.")
    bridge.print_status()
    bridge.verify_bridge_integrity() # This should now show a compromised state
    print("--- End of simulated flaw ---")

    # Continue with a normal transfer after the flaw (if the flaw wasn't catastrophic)
    bridge.transfer_xaut("Ethereum", "Solana", 100)
    bridge.reverse_transfer_xaut("Solana", "Ethereum", 200)
