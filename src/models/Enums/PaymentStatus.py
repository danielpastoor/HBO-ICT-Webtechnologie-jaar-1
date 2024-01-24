from enum import Enum


class PaymentStatus(Enum):
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    CANCELLED = 4
    ERROR = 5
