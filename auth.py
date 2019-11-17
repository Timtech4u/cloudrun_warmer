import time
import jwt
import json
import requests
import httplib2

# Permissions to request for Access Token
scopes = "https://www.googleapis.com/auth/cloud-platform"

# Length of token's validity
expires_in = 3600  # Expires in 1 hour


def create_signed_jwt(pkey, pkey_id, email, scope):
    '''
    Create a Signed JWT from a service account Json json_keyentials file
    This Signed JWT will later be exchanged for an Access Token
    '''

    # Google Endpoint for creating OAuth 2.0 Access Tokens from Signed-JWT
    auth_url = "https://www.googleapis.com/oauth2/v4/token"

    issued = int(time.time())
    expires = issued + expires_in  # expires_in is in seconds

    # JWT Headers
    additional_headers = {
        'kid': pkey_id,
        "alg": "RS256",
        "typ": "JWT"  # Google uses SHA256withRSA
    }

    # JWT Payload
    payload = {
        "iss": email,		# Issuer claim
        "sub": email,		# Issuer claim
        "aud": auth_url,  # Audience claim
        "iat": issued,		# Issued At claim
        "exp": expires,		# Expire time
        "scope": scope		# Permissions
    }

    # Encode the headers and payload and sign creating a Signed JWT (JWS)
    sig = jwt.encode(payload, pkey, algorithm="RS256",
                     headers=additional_headers)

    return sig


def exchangeJwtForAccessToken(signed_jwt):
    '''
    This function takes a Signed JWT and exchanges it for a Google OAuth Access Token
    '''

    auth_url = "https://www.googleapis.com/oauth2/v4/token"

    params = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": signed_jwt
    }

    r = requests.post(auth_url, data=params)

    if r.ok:
        return(r.json()['access_token'], '')

    return None, r.text


def getAccessToken():
    # @TODO: Replace this with Service Account JSON Key
    json_key = {
        "type": "service_account",
        "project_id": "",
        "private_key_id": "",
        "private_key": "",
        "client_email": "",
        "client_id": "",
        "auth_uri": "",
        "token_uri": "",
        "auth_provider_x509_cert_url": "",
        "client_x509_cert_url": ""
    }

    private_key = json['private_key']

    s_jwt = create_signed_jwt(
        private_key,
        json_key['private_key_id'],
        json_key['client_email'],
        scopes)

    token, err = exchangeJwtForAccessToken(s_jwt)

    return token