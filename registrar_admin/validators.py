from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_even(value):
    if value < 3 :
        raise ValidationError(
            _('Year required to complete degree program cannot be less than 3 year '),
            params={'value': value},
        )

    if value > 6 :
        raise ValidationError(
            _('Year required to complete degree program cannot be greater than 6 year '),
            params={'value': value},
        )






# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# def year_required(value):
#     if value<3:
#         raise ValidationError(_("year required cannt be below 3"),params={'value': value},)
#     if value>6:
#         raise ValidationError(_("year >6"),params={'value': value},)

#     return value