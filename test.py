import unittest
# import requests
from flask_api import status
from payment import app
from payment.forms import PaymentForm
from flask import Flask, request
from payment.payment_providers import PremiumPaymentGateway, ExpensivePaymentGateway, CheapPaymentGateway

class APITest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_pay(self):
        with app.app_context():
            form = PaymentForm()
            form.amount.data = 50
            res = self.app.get('/pay')
            self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_PremiumPaymentGateway_payment_success(self):
        premium_payment_gateway = PremiumPaymentGateway()
        res = premium_payment_gateway.payment_process()
        self.assertEqual(200, res[0])
        self.assertEqual(res[1], 'Your payment is successful via PremiumPaymentGateway.')

    def test_PremiumPaymentGateway_failed(self):
        premium_payment_gateway = PremiumPaymentGateway()
        premium_payment_gateway.server_failed = True
        res = premium_payment_gateway.payment_process()
        self.assertEqual(500, res[0])

    def test_ExpensivePaymentGateway_payment_success(self):
        expensive_payment_gateway = ExpensivePaymentGateway()
        res = expensive_payment_gateway.payment_process()
        self.assertEqual(200, res[0])

    def test_ExpensivePaymentGateway_payment_failed(self):
        expensive_payment_gateway = ExpensivePaymentGateway()
        expensive_payment_gateway.server_failed = True
        res = expensive_payment_gateway.payment_process()
        self.assertEqual(500, res[0])

    def test_CheapPaymentGateway_payment_success(self):
        cheap_payment_gateway = CheapPaymentGateway()
        res = cheap_payment_gateway.payment_process()
        self.assertEqual(200, res[0])

    def test_CheapPaymentGateway_payment_failed(self):
        cheap_payment_gateway = CheapPaymentGateway()
        cheap_payment_gateway.server_failed = True
        res = cheap_payment_gateway.payment_process()
        self.assertEqual(500, res[0])

    def test_CheapPaymentGateway_sucess_after_3_PremiumPaymentGateway_failure(self):
        premium_payment_gateway = PremiumPaymentGateway()
        cheap_payment_gateway = CheapPaymentGateway()

        premium_payment_gateway.server_failed = True
        cheap_payment_gateway.server_failed = False

        attempts = 1
        while attempts < 4:
            res = premium_payment_gateway.payment_process()
            self.assertEqual(500, res[0])
            attempts += 1

        res = cheap_payment_gateway.payment_process()
        self.assertEqual(200, res[0])
        self.assertEqual(res[1], 'Your payment is successful via CheapPaymentGateway.')

    def test_CheapPaymentGateway_sucess_after_1_ExpensivePaymentGateway_failure(self):
        cheap_payment_gateway = CheapPaymentGateway()
        expensive_payment_gateway = ExpensivePaymentGateway()
        expensive_payment_gateway.server_failed = True

        attempts = 0
        while attempts < 1:
            res = expensive_payment_gateway.payment_process()
            self.assertEqual(500, res[0])
            attempts += 1
        res = cheap_payment_gateway.payment_process()
        self.assertEqual(200, res[0])
        self.assertEqual(res[1], 'Your payment is successful via CheapPaymentGateway.')