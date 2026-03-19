from app.database.manipulations import ia_manipulations


def process_webhook_data(data:dict):
    """
    Função para processar todos os dados do webhook 
    """
    try:
        #coletar infos basicas
        ia_phone = data["sender"].split("@")[0]
        ia_name = data["instance"]

        # Pesquisar em nosso database qual IA direcionar
        ia_infos = ia_manipulations.filter_ia(ia_phone)
    except Exception as ex:
        print(f"ERROR in process: {ex}")