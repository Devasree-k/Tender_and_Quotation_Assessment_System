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


        