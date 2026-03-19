from app.database.manipulations import ia_manipulations


def process_webhook_data(data:dict):
    """
    Função para processar todos os dados do webhook 
    """
    try:
        #coletar infos basicas
        ia_phone = data["sender"].split("@")[0]
        ia_name = data["instance"]
        print(f"Processing webhook data for phone: {ia_phone}, instance: {ia_name}", flush=True)

        # Pesquisar em nosso database qual IA direcionar
        ia_infos = ia_manipulations.filter_ia(ia_phone)
        print(f"IA found: {ia_infos}", flush=True)
        
    except Exception as ex:
        print(f"ERROR in process: {ex}", flush=True)