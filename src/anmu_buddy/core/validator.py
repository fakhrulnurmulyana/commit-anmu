def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email

def is_valid_remote_url(url: str) -> bool:
    return url.startswith(("http://", "https://", "git@"))

def is_valid_username(name: str) -> bool:
    return len(name.strip()) > 0