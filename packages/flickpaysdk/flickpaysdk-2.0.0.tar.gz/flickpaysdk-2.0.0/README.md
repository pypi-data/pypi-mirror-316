# Flick SDK For PYTHON

flick_paymentSDK is a secure and quick way for customers to access accounts and interact with the Flick API for Identity, Financial Data, Payouts, Collections, and Miscellaneous operations. It provides a straightforward integration for python developers.

## Features

- **Checkout:** Collect payments easily with various options.
- **Banking:** Retrieve bank lists, perform name inquiries, and manage payouts.
- **Identity Verification:** Verify BVN, NIN, CAC, and more.
- **Secure SDK:** Handles multi_factor authentication, credential validation, and error handling.

---

## Getting Started

1. **Register on Flick:** <br>
   Sign up at [Flick](https://merchant.getflick.co/) to obtain your API keys (`secret_key` and `public_key`).

2. **Installation:** <br>
   Install the package via `pip`:

   ```bash
   pip install flickpaysdk(latest version)
   pip install dataclasses 
   pip install requests
   ```
## How to Use the Class
1. ### Initialize the SDK with your secret key:
Create an instance of the flick_payment class using your secret_key.

Usage: <br>
Initialize the SDK

```python
import requests
from flickpaysdk.flick import FlickpaySDK, checkOutRequest

# Replace with your actual secret key
sdk = FlickpaySDK(secret_key="your_secret_key")
```

2. ### For Checkout charge request
Initiate a checkout process:

```python

checkout_payload = checkOutRequest(
    amount = "1000",
    Phoneno = "1234567890",
    currency_collected = "NGN",
    currency_settled = "USD",
    email = "example@example.com",
    redirectUrl = "https://example.com/redirect",
    webhookUrl = "https://example.com/webhook",
)
charge_response = sdk.flickCheckOut(checkout_payload) 
print(charge_response)
```

3. ### Bank List Retrieval
Retrieve a list of supported banks:

```python

bank_list = sdk.flickBankListSdk()
print(bank_list)
```

4. ### Bank Name Inquiry
Perform a bank name inquiry:


```python

bank_name_payload = BankNameRequest(
    account_number = "1234567890",
    bank_code = "001"
)
response = sdk.flickBankNameInquiry(bank_name_payload)
print(response)
```

5. ### Payout Initialization
Initiate a payout:

```python

payout_payload = PayoutRequest(
    bank_name = "Example Bank",
    bank_code = "012",
    account_number = "1234567890",
    amount = "1000",
    narration = "Payment for services",
    currency = "NGN",
    beneficiary_name = "John Doe",
)
response = sdk.flickInitiatePayoutSdk(payout_payload)
print(response)
```

6. ### Payout Verification
Verify a payout:

```python

transaction_id = "1234567890"
verify_payout_response = verify_payout_response = sdk.flickVerifyPayoutSdk(transaction_id)
print(verify_payout_response)
```

7. ### Identity Verification
Perform various identity verifications:

```python

*** BVN Verification ***

bvn_payload = BvnRequest(
    data_type = "basic",
    data = "0000222211"
)
bvn_response = sdk.flickIdentityBvnSdk(bvn_payload)
print(bvn_response)


 *** NIN Verification ***

nin_payload = NinRequest(
    nin = "0001111222",
    dob = "0000222211"
)
nin_response = sdk.flickIdentityNinSdk(nin_payload)
print(nin_response)


*** CAC Verification (Basic) ***

cac_payload = CacRequest(
    rcNumber = "0001111222"
)
cac_response = sdk.flickIdentityCacBasicSdk(cac_payload)
print(cac_response)



*** CAC Verification (Advance) ***

cac_payload = CacRequest(
    rcNumber = "0001111222"
)
cac_response = sdk.flickIdentityCacBasicSdk(cac_payload)
print(cac_response)

```

# Best Practices
Always handle exceptions raised by API calls.
Store your secret_key securely to prevent unauthorized access.
# Support
If you need help with flick_paymentSDK or your Flick integration, reach out to support@getflick.app or join our Slack channel.

License
This project is licensed under the MIT License.
```
# pythonsdk
