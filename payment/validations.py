from datetime import datetime
from wtforms.validators import ValidationError

def validate_credit_card(form, field):
    odd = []
    even = []
    credit_card_no = field.data.replace(' ', '')
    # split all items into 2 sets
    for item in range(0, len(credit_card_no)):
        if item%2 == 0:
            even.append(int(credit_card_no[item]))
        else:
            odd.append(int(credit_card_no[item]))

    # Double all numbers in the first set
    double_even = [i*2 for i in even]

    # Add all double digit numbers as the sum of their digits
    sum_double_even = 0
    for i in double_even:
        if i > 9:
            sum_double_even += abs(9 - i)
        else:
            sum_double_even += i

    # Add all the odd digits to the even
    sum_total = sum_double_even + sum(odd)

    # If the final result is not divisible by 10, the card number is not valid.
    if sum_total%10 != 0:
        raise ValidationError('The credit card is not valid')

def validate_enddate_field(form, field):
    if field.data < datetime.today().date():
        raise ValidationError('Expiration date can not be in the past!')
