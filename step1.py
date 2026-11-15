# SheRu VoIcE TooLs — access gate with Device Lock

import urllib.request
import json
import urllib.parse
import builtins

builtins._ok = False

from google.colab.output import eval_js

# ==========================================
# CONFIGURATION
# ==========================================

api_url = 'https://script.google.com/macros/s/AKfycbzePUme8b5O7PMGiHsA9zVSYLhFOmtvb99dgyp7mcxDu2PhcGBMmBr1NJsOfgO_s0A/exec'

secret_key = 'sheru_secure_key_2026'

# ==========================================
# EMAIL INPUT
# ==========================================

try:
    em = input(
        'Enter your registered Gmail, then press Enter: '
    ).strip().lower()

except Exception:
    em = ''

if not em:

    print(
        '⚠️ No email entered. Run this cell again '
        'and type your registered Gmail.'
    )

else:

    try:

        # ==========================================
        # DEVICE ID GENERATION
        # ==========================================

        device_id = eval_js("""
        (() => {

          let id = localStorage.getItem('sheru_device_id');

          if (!id) {

            id = 'SHERU-' + (
              crypto.randomUUID
                ? crypto.randomUUID()
                : Math.random().toString(36).substring(2)
                  + Date.now().toString(36)
            );

            localStorage.setItem('sheru_device_id', id);

          }

          return id;

        })()
        """)

        print('📱 Device ID:', device_id)

        # ==========================================
        # SERVER VERIFICATION
        # ==========================================

        params = {
            'key': secret_key,
            'email': em,
            'deviceId': device_id
        }

        request_url = (
            api_url
            + '?'
            + urllib.parse.urlencode(params)
        )

        req = urllib.request.Request(
            request_url,
            headers={
                'User-Agent': 'Mozilla/5.0'
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=15
        ) as r:

            data = json.loads(
                r.read().decode()
            )

        status = data.get('status', '')

        # ==========================================
        # ACCESS GRANTED
        # ==========================================

        if status == 'ok':

            builtins._ok = True

            print('\n✅ Access Granted!')
            print('Welcome:', data.get('username', 'User'))
            print('Plan:', data.get('plan', ''))
            print('Expiry:', data.get('expiry', ''))

            if data.get('device') == 'registered':

                print(
                    '📱 This device has been registered successfully.'
                )

            elif data.get('device') == 'verified':

                print(
                    '📱 Registered device verified.'
                )

            print(
                'Now run Step 2 below. 👇'
            )

        # ==========================================
        # DEVICE MISMATCH
        # ==========================================

        elif status == 'device_mismatch':

            builtins._ok = False

            from IPython.display import display, HTML

            display(HTML(
                "<div style='font-family:Inter,Arial,sans-serif;max-width:580px;background:linear-gradient(135deg,#1c0f14,#2a1420);border:1.5px solid #ff6b6b;border-radius:14px;padding:24px 28px;'>"
                "<div style='font-size:1.3em;font-weight:800;color:#ff9a9a;'>&#128274; Device Not Authorized</div>"
                "<div style='color:#e8d4d4;margin-top:10px;line-height:1.65;'>This Gmail is already registered on another device. Access from this device is blocked.</div>"
                "<div style='margin-top:16px;color:#fff;line-height:2;font-size:1em;'>&#128231; &nbsp;<b>Email:</b> &nbsp;automationy156@gmail.com<br>&#128172; &nbsp;<b>WhatsApp:</b> &nbsp;0337-7217981</div>"
                "<a href='https://wa.me/923377217981' target='_blank' style='display:inline-block;margin-top:18px;background:linear-gradient(135deg,#25d366,#128c7e);color:#fff;text-decoration:none;padding:11px 24px;border-radius:9px;font-weight:700;font-size:.95em;'>&#128172; Contact Admin</a>"
                "</div>"
            ))

        # ==========================================
        # SERVICE OFF
        # ==========================================

        elif status == 'off':

            print(
                '🔴 Your account is currently disabled. '
                'Please contact the administrator.'
            )

        # ==========================================
        # SUBSCRIPTION EXPIRED
        # ==========================================

        elif status == 'expired':

            from IPython.display import display, HTML

            exp = str(data.get('expires', ''))

            exp_line = (
                "<div style='color:#f2c9c9;margin-top:6px;font-size:.9em;'>Your access ended on <b>"
                + exp
                + "</b>.</div>"
            ) if exp else ""

            display(HTML(
                "<div style='font-family:Inter,Arial,sans-serif;max-width:580px;background:linear-gradient(135deg,#1c0f14,#2a1420);border:1.5px solid #ff6b6b;border-radius:14px;padding:24px 28px;'>"
                "<div style='font-size:1.3em;font-weight:800;color:#ff9a9a;'>&#9203; Your Subscription Has Expired</div>"
                + exp_line +
                "<div style='color:#e8d4d4;margin-top:10px;line-height:1.65;'>Your access to <b style='color:#fff;'>SheRu VoIcE TooLs</b> has ended. To renew and reactivate your account, please contact us:</div>"
                "<div style='margin-top:16px;color:#fff;line-height:2;font-size:1em;'>&#128231; &nbsp;<b>Email:</b> &nbsp;automationy156@gmail.com<br>&#128172; &nbsp;<b>WhatsApp:</b> &nbsp;0337-7217981</div>"
                "<a href='https://wa.me/923377217981' target='_blank' style='display:inline-block;margin-top:18px;background:linear-gradient(135deg,#25d366,#128c7e);color:#fff;text-decoration:none;padding:11px 24px;border-radius:9px;font-weight:700;font-size:.95em;'>&#128172; Renew on WhatsApp</a>"
                "</div>"
            ))

        # ==========================================
        # EMAIL NOT FOUND
        # ==========================================

        elif status == 'not_found':

            from IPython.display import display, HTML

            display(HTML(
                "<div style='font-family:Inter,Arial,sans-serif;max-width:580px;background:linear-gradient(135deg,#141018,#1e1420);border:1.5px solid #e0685a;border-radius:14px;padding:24px 28px;'>"
                "<div style='font-size:1.3em;font-weight:800;color:#ff9a8f;'>&#128274; Access Denied</div>"
                "<div style='color:#e0d2d2;margin-top:10px;line-height:1.65;'>This account is not approved yet. To get access to <b style='color:#fff;'>SheRu VoIcE TooLs</b>, please contact us:</div>"
                "<div style='margin-top:16px;color:#fff;line-height:2;font-size:1em;'>&#128231; &nbsp;<b>Email:</b> &nbsp;automationy156@gmail.com<br>&#128172; &nbsp;<b>WhatsApp:</b> &nbsp;0337-7217981</div>"
                "<a href='https://wa.me/923377217981' target='_blank' style='display:inline-block;margin-top:18px;background:linear-gradient(135deg,#25d366,#128c7e);color:#fff;text-decoration:none;padding:11px 24px;border-radius:9px;font-weight:700;font-size:.95em;'>&#128172; Get Access on WhatsApp</a>"
                "</div>"
            ))

        elif status == 'bad_key':

            print('❌ Invalid Security Key.')

        else:

            print('❌ Access Denied.')
            print('Server Response:', data)

    except Exception as e:

        builtins._ok = False

        print(
            '⚠️ Connection error. Make sure "Internet" '
            'is ON in the right-side Settings panel, then run again.'
        )

        print('Error:', str(e))
