# UserAuthenticationService.py
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from DatabaseConfig import PostgreSQLConfig

class UserAuthenticationService:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=PostgreSQLConfig.DATABASE,
            user=PostgreSQLConfig.USER,
            password=PostgreSQLConfig.PASSWORD,
            host=PostgreSQLConfig.HOST,
            port=PostgreSQLConfig.PORT
        )

    def create_user(self, username, email, password):
        cursor = self.connection.cursor()
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            cursor.close()

    def verify_user(self, username, password):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            password_hash = cursor.fetchone()
            if password_hash and check_password_hash(password_hash[0], password):
                return True
            return False
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False
        finally:
            cursor.close()

    def __del__(self):
        self.connection.close()
