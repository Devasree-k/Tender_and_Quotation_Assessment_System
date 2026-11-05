class TenderNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class TenderBusinessRuleException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class InvalidTenderStatusException(TenderBusinessRuleException):
    def __init__(self, msg):
        super().__init__(msg)

class QuotationNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class QuotationBusinessRuleException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class QuotationAccessDeniedException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class EvaluationNotFoundException(Exception):
    def __init__(self, message: str = "Evaluation not found"):
        self.message = message
        super().__init__(self.message)


class EvaluationBusinessRuleException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EvaluationAccessDeniedException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class SanctionNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class SanctionBusinessRuleException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

    