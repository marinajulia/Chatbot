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
        
        if not ia_infos:
            raise(Exception(f"No IA found for phone number: {ia_phone}"))
        
        if ia_infos.status != True:
            raise(Exception(f"IA {ia_infos.name} is inactive. Skipping processing."))
        
        #Extrair conteudo da mensagem
        message_id = data["data"]["key"]["id"]
        message_type = data["data"]["messageType"]
        message_content = processar_mensagem(data, ia_name, message_id, message_type, ia_infos)

        if not message_content:
            raise(Exception(f"Tipo de mensagem não foi possível de processar: {message_type}"))
        
        # extraindo informações do lead
        lead_name = data["data"]["pushName"]
        lead_phone = data["data"]["key"]["remoteJid"].split("@")[0]

        print(f"Lead info - Name: {lead_name}, Phone: {lead_phone}, Message: {message_content}", flush=True)

    except Exception as ex:
        print(f"ERROR in process: {ex}", flush=True)

def processar_mensagem(data:dict, instance:str, message_id, message_type:str, ia_infos: object) -> str :

    if message_type == "conversation":
        return data["data"]["message"]["conversation"]
    
    elif message_type == "extendedTextMessage":
        return data["data"]["message"]["extendedTextMessage"]["text"]
    
    elif message_type == "imageMessage":
        print("Imagem detectada!")
        #return processar_imagem(instance, message_id, ia_infos)
        return "Mensagem de imagem"
    
    elif message_type == "audioMessage":
        print("Audio identificado!")
        #return processar_audio(instance, message_id, ia_infos)
        return "Mensagem de audio"
    
    elif message_type == "documentWithCaptionMessage":
        print("Documento identificado!")
        type_file = data.get("data").get("message").get("documentWithCaptionMessage").get("message").get("documentMessage").get("mimetype").split("/")[1]
        #return processar_documento(instance, message_id, type_file, ia_infos), type_file
        return "Mensagem de documento"

    else:
        print(f"Tipo de mensagem não identificada: {message_type} retornando ... ")
        return ""
