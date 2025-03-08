#!/usr/bin/env python

import mintotp
import base64

admin_secret = "GBYHMZDVMVRVIV3YJ44G66LNPFRXG6LC"
totp_code = mintotp.totp(admin_secret)
print(totp_code)
