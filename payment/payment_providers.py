from flask_api import status


class payment_provider:
    server_failed = False
    def payment_process(self):
        if not self.server_failed:
            return (status.HTTP_200_OK, self.response)
        else:
            return (status.HTTP_500_INTERNAL_SERVER_ERROR, 'We are experiencing some trouble on our end. Please try again in the near future')


class PremiumPaymentGateway(payment_provider):
    response = 'Your payment is successful via PremiumPaymentGateway.'


class ExpensivePaymentGateway(payment_provider):
    response = 'Your payment is successful via ExpensivePaymentGateway.'


class CheapPaymentGateway(payment_provider):
    response = 'Your payment is successful via CheapPaymentGateway.'



