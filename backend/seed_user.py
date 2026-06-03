import argparse

from database.database import SessionLocal
from database.models import User
from auth.password_manager import PasswordManager
from database.user_repository import UserRepository


def seed_user(email: str, password: str):
    email = email.strip().lower()
    if not email or not password:
        raise ValueError('Both email and password are required.')

    existing_user = UserRepository.get_by_email(email)
    if existing_user:
        print(f'User already exists: {email}')
        return False

    hashed_password = PasswordManager.hash_password(password)
    user = UserRepository.create_user(email, hashed_password)

    if not user:
        print('Failed to create user. Check the database or email uniqueness.')
        return False

    print(f'Seed user created: {email}')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed a user into the backend SQLite database.')
    parser.add_argument('--email', help='Email address for the seed user')
    parser.add_argument('--password', help='Password for the seed user')
    parser.add_argument('--show-count', action='store_true', help='Show current user count and exit')
    args = parser.parse_args()

    if args.show_count:
        session = SessionLocal()
        count = session.query(User).count()
        session.close()
        print(f'Current user count: {count}')
    elif args.email and args.password:
        seed_user(args.email, args.password)
    else:
        parser.error('Either --show-count or both --email and --password are required.')
