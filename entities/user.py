from entities.permissions import Permission
from persistance.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from enums.value_permission import ValuePermission
from enums.profile import Profile
import pymysql
from flask_login import UserMixin
from typing import Optional

class User(UserMixin):
    
    def __init__(self,id:int, name:str, email:str, password:str, profile:Profile, permissions:list[ValuePermission], is_active:bool):
        
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.profile = profile
        self.permissions = permissions
        self._is_active = is_active
        
    
         
    @property
    def is_active(self):
        return self._is_active
    
    def check_email_exists(email) -> bool:
        """
            Verifica si la cuenta de correo electrónico ya se encuentra registrada.

            Parameters:
                email (str): Correo electrónico a validar.

            Returns:
                bool: True si el correo ya se encunetra registrado; de lo contrario, False.
        """
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT email from users WHERE email = %s"
        cursor.execute(sql, (email,))

        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row is not None
    
        
    def save(name: str, email:str, password:str) -> bool:
        """
            Guarda un registro de usuario en la base de datos

            Parameters:
                name (str): Nombre del usuario.
                email (str): Correo electrónico del usuario.
                password (str): Contraseña del usuario en texto plano.

            Returns:
                bool: True si la cuenta se guardó correctamente; de lo contrario, False.
        """
        try:
            connection = get_connection()
            cursor = connection.cursor()
            hash_password = generate_password_hash(password)

            query = "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, hash_password))
            connection.commit()

            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error saving users:{ex}")
            return False
    
    
    #probar con join
    def check_login(email: str, password: str) -> Optional["User"]:
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT id, name, email, password_hash, is_active, profile
                FROM users
                WHERE email = %s
            """
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if not user:
                return None

            if not check_password_hash(user["password_hash"], password):
                return None

            return User(
                user["id"],
                user["name"],
                user["email"],
                "",
                user["profile"],
                [],
                bool(user["is_active"])
            )

        except Exception as ex:
            print(f"Error login user: {ex}")
            return None


    #Agregarle los permissions igual que en login()
    def get_by_id(user_id):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = "SELECT id,name, email, profile, is_active FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            
            user = cursor.fetchone()

            cursor.close()
            connection.close()
            return User(user['id'],
                            user['name'],
                            user['email'], 
                            '', 
                            user['profile'],
                            [],
                            bool(user['is_active']))
                
        except Exception as ex:
            print(f"Error loging user:{ex}")
            return None
        
    
    def get_all_users():
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            query = "SELECT id, name, email, profile, is_active FROM users"
            cursor.execute(query)
            
            users = cursor.fetchall()

            cursor.close()
            connection.close()
            
            return users
                
        except Exception as ex:
            print(f"Error trayendo los usuarios:{ex}")
            return False
    
    
    def delete_user(user_id: int):
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()

            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            print(f"Error deleting user:{ex}")
            return False