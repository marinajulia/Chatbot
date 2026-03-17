
def process_webhook_data(data:dict):
    """
    Função para processar todos os dados do webhook 
    """
    try:
        print(data)
    except Exception as ex:
        print(f"ERROR in process: {ex}")