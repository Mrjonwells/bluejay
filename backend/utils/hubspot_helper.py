import os
import requests
from datetime import datetime

HUBSPOT_PORTAL_ID = os.getenv("HUBSPOT_PORTAL_ID")
HUBSPOT_FORM_ID = os.getenv("HUBSPOT_FORM_ID")
HUBSPOT_URL = f"https://api.hsforms.com/submissions/v3/integration/submit/{HUBSPOT_PORTAL_ID}/{HUBSPOT_FORM_ID}"

def submit_lead_to_hubspot(name, email, phone, thread_summary):
    try:
        data = {
            "submittedAt": int(datetime.utcnow().timestamp() * 1000),
            "fields": [
                {"name": "firstname", "value": name},
                {"name": "email", "value": email},
                {"name": "phone", "value": phone},
            ],
            "context": {
                "pageUri": "https://askbluejay.ai/",
                "pageName": "BlueJay Assistant"
            },
            "legalConsentOptions": {
                "consent": {
                    "consentToProcess": True,
                    "text": "I agree to allow BlueJay to store and process my personal data.",
                    "communications": [
                        {
                            "value": True,
                            "subscriptionTypeId": 999,
                            "text": "I agree to receive other communications from BlueJay."
                        }
                    ]
                }
            }
        }

        if thread_summary:
            data["fields"].append({"name": "message", "value": thread_summary})

        response = requests.post(HUBSPOT_URL, json=data, timeout=5)
        response.raise_for_status()
        print(f"HubSpot submission success: {response.status_code}")
        return True
    except Exception as e:
        print(f"HubSpot submission failed: {e}")
        return False
