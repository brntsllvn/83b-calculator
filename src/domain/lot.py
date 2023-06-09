from dataclasses import dataclass
from src.domain.portfolio_event import Grant, Vest


@dataclass
class Lot:
    acquisition_time_idx: int
    basis_per_share: float
    share_count: int

    def __eq__(self, o):
        if isinstance(o, Lot):
            equal = self.acquisition_time_idx == o.acquisition_time_idx and \
                self.basis_per_share == o.basis_per_share and \
                self.share_count == o.share_count
            return equal
        return False


def get_portfolio_lots(filed_83b, all_portfolio_events, share_price_process):
    if filed_83b:
        grant_share_price = share_price_process[0]
        grant_share_count = 0
        for portfolio_event in all_portfolio_events:
            if isinstance(portfolio_event, Grant):
                grant_share_count = portfolio_event.share_count
        lots = [Lot(0, grant_share_price, grant_share_count)]
        return lots

    lots = []
    for portfolio_event in all_portfolio_events:
        if isinstance(portfolio_event, Vest):
            event_basis = share_price_process[portfolio_event.time_idx]
            event_share_count = portfolio_event.share_count
            lot = Lot(portfolio_event.time_idx, event_basis, event_share_count)
            lots.append(lot)
    return lots
