"""
Converte o relatório exportado da Doity (xlsx) em JSON pronto para
importar na coleção "congresso_participantes" do Firestore.

Uso:
    python importar_participantes.py relatorio.xlsx participantes.json

Cada participante vira um documento cuja CHAVE (id do documento) é o
próprio código do QR (ex: "DOI-66C3EA6AF"), então na leitura do QR
o check-in busca direto pelo ID, sem precisar de query.
"""

import sys
import json
import pandas as pd

def main(xlsx_path, out_path):
    df = pd.read_excel(xlsx_path)

    participantes = {}
    for _, row in df.iterrows():
        codigo = str(row["Nº Inscrição"]).strip()
        if not codigo or codigo == "nan":
            continue

        participantes[codigo] = {
            "nome": str(row.get("Nome", "")).strip(),
            "nome_cracha": str(row.get("Nome para Crachá", "")).strip(),
            "orgao": str(row.get("Órgão", "")).strip(),
            "cargo": str(row.get("Cargo/Função", "")).strip(),
            "estado": str(row.get("Estado", "")).strip(),
            "email": str(row.get("E-mail", "")).strip(),
            "situacao_inscricao": str(row.get("Situação da inscrição", "")).strip(),
        }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(participantes, f, ensure_ascii=False, indent=2)

    print(f"{len(participantes)} participantes exportados para {out_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python importar_participantes.py relatorio.xlsx participantes.json")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
