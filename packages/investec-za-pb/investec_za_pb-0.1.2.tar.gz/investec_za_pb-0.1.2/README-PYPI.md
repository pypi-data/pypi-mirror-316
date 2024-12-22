# investec-za-pb

Developer-friendly & type-safe Python SDK specifically catered to leverage *investec-za-pb* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=investec-za-pb&utm_campaign=python"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<br /><br />
> [!IMPORTANT]
> This SDK is not yet ready for production use. To complete setup please follow the steps outlined in your [workspace](https://app.speakeasy.com/org/rijnhardtkotze/investec-za-pb). Delete this section before > publishing to a package manager.

<!-- Start Summary [summary] -->
## Summary

SA PB Account Information: # Introduction
The Investec Private Banking API is a set of programmatic endpoints that can access Private Bank personal and business banking accounts. This API allows you to access the following:
- Accounts
- Balances
- Transactions
- Beneficiaries
- Beneficiary Payments
- Account Transfers
- Documents

There are many possible use cases for the Account Information API: from extracting the data to aggregate it with financial data from other banking institutions to personal money management tools. 

# Getting Started
To start using the Programmable Card API, you'll need API credentials, which you can access in your [Investec Online Banking](https://login.secure.investec.com) profile. Create a new API key (x-api-key) with specified API scopes. Remember to include the *cards* scope

Optionally, use the Investec Sandbox account and credentials to generate mock responses to test your applications. You can use the Sandbox account without opening an Investec Private Bank account. 

## Run with Postman
[Open the collection in postman](https://www.postman.com/investec-open-api/workspace/programmable-banking/collection/26868804-00260d55-0009-42ee-b148-d439992e64ff?action=share&creator=26868804)  
or fork  
[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/26868804-00260d55-0009-42ee-b148-d439992e64ff?action=collection%2Ffork&collection-url=entityId%3D26868804-00260d55-0009-42ee-b148-d439992e64ff%26entityType%3Dcollection%26workspaceId%3D905c2bab-81a1-4297-8b70-2456c776a7a0)

The instructions below will guide you through the process of authenticating in the Postman app: 
1. Set the verb to POST and enter the auth URL [https://openapi.investec.com/identity/v2/oauth2/token](https://openapi.investec.com/identity/v2/oauth2/token) as the request URL.
2. The endpoint receives your client ID and client secret as [BASIC](https://en.wikipedia.org/wiki/BASIC) authentication headers. Select the Authorization tab and select BASIC AUTH from the Type list.
3. Enter your client_ID into the USERNAME field and your secret into the PASSWORD field 
4. Select the Headers tab and enter the **x-api-key** into the KEY field
5. Enter your API key into the VALUE field
6. Select the Body tab and select the x-www-form-urlencoded option
7. Enter grant_type into the KEY field and client_credentials into the VALUE field.
8. Send off your request.

If your keys are valid, the response will contain an access token and the number of seconds the access token is valid. 
Sample response:
```json
{ "access_token": "Z1CRQarGOSogNuUhRlENi5iKAGqh�, "token_type": "Bearer", "expires_in": 1799, "scope": "accounts" }
```

# Authentication
1. OAuth 2.0 access tokens are used to authenticate requests. Your access token authorises you to use the Programmable Card API.
2. To call the API, you must exchange your client ID, secret and API (x-api-key) key for an access token. 
3. You need to include the access token in the Authorisation header with the designation bearer when making calls to the API
4. The access token returned during the authentication request is valid for 30 minutes, at which point it will expire, and you will need to request a new one by calling /identity/v2/oauth2/token again.

When you make calls to the API, include the access token in the Authorisation header with the designation as Bearer. 
<SecurityDefinitions /> 

# Release Notes 
2024-11-07
*   **Enhancement**: Added an additional pending transactions endpoint za/pb/v1/accounts/{accountid}/pending-transactions just returning the pending ones with only the properties available.
*   **Enhancement**: Added the pending transactions to the existing transactions endpoint. Append `?includePending=true` to the querystring
*   **Enhancement**: Added a uuid property to the transactions endpoint. `( accountId.Substring(accountId.Length - 5) + postingDate.Replace("-", "") + postedOrder.PadLeft(7, '0') )` This will only be populated for posted transaction on Private Bank Accounts. This is not a backend banking generated ID and will change if any of the properties making it up changes.
*   **Enhancement**: Added approved beneficiaries to the beneficiary endpoint. They can be identified by the `"beneficiaryType": "INVESTECAPPROVED"` property with another new property eg. `"approvedBeneficiaryCategory": "Municipalities"`

2023-09-07
*   **Enhancement**: Added payment initiation requiring authorisation

2023-08-24
*   **Enhancement**: Added document retreival
*   **Enhancement**: Added more balances to the Balance endpoint

2023-05-29
*   **Enhancement**: Updated response codes returned

2023-03-05
*   **Enhancement**: Added a sandbox environment

2022-11-25
*   **Enhancement**: Included inter account transfers v2 - Transfer Multiple v2
*   **Enhancement**: Included beneficiary payments - Pay Multiple
*   **Enhancement**: Included beneficiaries - Get Beneficiaries
*   **Enhancement**: Included beneficiary categories - Get Beneficiary Categories
*   **Enhancement**: Added properties kycCompliant and profileId to accounts - Get Accounts
*   **Enhancement**: Added property profileId to beneficiaries - Beneficiaries

2022-02-21
*   **Enhancement**: Included inter account transfers - Transfer Multiple

2021-10-01
*   **Fix**: The runningBalance on transactions shows (-) if it is a negative balance - Get Account Transactions

2020-07-21
*   **Enhancement**: Included transactionDate to - Get Account Transactions
*   **Enhancement**: Included date range filter to - Get Account Transactions

2020-09-08
*   **Fix**: Implemented CORS support
*   **Fix**: Implemented multi User-Agent support

2020-11-10
*   **Enhancement**: Included postedOrder to - Get Account Transactions
*   **Enhancement**: Included transactionType to - Get Account Transactions

2020-11-13
*   **Enhancement**: Included transaction type filter to - Get Account Transactions


More information about the API can be found at .
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [investec-za-pb](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#investec-za-pb)
* [Getting Started](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#getting-started)
  * [Run with Postman](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#run-with-postman)
* [Authentication](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#authentication)
* [Release Notes](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#release-notes)
  * [SDK Installation](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#sdk-installation)
  * [IDE Support](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#ide-support)
  * [SDK Example Usage](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#sdk-example-usage)
  * [Authentication](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#authentication-1)
  * [Available Resources and Operations](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#available-resources-and-operations)
  * [Retries](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#retries)
  * [Error Handling](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#error-handling)
  * [Server Selection](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#server-selection)
  * [Custom HTTP Client](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#custom-http-client)
  * [Debugging](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#debugging)
* [Development](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#development)
  * [Maturity](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#maturity)
  * [Contributions](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!TIP]
> To finish publishing your SDK to PyPI you must [run your first generation action](https://www.speakeasy.com/docs/github-setup#step-by-step-guide).


The SDK can be installed with either *pip* or *poetry* package managers.

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install git+https://github.com/rijnhardtkotze/investec-za-pb-python.git
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add git+https://github.com/rijnhardtkotze/investec-za-pb-python.git
```
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
# Synchronous Example
import investec_za_pb
from investec_za_pb import Investec
import os

with Investec(
    security=investec_za_pb.Security(
        client_id=os.getenv("INVESTEC_CLIENT_ID", ""),
        client_secret=os.getenv("INVESTEC_CLIENT_SECRET", ""),
    ),
) as investec:

    res = investec.accounts.get_all()

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
import investec_za_pb
from investec_za_pb import Investec
import os

async def main():
    async with Investec(
        security=investec_za_pb.Security(
            client_id=os.getenv("INVESTEC_CLIENT_ID", ""),
            client_secret=os.getenv("INVESTEC_CLIENT_SECRET", ""),
        ),
    ) as investec:

        res = await investec.accounts.get_all_async()

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name                            | Type   | Scheme                         | Environment Variable                                                       |
| ------------------------------- | ------ | ------------------------------ | -------------------------------------------------------------------------- |
| `client_id`<br/>`client_secret` | oauth2 | OAuth2 Client Credentials Flow | `INVESTEC_CLIENT_ID`<br/>`INVESTEC_CLIENT_SECRET`<br/>`INVESTEC_TOKEN_URL` |

You can set the security parameters through the `security` optional parameter when initializing the SDK client instance. For example:
```python
import investec_za_pb
from investec_za_pb import Investec
import os

with Investec(
    security=investec_za_pb.Security(
        client_id=os.getenv("INVESTEC_CLIENT_ID", ""),
        client_secret=os.getenv("INVESTEC_CLIENT_SECRET", ""),
    ),
) as investec:

    res = investec.accounts.get_all()

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [accounts](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/accounts/README.md)

* [get_all](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/accounts/README.md#get_all) - Get Accounts
* [get_balance](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/accounts/README.md#get_balance) - Get Account Balance
* [get_transactions](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/accounts/README.md#get_transactions) - Get Account Transactions
* [get_pending_transactions](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/accounts/README.md#get_pending_transactions) - Get Account Pending Transactions
* [get_profile_accounts](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/accounts/README.md#get_profile_accounts) - Get Profile Accounts
* [get_authorization_setup](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/accounts/README.md#get_authorization_setup) - Get Authorisation Setup Details
* [get_profile_beneficiaries](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/accounts/README.md#get_profile_beneficiaries) - Get Profile Beneficiaries

### [beneficiaries](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/beneficiaries/README.md)

* [pay_multiple](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/beneficiaries/README.md#pay_multiple) - Pay Multiple
* [get_all](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/beneficiaries/README.md#get_all) - Get Beneficiaries
* [get_categories](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/beneficiaries/README.md#get_categories) - Get Beneficiary Categories

### [documents](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/documents/README.md)

* [get_all](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/documents/README.md#get_all) - Get Documents
* [get_specific](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/documents/README.md#get_specific) - Get Document

### [inter_account_transfers](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/interaccounttransfers/README.md)

* [~~transfer~~](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/interaccounttransfers/README.md#transfer) - Transfer Multiple (TO BE DEPRECATED) :warning: **Deprecated**
* [transfer_v2](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/interaccounttransfers/README.md#transfer_v2) - Transfer Multiple v2


### [profiles](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/profiles/README.md)

* [get](https://github.com/rijnhardtkotze/investec-za-pb-python/blob/master/docs/sdks/profiles/README.md#get) - Get Profiles

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
import investec_za_pb
from investec_za_pb import Investec
from investec_za_pb.utils import BackoffStrategy, RetryConfig
import os

with Investec(
    security=investec_za_pb.Security(
        client_id=os.getenv("INVESTEC_CLIENT_ID", ""),
        client_secret=os.getenv("INVESTEC_CLIENT_SECRET", ""),
    ),
) as investec:

    res = investec.accounts.get_all(,
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
import investec_za_pb
from investec_za_pb import Investec
from investec_za_pb.utils import BackoffStrategy, RetryConfig
import os

with Investec(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    security=investec_za_pb.Security(
        client_id=os.getenv("INVESTEC_CLIENT_ID", ""),
        client_secret=os.getenv("INVESTEC_CLIENT_SECRET", ""),
    ),
) as investec:

    res = investec.accounts.get_all()

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations. All operations return a response object or raise an exception.

By default, an API error will raise a models.APIError exception, which has the following properties:

| Property        | Type             | Description           |
|-----------------|------------------|-----------------------|
| `.status_code`  | *int*            | The HTTP status code  |
| `.message`      | *str*            | The error message     |
| `.raw_response` | *httpx.Response* | The raw HTTP response |
| `.body`         | *str*            | The response content  |

When custom error responses are specified for an operation, the SDK may also raise their associated exceptions. You can refer to respective *Errors* tables in SDK docs for more details on possible exception types for each operation. For example, the `get_all_async` method may raise the following exceptions:

| Error Type      | Status Code | Content Type |
| --------------- | ----------- | ------------ |
| models.APIError | 4XX, 5XX    | \*/\*        |

### Example

```python
import investec_za_pb
from investec_za_pb import Investec, models
import os

with Investec(
    security=investec_za_pb.Security(
        client_id=os.getenv("INVESTEC_CLIENT_ID", ""),
        client_secret=os.getenv("INVESTEC_CLIENT_SECRET", ""),
    ),
) as investec:
    res = None
    try:

        res = investec.accounts.get_all()

        # Handle response
        print(res)

    except models.APIError as e:
        # handle exception
        raise(e)
```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import investec_za_pb
from investec_za_pb import Investec
import os

with Investec(
    server_url="https://openapi.investec.com",
    security=investec_za_pb.Security(
        client_id=os.getenv("INVESTEC_CLIENT_ID", ""),
        client_secret=os.getenv("INVESTEC_CLIENT_SECRET", ""),
    ),
) as investec:

    res = investec.accounts.get_all()

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from investec_za_pb import Investec
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Investec(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from investec_za_pb import Investec
from investec_za_pb.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Investec(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from investec_za_pb import Investec
import logging

logging.basicConfig(level=logging.DEBUG)
s = Investec(debug_logger=logging.getLogger("investec_za_pb"))
```

You can also enable a default debug logger by setting an environment variable `INVESTEC_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=investec-za-pb&utm_campaign=python)
