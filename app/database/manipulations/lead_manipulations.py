from ..models import *
from ..connection import init_db

def filter_lead(phone:str, message:dict) -> Lead:
    db = init_db()

    if not db:
        raise(Exception("Database connection failed"))
    
    try:
        lead =db.query(Lead).filter(Lead.phone == phone).first()
        if not lead:
            print(f"No lead found for phone number: {phone}", flush=True)
            return None
        
        historico = lead.message
        if not historico:
            historico = []

        historico.append(message)

        lead.message = historico
        db.commit()
        db.refresh(lead)
        print(f"Lead updated successfully for phone number: {lead.name}-{lead.phone}", flush=True)

        return lead
    except Exception as ex:
        print(f"ERROR in filter_lead: {ex}", flush=True)
    
    finally:
        db.close()
    return None


def new_lead(ia_id:int, name:str, phone:str, message:list) -> Lead:
    db = init_db()

    if not db:
        raise(Exception("Database connection failed"))
    
    try:
        lead = Lead(
            ia_id=ia_id,
            name=name,
            phone=phone,
            message=message
        )

        db.add(lead)
        db.commit()
        db.refresh(lead)

        print(f"New lead created successfully for phone number: {lead.name}-{lead.phone}", flush=True)

        return lead
    except Exception as ex:
        print(f"ERROR in new_lead: {ex}", flush=True)
    
    finally:
        db.close()
    return None