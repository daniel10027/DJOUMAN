from infrastructure.providers.payments.fake_adapter import FakePaymentAdapter
from infrastructure.providers.payments.orange_money_adapter import OrangeMoneyAdapter
from infrastructure.providers.payments.mtn_momo_adapter import MtnMoMoAdapter
from infrastructure.providers.payments.wave_adapter import WaveAdapter
from infrastructure.providers.payments.stripe_adapter import StripeAdapter

def get_payment_provider(method: str):
    mapping = {
        "orange_money": OrangeMoneyAdapter(),
        "mtn_momo": MtnMoMoAdapter(),
        "wave": WaveAdapter(),
        "stripe": StripeAdapter(),
    }
    return mapping.get(method, FakePaymentAdapter())