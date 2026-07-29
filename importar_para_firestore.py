"""
Importa participantes.json para a coleção "congresso_participantes"
no Firestore, usando uma chave de conta de serviço (admin).

Uso:
    pip install firebase-admin --break-system-packages
    python importar_para_firestore.py chave-admin.json participantes.json

Cada participante vira um documento cujo ID é o próprio código do QR
(ex: "DOI-66C3EA6AF"), permitindo busca direta (sem query) na leitura.
"""

import sys
import json
import firebase_admin
from firebase_admin import credentials, firestore

def main(chave_path, participantes_path):
    cred = credentials.Certificate(chave_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    with open(participantes_path, "r", encoding="utf-8") as f:
        participantes = json.load(f)

    batch = db.batch()
    count = 0
    for codigo, dados in participantes.items():
        ref = db.collection("congresso_participantes").document(codigo)
        batch.set(ref, dados)
        count += 1
        # Firestore limita 500 operações por batch
        if count % 450 == 0:
            batch.commit()
            batch = db.batch()
            print(f"{count} importados...")

    batch.commit()
    print(f"Concluído: {count} participantes importados para congresso_participantes.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python importar_para_firestore.py chave-admin.json participantes.json")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
