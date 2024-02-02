import json
from didkit import DIDKit

try:
    # Create a DIDKit instance
    dk = DIDKit()

    # Collect user information
    user_data = {
        "name": input("Enter your name: "),
        "email": input("Enter your email: "),
        # ... (collect other relevant information)
    }

    # Generate the verifiable credential (VC)
    vc = dk.issuer_create_credential(
        issuer_did=dk.key_did,
        subject_did=dk.key_did,  # Use a different subject DID if needed
        credential_data=user_data
    )

    # Present the VC to the user
    print("Your verifiable credential:")
    print(json.dumps(vc, indent=4))  # Print formatted JSON

    # Store the VC (optional)
    with open("credential.json", "w") as f:
        json.dump(vc, f)

except Exception as e:
    print("Error:", e)
