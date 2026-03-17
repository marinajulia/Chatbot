from fastapi import APIRouter, BackgroundTasks, status


router = APIRouter()

@router.post("/webhook", status_code= status.HTTP_200_OK)

async def receive_webhook(data: dict, backgrount_tasks: BackgroundTasks):
    """
    Endpoint que recebe os dados do webhook e processa em backgroud
    """

    try:
        print(data)
    except Exception as ex:
        print(f"ERROR: {ex}")
        return {"message": "Error"}