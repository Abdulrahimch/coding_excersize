from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Length, NumberRange
from payment.validations import validate_credit_card, validate_enddate_field


class PaymentForm(FlaskForm):
    credit_card_number = wtforms.StringField('Credit Card Number ',
                                             validators=[DataRequired(), validate_credit_card])
    card_holder = wtforms.StringField('Card Holder', validators=[DataRequired()])
    expiration_date = wtforms.DateField('Expiration Date', format='%Y-%m-%d', validators=[DataRequired(), validate_enddate_field])
    security_code = wtforms.StringField('Security Code',
                                       validators=[DataRequired(), Length(min=3, max=3)])
    amount = wtforms.DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = wtforms.SubmitField('Pay with card')