"""The package's own JS, exposed to the compiling app as shared assets.

``rx.asset(..., shared=True)`` resolves a file next to the module that calls it, so the call lives
here, beside ``trigger.jsx``. It links the file into the app's ``assets/external/`` and gives the
path a compiled module imports it from.
"""

import reflex as rx

#: ``sp_trigger``'s component as a module: what ``SpTrigger.library`` imports ``SilverpointTrigger`` from.
TRIGGER_MODULE: str = rx.asset("trigger.jsx", shared=True).importable_path
