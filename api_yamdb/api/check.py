def check_confirmation_code(user, confirmation_code) -> bool:
    return user.confirmation_code == confirmation_code
