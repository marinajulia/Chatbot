
def process_webhook_data(data:dict):
    """
    Função para processar todos os dados do webhook 
    """
    try:
        #coletar infos basicas
        ia_phone = data["sender"].split("@")[0]
        ia_name = data["instance"]

        # Pesquisae em nosso database qual IA direcionar
        print(data)
    except Exception as ex:
        print(f"ERROR in process: {ex}")