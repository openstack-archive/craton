"""oslo.i18n integration module.

See http://docs.openstack.org/developer/oslo.i18n/usage.html

"""

import oslo_i18n


_translators = oslo_i18n.TranslatorFactory(domain='craton')

# The primary translation function using the well-known name "_"
_ = _translators.primary

# The contextual translation function using the name "_C"
_C = _translators.contextual_form

# The plural translation function using the name "_P"
_P = _translators.plural_form
