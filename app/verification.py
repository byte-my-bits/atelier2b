from itsdangerous import URLSafeTimedSerializer
import configparser
import os

# Configuration
config_file_path = 'configuration.ini'

# TODO: Use jsonLOAD function
if not os.path.exists(config_file_path):
    print(f"Required {config_file_path} doesn't exist. Exiting...")
    # Print a list with all existing files.
    print("Existing files:")
    for root, dirs, files in os.walk("."):
        for file in files:
            if config_file_path in file:
                # Print file and abs file path
                print(f"Configuration file path: {os.path.join(root, file)}")

    exit(1)

config = configparser.ConfigParser()
config.read(config_file_path)
default = config['DEFAULT']

if not config:
    print("Error at reading configuration file. Exiting...")
    exit(1)

if not default:
    print("Error at reading default. Exiting...")
    exit(1)

SECRET_KEY = default['SECRET_KEY']
SECURITY_PASSWORD_SALT = default['SECURITY_PASSWORD_SALT']

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email
