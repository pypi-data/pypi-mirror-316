"""
:mod:`zsl_jwt.codec`
--------------------

The module provides the two main functions :func:`.encode` and :func:`.decode`
which encode and decode the given payload.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
from builtins import *  # NOQA
from typing import Any  # NOQA
from typing import Dict  # NOQA

import jwt
from zsl import Injected
from zsl import inject
from zsl.db.model.app_model_json_encoder import AppModelJSONEncoder
from zsl.errors import ZslError

from zsl_jwt.configuration import DEFAULT_PROFILE_NAME
from zsl_jwt.configuration import JWTConfiguration

#: The list of JWT claim names.
CLAIMS = ('exp', 'nbf', 'iss', 'aud', 'iat')


class ZslJwtError(ZslError):
    """Main exception type raised from this module."""
    pass


class ZslJwtInvalidAudienceError(ZslJwtError):
    """When the audience of the token does not match the
    audience of the profile used to decode the token."""
    pass


class ZslJwtExpiredSignatureError(ZslJwtError):
    pass


class ZslJwtInvalidNbfClaimError(ZslJwtError):
    pass


@inject(jwt_configuration=JWTConfiguration)
def encode(payload, profile=DEFAULT_PROFILE_NAME, jwt_configuration=Injected):
    # type: (Dict[str, str], str, JWTConfiguration, str)->str
    """
    Encodes the payload.
    :param payload: The payload to be encoded.
    :param jwt_configuration: The JWT configuration, it is injected.
    :param algorithm: Algorithm name. A reasonable default is provided.
    :param profile: The JWT profile to be used. See
                    :class:`zsl_jwt.configuration.JWTProfile`.
    :return: The JWT token.
    """
    payload = _append_claims(payload, profile)
    profile = jwt_configuration[profile]
    token = jwt.encode(payload, profile.secret, json_encoder=AppModelJSONEncoder,
                       algorithm=profile.algorithm)
    token = token.decode('ascii') if isinstance(token, bytes) else token
    return token


@inject(jwt_configuration=JWTConfiguration)
def decode(token, profile=DEFAULT_PROFILE_NAME, jwt_configuration=Injected):
    # type: (str, str, JWTConfiguration)->Dict[str, Any]
    """
    Decodes the encoded token.

    :param token: The encoded token.
    :param jwt_configuration: The configuration, injected.
    :param profile: The profile name used for encoding.
    :return: The decoded payload.
    """
    try:
        profile = jwt_configuration[profile]
        payload = jwt.decode(token, profile.secret, audience=profile.audience,
                             algorithms=[profile.algorithm])
    except jwt.InvalidAudienceError as e:
        raise ZslJwtInvalidAudienceError(e)
    except jwt.ExpiredSignatureError as e:
        raise ZslJwtExpiredSignatureError(e)
    except jwt.ImmatureSignatureError as e:
        raise ZslJwtInvalidNbfClaimError(e)
    except Exception as e:
        raise ZslJwtError(e)
    payload = _remove_claims(payload)
    return payload


@inject(jwt_configuration=JWTConfiguration)
def _append_claims(payload, profile, jwt_configuration):
    # type: (Dict[str, str], str, JWTConfiguration)->Dict[str, str]
    for claim in CLAIMS:
        if claim in payload:
            raise ZslJwtError(f"Claim '{claim}' found in payload. Please use payloads without claims - {CLAIMS}.")

    payload = payload.copy()
    profile = jwt_configuration[profile]
    payload['exp'] = datetime.datetime.now(tz=datetime.timezone.utc) + profile.expiration
    payload['nbf'] = datetime.datetime.now(tz=datetime.timezone.utc) + profile.not_before
    payload['iss'] = profile.issuer
    payload['aud'] = profile.audience
    payload['iat'] = datetime.datetime.now(tz=datetime.timezone.utc)
    return payload


def _remove_claims(payload):
    for claim in CLAIMS:
        del payload[claim]
    return payload
