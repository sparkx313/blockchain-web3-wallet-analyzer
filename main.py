import random
from dataclasses import dataclass, field
from typing import List

@dataclass
class TokenHolding:
    symbol: str
    amount: float
    cost_basis_usd: float
    current_price_usd: float

    @property
    def current_value_usd(self) -> float:
        return self.amount * self.current_price_usd

    @property
    def unrealized_pnl(self) -> float:
        return self.current_value_usd - self.cost_basis_usd

    @property
    def roi(self) -> float:
        if self.cost_basis_usd == 0:
            return 0.0
        return (self.current_value_usd - self.cost_basis_usd) / self.cost_basis_usd

@dataclass
class WalletPortfolio:
    address: str
    holdings: List[TokenHolding] = field(default_factory=list)

    @property
    def total_value_usd(self) -> float:
        return sum(h.current_value_usd for h in self.holdings)

    @property
    def total_cost_basis(self) -> float:
        return sum(h.cost_basis_usd for h in self.holdings)

    @property
    def total_unrealized_pnl(self) -> float:
        return sum(h.unrealized_pnl for h in self.holdings)

    def print_report(self):
        print(f"Wallet: {self.address[:10]}...")
        print(f"{'Symbol':<10} {'Amount':>12} {'Price':>10} {'Value':>12} {'P&L':>12} {'ROI':>8}")
        print("-" * 70)
        for h in sorted(self.holdings, key=lambda x: x.current_value_usd, reverse=True):
            pnl_str = f"${h.unrealized_pnl:+,.2f}"
            print(f"{h.symbol:<10} {h.amount:>12.4f} {h.current_price_usd:>10.2f} "
                  f"${h.current_value_usd:>10,.2f} {pnl_str:>12} {h.roi:>7.1%}")
        print("-" * 70)
        print(f"{'TOTAL':<10} {'':>12} {'':>10} ${self.total_value_usd:>10,.2f} "
              f"${self.total_unrealized_pnl:>+10,.2f} "
              f"{self.total_unrealized_pnl/max(self.total_cost_basis,1):>7.1%}")

if __name__ == "__main__":
    random.seed(42)
    prices = {"ETH": 3450, "BTC": 67000, "USDC": 1.0, "ARB": 1.85, "UNI": 7.20, "LINK": 14.50}
    wallet = WalletPortfolio("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    for sym, price in prices.items():
        amt = random.uniform(0.1, 10) if sym != "USDC" else random.uniform(1000, 50000)
        cost = amt * price * random.uniform(0.4, 1.6)
        wallet.holdings.append(TokenHolding(sym, amt, cost, price))
    wallet.print_report()
