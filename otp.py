#!/usr/bin/env python

import mintotp
import base64

admin_secret = base64.b32encode(b"admin").decode().replace("=", "")
totp_code = mintotp.totp(admin_secret)
print(totp_code)
