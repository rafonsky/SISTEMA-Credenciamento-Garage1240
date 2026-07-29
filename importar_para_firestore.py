"""
Importa participantes.json para a coleção por evento
"participantes/{evento_id}/lista" no Firestore, usando uma chave de
conta de serviço (admin).

Uso:
    pip install firebase-admin --break-system-packages
    python importar_para_firestore.py chave-admin.json participantes.json <evento_id>

O <evento_id> é o ID do documento do evento em "eventos" (visível no
painel administrativo, ex: na URL copiada de uma sala). Cada
participante vira um documento cujo ID é o próprio código do QR
(ex: "DOI-66C3EA6AF"), permitindo busca direta (sem query) na leitura.
"""

import sys
import json
import firebase_admin
from firebase_admin import credentials, firestore

def main(chave_path, participantes_path, evento_id):
    cred = credentials.Certificate(chave_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    with open(participantes_path, "r", encoding="utf-8") as f:
        participantes = json.load(f)

    lista_ref = db.collection("participantes").document(evento_id).collection("lista")

    batch = db.batch()
    count = 0
    for codigo, dados in participantes.items():
        ref = lista_ref.document(codigo)
        batch.set(ref, dados)
        count += 1
        # Firestore limita 500 operações por batch
        if count % 450 == 0:
            batch.commit()
            batch = db.batch()
            print(f"{count} importados...")

    batch.commit()
    print(f"Concluído: {count} participantes importados para participantes/{evento_id}/lista.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python importar_para_firestore.py chave-admin.json participantes.json <evento_id>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
