"""
Cria um usuário (Master ou Admin) no sistema de check-in, usando a
chave de admin do Firebase. Cria a conta de autenticação E o
documento de papel/permissões no Firestore, na mesma operação.

Uso:
    python criar_usuario.py chave-admin.json

O script pergunta interativamente: e-mail, senha temporária, nome,
papel (master/admin) e, se for admin, quais eventos ele pode gerenciar.
"""

import sys
import firebase_admin
from firebase_admin import credentials, auth, firestore

def main(chave_path):
    cred = credentials.Certificate(chave_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    print("=== Criar usuário do sistema ===")
    email = input("E-mail: ").strip()
    senha = input("Senha temporária (mín. 6 caracteres): ").strip()
    nome = input("Nome: ").strip()

    papel = ""
    while papel not in ("master", "admin"):
        papel = input("Papel (master/admin): ").strip().lower()

    eventos_permitidos = []
    if papel == "admin":
        print("\nEventos existentes:")
        eventos = list(db.collection("eventos").stream())
        if not eventos:
            print("(nenhum evento cadastrado ainda — pode deixar em branco e editar depois)")
        else:
            for ev in eventos:
                print(f"  - {ev.id}: {ev.to_dict().get('nome', '')}")
        ids = input("IDs dos eventos permitidos, separados por vírgula (ou Enter p/ nenhum): ").strip()
        if ids:
            eventos_permitidos = [i.strip() for i in ids.split(",")]

    # Cria a conta de autenticação
    user = auth.create_user(email=email, password=senha, display_name=nome)

    # Cria o documento de papel/permissões
    db.collection("usuarios").document(user.uid).set({
        "nome": nome,
        "email": email,
        "papel": papel,
        "eventos_permitidos": eventos_permitidos,
    })

    print(f"\nUsuário criado com sucesso: {email} ({papel})")
    print(f"UID: {user.uid}")
    print("Peça pra essa pessoa trocar a senha no primeiro acesso.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python criar_usuario.py chave-admin.json")
        sys.exit(1)
    main(sys.argv[1])
