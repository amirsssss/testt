import random
import string

from django.conf import settings


# SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 12)


def code_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def urlcode_generator(size=30, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def pass_code_generator(size=50, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))