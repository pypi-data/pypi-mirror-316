# Type hints for the subset of sh we use.
# Extend as needed.
#
# Copyright (C) 2021 Collabora Ltd
# Copyright (C) 2021 Andrej Shadura <andrew.shadura@collabora.co.uk>
#
# SPDX-License-Identifier: GPL-2.0-or-later

class ErrorReturnCode(Exception): ...

DEFAULT_ENCODING: str
__version__: str
