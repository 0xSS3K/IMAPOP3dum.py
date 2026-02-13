import imaplib
import poplib
import os
import argparse
import re
import shlex

# args
parser = argparse.ArgumentParser(description="IMAP & POP3 Fast dumper")
parser.add_argument("protocol", choices=["imap", "pop3"], help="Protocolo a usar: imap o pop3")
parser.add_argument("host", help="IP o Dominio del servidor")
parser.add_argument("user", help="Usuario")
parser.add_argument("password", help="Contraseña")
parser.add_argument("--port", type=int, help="Puerto (Opcional. Default: 993 IMAP-SSL, 995 POP3-SSL)")
parser.add_argument("--folder", help="Carpeta específica (Solo IMAP). Si se omite, descarga TODAS.")

args = parser.parse_args()

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def get_imap_folders(mail):
    folders = []
    try:
        status, response = mail.list()
        if status != 'OK':
            print("[!] Error listando carpetas.")
            return []

        print(f"[*] Escaneando estructura de carpetas...")
        for folder_info in response:
            if not folder_info: continue
            folder_str = folder_info.decode()
            
            try:
                parts = shlex.split(folder_str)
                
                folder_name = parts[-1]
                
                folders.append(folder_name)
            except ValueError:
                pass
                
        return folders
    except Exception as e:
        print(f"[!] Error obteniendo carpetas: {e}")
        return []

def dump_imap():
    port = args.port if args.port else 993
    print(f"\n[+] Iniciando conexión IMAP SSL a {args.host}:{port} como {args.user}")
    
    try:
        mail = imaplib.IMAP4_SSL(args.host, port)
        mail.login(args.user, args.password)
        
        target_folders = []
        if args.folder:
            target_folders = [args.folder]
        else:
            target_folders = get_imap_folders(mail)
            print(f"[*] Carpetas encontradas: {', '.join(target_folders)}")

        for folder in target_folders:
            print(f"\n>>> Procesando carpeta: {folder}")
            
            local_dir = os.path.join("dumped_emails", sanitize_filename(folder))
            os.makedirs(local_dir, exist_ok=True)
            
            status, data = mail.select(f'"{folder}"')
            if status != 'OK':
                print(f"[!] No se pudo acceder a {folder}. Saltando...")
                continue

            status, messages = mail.search(None, 'ALL')
            if not messages[0]:
                print(f"    [-] Carpeta vacía.")
                continue
                
            mail_ids = messages[0].split()
            print(f"    [*] Descargando {len(mail_ids)} correos...")

            for i in mail_ids:
                try:

                    res, msg_data = mail.fetch(i, '(RFC822)')
                    raw_email = msg_data[0][1]
                    
                    filename = os.path.join(local_dir, f"msg_{i.decode()}.eml")
                    with open(filename, 'wb') as f:
                        f.write(raw_email)
                except Exception as e:
                    print(f"    [!] Error bajando mensaje ID {i}: {e}")

        mail.close()
        mail.logout()
        print("\n[+] Descarga IMAP completada.")
        
    except Exception as e:
        print(f"[!] Error IMAP: {e}")

def dump_pop3():
    port = args.port if args.port else 995
    print(f"\n[+] Iniciando conexión POP3 SSL a {args.host}:{port} como {args.user}")
    
    try:
        mail = poplib.POP3_SSL(args.host, port)
        mail.user(args.user)
        mail.pass_(args.password)
        
        local_dir = os.path.join("dumped_emails", "POP3_INBOX")
        os.makedirs(local_dir, exist_ok=True)
        
        num_messages = len(mail.list()[1])
        print(f"[*] Se encontraron {num_messages} correos en el servidor.")
        
        for i in range(1, num_messages + 1):
            try:
                response, lines, octets = mail.retr(i)
                msg_content = b'\r\n'.join(lines)
                
                filename = os.path.join(local_dir, f"pop3_msg_{i}.eml")
                with open(filename, 'wb') as f:
                    f.write(msg_content)
                print(f"    [+] Guardado: {filename}")
            except Exception as e:
                print(f"    [!] Error bajando mensaje {i}: {e}")
            
        mail.quit()
        print("\n[+] Descarga POP3 completada.")
        
    except Exception as e:
        print(f"[!] Error POP3: {e}")

if __name__ == "__main__":
    if args.protocol == "imap":
        dump_imap()
    elif args.protocol == "pop3":
        dump_pop3()
