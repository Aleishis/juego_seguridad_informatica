import pymysql

from persistance.db import get_connection


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