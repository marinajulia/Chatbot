import random
import time

from app.database.manipulations import ia_manipulations, lead_manipulations
from app.service.queue_manager import get_phone_lock
from app.service.llm_response import IAresponse
from app.service.quebra_mensagens import *


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

        lock = get_phone_lock(lead_phone)

        with lock:
            message_atual_lead = {
                "role": "user",
                "name": lead_name,
                "content": message_content
            }

            lead_db = lead_manipulations.filter_lead(lead_phone, message_atual_lead)

            if not lead_db:
                lead_db = lead_manipulations.new_lead(ia_infos.id, lead_name, lead_phone, [message_atual_lead])


            # Gerar resposta da LLM:
            
            historico = lead_db.message
            resume_lead = lead_db.resume
            api_key = ia_infos.ia_config.credentials.get("api_key")
            ia_model = ia_infos.ia_config.credentials.get("ai_model", "")
            system_prompt = ia_infos.active_prompt

            if not system_prompt:
                raise(Exception("Nenhum prompt cadastrado"))

            llm = IAresponse(api_key, ia_model, system_prompt.prompt_text, resume_lead)
            response_lead = llm.generate_response(message_content, historico)

            if not response_lead:
                raise(Exception("Nenhuma resposta gerada pela IA"))
            
            #tratar mensagem da IA
            list_message_to_lead = quebrar_mensagens(response_lead)

            if not list_message_to_lead:
                list_message_to_lead = [response_lead] 

            # Enviar resposta para o lead

            for msg in list_message_to_lead:
                delay = calculate_typing_delay(msg)
                print(f"Simulating typing delay of {delay:.2f} seconds for message: {msg}", flush=True)
                print(f"Enviando mensagem para o lead {lead_phone}: {msg}", flush=True)


            resumo = None
            total_interacoes = 0
            ultimo_role = 0

            for mensagem in historico:
                if mensagem["role"] != ultimo_role:
                    total_interacoes += 1
                    ultimo_role = 0
                
            print(f"Total de interações com o lead {lead_phone}: {total_interacoes}", flush=True)


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
