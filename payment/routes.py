from payment.forms import PaymentForm
from flask import render_template, flash, redirect, url_for
from payment import app
from flask_api import FlaskAPI, status, exceptions
from payment.payment_providers import PremiumPaymentGateway, CheapPaymentGateway, ExpensivePaymentGateway

cheap_payment = CheapPaymentGateway()
expensive_payment = ExpensivePaymentGateway()
premium_payment = PremiumPaymentGateway()

# Uncomment the payment that you want it to fail.
#premium_payment.server_failed = True
#expensive_payment.server_failed = True
#cheap_payment.server_failed = True

@app.route('/pay', methods=['GET','POST'])
def ProcessPayment():
    attempts = 1
    form = PaymentForm()
    if form.validate_on_submit():

        if form.amount.data <= 20:
            res = cheap_payment.payment_process()
            return render_template('200.html', res=res[1])

        elif form.amount.data >= 21 and form.amount.data <= 500:
            if not expensive_payment.server_failed:
                res = expensive_payment.payment_process()
                return render_template('200.html', res=res[1])
            else:
                res = cheap_payment.payment_process()
                return render_template('200.html', res=res[1])
            return render_template('errors/500.html')

        else:
            while attempts < 4:
                res = premium_payment.payment_process()
                if res[0] == 200:
                    return render_template('200.html', res=res[1])
                attempts += 1
            return render_template('errors/500.html')

    return render_template('index.html', form=form)

