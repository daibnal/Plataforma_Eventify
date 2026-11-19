CAMPOS_OBJECTID = ("_id", "usuario_id", "evento_id")

##Convierte a texto los ObjectId de un documento. Solo convierte los
##campos que el doc tiene, sirviendo para usuarios y eventos y para ordenes_compra
##y review_evaluaciones (que tiene id, usuario id y evento id)
def serializar_documento(documento):
    if documento:
        for campo in CAMPOS_OBJECTID:
            if campo in documento:
                documento[campo] = str(documento[campo])

    return documento

## Aplica serializar_documento a cada documento en un find()
def serializar_lista(documentos):
    """Aplica serializar_documento a cada documento de un find()."""
    return [
        serializar_documento(documento)
        for documento in documentos
    ]