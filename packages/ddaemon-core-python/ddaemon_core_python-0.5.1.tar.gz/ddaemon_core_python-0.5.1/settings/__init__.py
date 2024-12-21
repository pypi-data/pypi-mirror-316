"""(C) 2013-2024 Copycat Software, LLC. All Rights Reserved."""

__version__ = "0.5.1"

import django

from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy


django.utils.encoding.smart_text = smart_str
django.utils.encoding.smart_unicode = smart_str
django.utils.translation.ugettext_lazy = gettext_lazy
