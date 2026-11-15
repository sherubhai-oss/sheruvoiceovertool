# ==========================================
# SheRu VoIcE TooLs — ACCESS GATE
# ==========================================

import urllib.request
import urllib.parse
import json
import builtins

builtins._ok = False

# ==========================================
# CONFIGURATION
# ==========================================

api_url = 'https://script.google.com/macros/s/AKfycbyaDgk7KsW8a9FFCpnVxSCaMCV40-seQIhjVV3I1kld6ONHuBc1KwVyBSrZOvCah3k/exec'

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

    print('⚠️ No email entered.')

else:

    # ==========================================
    # DEVICE ID INPUT
    # ==========================================

    device_id = input(
        'Paste your Device ID from Authentication Webpage: '
    ).strip()

    if not device_id:

        print('⚠️ Device ID is required.')

    else:

        try:

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
                timeout=20
            ) as r:

                data = json.loads(
                    r.read().decode()
                )

            status = data.get('status', '')

            # ACCESS GRANTED

            if status == 'ok':

                builtins._ok = True

                print('\n✅ Access Granted!')

                print(
                    'Welcome:',
                    data.get('username', 'User')
                )

                print(
                    'Plan:',
                    data.get('plan', '')
                )

                print(
                    'Expiry:',
                    data.get('expiry', '')
                )

                if data.get('device') == 'registered':

                    print(
                        '📱 This device has been registered successfully.'
                    )

                else:

                    print(
                        '📱 Registered device verified.'
                    )

                print('Now run Step 2 below. 👇')

            # DEVICE MISMATCH

            elif status == 'device_mismatch':

                builtins._ok = False

                from IPython.display import display, HTML

                display(HTML("""
                <div style="font-family:Arial;max-width:580px;
                background:#24131b;border:1px solid #ff6b6b;
                border-radius:14px;padding:24px;color:white;">

                <h2 style="color:#ff9a9a;">
                🔒 Device Not Authorized
                </h2>

                <p>
                This Gmail is already registered on another device.
                Access from this device is blocked.
                </p>

                <p>
                📧 automationy156@gmail.com<br>
                📱 0337-7217981
                </p>

                <a href="https://wa.me/923377217981"
                style="background:#25d366;color:white;
                padding:12px 20px;border-radius:8px;
                text-decoration:none;">
                Contact Admin
                </a>

                </div>
                """))

            elif status == 'off':

                print('🔴 Your account is currently disabled.')

            elif status == 'expired':

                print('⏳ Your Subscription Has Expired.')

                print(
                    'Expiry:',
                    data.get('expires', '')
                )

                print('Contact: 0337-7217981')

            elif status == 'not_found':

                print('🔒 This Gmail is not registered.')

            elif status == 'bad_key':

                print('❌ Invalid Security Key.')

            else:

                print('❌ Access Denied.')

                print('Server Response:', data)

        except Exception as e:

            builtins._ok = False

            print('⚠️ Connection error.')

            print('Error:', str(e))
