import pymysql

from persistance.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash



class Word:

    def __init__(self, id: int, word: str, hint: str):
        self.id = id
        self.word = word
        self.hint = hint

    def get_random_words():
        """
            Obtiene 5 palabras aleatorias de la base de datos
            
            Returns:
                List[Word]: Lista de objetos Word con las palabras obtenidas
        """
        
        try: 
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            query = "SELECT id, word, hint FROM words ORDER BY RAND() LIMIT 5"
            cursor.execute(query)
            rs = cursor.fetchall()
            cursor.close()
            connection.close()
            
            words = [Word(w['id'], w['word'], w['hint']) for w in rs]
            
            return words
        except Exception as ex:
            print(f"Error trayendo palabras aleatorias: {ex}")
            return []
        
    def get_by_id(word_id):
        
        """
            Obtiene una palabra por su ID
            
            Returns: Word: Objeto Word, None si no se encuentra palabra con id dado
        """
        
        
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT id, word, hint FROM words WHERE id = %s"
            cursor.execute(query, (word_id,))   
            
            w = cursor.fetchone()
            
            return Word(w['id'], w['word'], w['hint'])
        except Exception as ex:
            print(f"Error trayendo palabra por id: {ex}")
            return None
        
    def get_all_words():
        """
            Obtiene todas las palabras de la base de datos
            
            Returns: List[Word]: Lista de objetos Word con todas las palabras
        """
        
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT id, word, hint FROM words"
            cursor.execute(query)   
            
            rs = cursor.fetchall()
            
            words = [Word(w['id'], w['word'], w['hint']) for w in rs]
            
            return words
        except Exception as ex:
            print(f"Error trayendo todas las palabras: {ex}")
            return []
        
    def create(word, hint):
        """
            Crea una nueva palabra en la base de datos
            
            Returns: bool: True si se creó correctamente, False en caso contrario
        """
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = "INSERT INTO words (word, hint) VALUES (%s, %s)"
            
            word_hash = generate_password_hash(word) #se hashea para que no sea visible en texto plano
            
            cursor.execute(query, (word_hash, hint))
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        except Exception as ex:
            print(f"Error creando palabra: {ex}")
            return False
    
    def delete(word_id):
        """
            Elimina una palabra de la base de datos por su ID
            
            Returns: bool: True si se eliminó correctamente, False en caso contrario
        """
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = "DELETE FROM words WHERE id = %s"
            cursor.execute(query, (word_id,))
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        except Exception as ex:
            print(f"Error eliminando palabra: {ex}")
            return False
        
    def edit(word_id, new_word, new_hint):
        """
            Edita una palabra existente en la base de datos
            
            Returns: bool: True si se editó correctamente, False en caso contrario
        """
        
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = "UPDATE words SET word = %s, hint = %s WHERE id = %s"
            
            new_word_hash = generate_password_hash(new_word) #se hashea para que no sea visible en texto plano
            
            cursor.execute(query, (new_word_hash, new_hint, word_id))
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        except Exception as ex:
            print(f"Error editando palabra: {ex}")
            return False
    
    def check_word(word_id, guess):
        """
            Verifica si la palabra adivinada es correcta comparándola con la palabra hasheada en la base de datos
            
            Returns: bool: True si la adivinanza es correcta, False en caso contrario
        """
        
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            query = "SELECT word FROM words WHERE id = %s"
            cursor.execute(query, (word_id,))
            w = cursor.fetchone()
            
            if not w:
                return False
            
            word_hash = w['word']
            
            return check_password_hash(word_hash, guess)
        except Exception as ex:
            print(f"Error verificando palabra: {ex}")
            return False