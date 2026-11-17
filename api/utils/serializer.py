from bson import ObjectId

def serializar_valor(valor):
    if isinstance(valor, ObjectId):
        return str(valor)
    if isinstance(valor, dict):
        return {k: serializar_valor(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [serializar_valor(v) for v in valor]
    return valor

def serializar_documento(documento):
    return serializar_valor(documento) if documento else documento

def serializar_lista(documentos):
    return [serializar_documento(d) for d in documentos]