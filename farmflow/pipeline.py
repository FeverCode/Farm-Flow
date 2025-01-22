from social_core.exceptions import AuthForbidden
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist

def check_existing_email(backend, details, user=None, *args, **kwargs):
    """
    Checks if a user with the provided email already exists. If an existing user 
    is found, validates whether the user is associated with the current backend.
    
    Parameters:
    - backend: The authentication backend being used.
    - details: Dictionary containing user details like email.
    - user: Currently logged-in user (if any).

    Returns:
    - A dictionary containing the existing user if found and valid.

    Raises:
    - AuthForbidden: If an account with the email exists but belongs to another auth provider.
    """
    if user:
        return None  # If a user is already logged in, no further checks are required.

    email = details.get('email')
    if not email:
        return None  # No email provided, cannot perform checks.

    try:
        existing_user = User.objects.get(email=email)
        if social_auth := existing_user.social_auth.filter(
            provider=backend.name
        ).exists():
            # User is already linked to this backend, allow login.
            return {'user': existing_user}
        else:
            # User exists with this email but is linked to another provider.
            raise AuthForbidden(
                backend,
                'An account already exists with this email. Please log in with your original account credentials.'
            )
    except ObjectDoesNotExist:
        # No user found with the given email, proceed with normal flow.
        return None

def check_existing_email(backend, details, user=None, *args, **kwargs):
    if not user:
        if email := details.get('email'):
            if existing_user := User.objects.filter(email=email).first():
                if social := existing_user.social_auth.filter(
                    provider=backend.name
                ).first():
                    # User already has account with this social auth, proceed with login
                    return {'user': existing_user}
                else:
                    # User exists but with different auth method
                    raise AuthForbidden(
                        backend,
                        'An account already exists with this email. Please login with your original account credentials.'
                    )
