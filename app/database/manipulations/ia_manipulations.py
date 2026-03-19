from ..models import *
from..connection import init_db

def filter_ia(phone:str) -> IA:
    db = init_db()

    if not db:
        raise(Exception("Database connection error"))
    
    try: 
        ia = db.query(IA).filter(IA.phone_number == phone).first()

        if not ia:
            print(f"No IA found with phone number: {phone}")
            return None

        # Adicionar as Fks
        ia.ia_config
        ia.active_prompt

        print(f"IA Localizada: {ia.name} - {ia.phone_number}")
        return ia
    except Exception as ex:
        print(f"Error in filter_ia: {ex}")
    finally:
        if db:
            db.close()
    return None
    
