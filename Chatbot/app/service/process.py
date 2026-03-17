from fastapi import APIRouter, BackgroundTasks, status
from app.service.process import process_webwook_data
router = APIRouter()

@router.post("/webhook", status_code=status.HTTP_200_OK)
def process_webwook_data(data:dict, backgrount_tasks: BackgroundTasks):
    """
    Função para processar todos os dados do webhook e processa em background
    """
    try:
        backgrount_tasks.add_task(process_webwook_data, data)
        return("")
    except Exception as ex:
        print(f"ERROR:" {ex})
        return{"message": "Error"}