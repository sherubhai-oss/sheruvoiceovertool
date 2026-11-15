import requests
import builtins
from google.colab import output
from IPython.display import display, HTML
from getpass import getpass

# =====================================
# SHERU VOICE TOOLS CONFIGURATION
# =====================================

API_URL = "https://script.google.com/macros/s/AKfycbxfpb-HWCM_MuUtC8A0PaZK7brcMHd9IG8OG6pYg0eHiRTjG40l7JIbgaV0WxUq22Y/exec"

DEVICE_PAGE_URL = API_URL + "?action=devicePage"

SECRET_KEY = "sheru_secure_key_2026"

builtins._ok = False


# =====================================
# GMAIL INPUT
# =====================================

email = input("Enter Your Gmail: ").strip().lower()

if not email or "@" not in email:
    raise Exception("Please enter a valid Gmail address.")


# =====================================
# AUTOMATIC DEVICE ID RETRIEVAL
# =====================================

print("Verifying your device...")

device_id = output.eval_js("""
new Promise((resolve, reject) => {

    let iframe = document.createElement("iframe");

    iframe.style.display = "none";
    iframe.src = """ + repr(DEVICE_PAGE_URL) + """;

    let completed = false;

    function receiveDevice(event) {

        if (
            event.data &&
            event.data.type === "SHERU_DEVICE_ID" &&
            event.data.deviceId
        ) {

            if (!completed) {
                completed = true;

                window.removeEventListener(
                    "message",
                    receiveDevice
                );

                iframe.remove();

                resolve(event.data.deviceId);
            }
        }
    }

    window.addEventListener("message", receiveDevice);

    document.body.appendChild(iframe);

    setTimeout(() => {

        if (!completed) {

            window.removeEventListener(
                "message",
                receiveDevice
            );

            iframe.remove();

            reject("Device ID could not be retrieved.");

        }

    }, 20000);

})
""")


# =====================================
# SERVER VERIFICATION
# =====================================

try:

    response = requests.get(
        API_URL,
        params={
            "key": SECRET_KEY,
            "email": email,
            "deviceId": device_id
        },
        timeout=30
    )

    result = response.json()

    status = result.get("status", "")


    # =================================
    # ACCESS GRANTED
    # =================================

    if status == "ok":

        builtins._ok = True

        print("\nACCESS GRANTED")
        print("Welcome to SheRu Voice Tools!")

        print("Plan:", result.get("plan", ""))
        print("Username:", result.get("username", ""))
        print("Expiry:", result.get("expiry", ""))


    # =================================
    # ACCESS DENIED
    # =================================

    elif status == "device_mismatch":

        print("\nDEVICE NOT AUTHORIZED")
        print("This Gmail is already registered on another device.")

    elif status == "expired":

        print("\nSUBSCRIPTION EXPIRED")

    elif status == "off":

        print("\nACCOUNT DISABLED")

    elif status == "not_found":

        print("\nGMAIL NOT REGISTERED")

    elif status == "bad_key":

        print("\nINVALID API KEY")

    else:

        print("\nVERIFICATION FAILED:", status)


except Exception as e:

    print("\nCONNECTION ERROR:", str(e))

    builtins._ok = False
