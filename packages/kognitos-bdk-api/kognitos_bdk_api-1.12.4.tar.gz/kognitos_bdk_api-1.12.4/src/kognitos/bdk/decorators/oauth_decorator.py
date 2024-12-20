import inspect
from typing import List, Optional, Type

from ..reflection import (BookOAuthAuthenticationDescriptor, OAuthFlow,
                          OAuthProvider)


class oauth:  # pylint: disable=invalid-name
    id: str
    provider: OAuthProvider
    flows: List[OAuthFlow]
    authorize_endpoint: str
    token_endpoint: str
    scopes: Optional[List[str]]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        id: str,  # pylint: disable=redefined-builtin
        provider: OAuthProvider,
        authorize_endpoint: str,
        token_endpoint: str,
        flows: Optional[List[OAuthFlow]] = None,
        scopes: Optional[List[str]] = None,
    ):
        self.id = id
        self.provider = provider
        self.flows = flows if flows else [OAuthFlow.AUTHORIZATION_CODE]
        self.authorize_endpoint = authorize_endpoint
        self.token_endpoint = token_endpoint
        self.scopes = scopes

    def __call__(self, cls: Type):
        def decorator(cls):
            if not inspect.isclass(cls):
                raise TypeError("The oauth decorator can only be applied to classes.")

            if not hasattr(cls, "__oauth__"):
                cls.__oauth__ = []

            cls.__oauth__.append(
                BookOAuthAuthenticationDescriptor(
                    id=self.id,
                    description=None,
                    provider=self.provider,
                    flows=self.flows,
                    authorize_endpoint=self.authorize_endpoint,
                    token_endpoint=self.token_endpoint,
                    scopes=self.scopes,
                    name="oauth",
                )
            )

            return cls

        if cls is None:
            return decorator

        return decorator(cls)
