# IMAPOP3dumpy
Un script en Python ligero y robusto diseñado para la descarga masiva y automatizada de correos electrónicos desde servidores IMAP y POP3.

Esta herramienta fue creada específicamente para agilizar la fase de exfiltración en entornos de CTF y pruebas de penetración, resolviendo la necesidad de enumerar manualmente carpetas o adivinar UIDs de mensajes. Permite obtener el contenido completo de los buzones sin dependencias externas.

### Características Principales
- Soporte dual para protocolos IMAP y POP3 con conexión SSL/TLS por defecto.
- Auto-descubrimiento inteligente de carpetas IMAP: lista y descarga recursivamente el contenido de todos los buzones disponibles (INBOX, Sent, Trash, carpetas personalizadas).
- Implementa shlex para un parsing robusto de las respuestas del servidor, manejando correctamente nombres de carpetas con espacios o formatos de comillas no estándar.
- Organización local automática: crea una estructura de directorios en tu máquina que replica la del servidor, guardando cada correo como un archivo .eml individual.
- No requiere instalación de librerías externas (funciona con las librerías nativas de Python 3).

### Requisitos
- Python 3

### Uso
- El script no requiere instalación. Simplemente descárgalo o crea el archivo.
- Ejecuta la herramienta especificando el protocolo, el host (IP/Dominio) y las credenciales:

```bash
python3 IMAPOP3dump.py <PROTOCOLO> <HOST> <USUARIO> <CONTRASEÑA> [OPCIONES]
```

### Ejemplo
Modo IMAP (Auto-descubrimiento de carpetas):
```bash
python3 IMAPOP3dump.py imap 10.129.4.178 robin robin
```
Modo POP3 (Descarga de bandeja de entrada):
```bash
python3 IMAPOP3dump.py pop3 10.129.4.178 robin robin --port 995
```

### Salida de Ejemplo
```plaintext
[+] Iniciando conexión IMAP SSL a 10.129.4.178:993 como robin
[*] Escaneando estructura de carpetas (Modo Robusto)...
[*] Carpetas encontradas: INBOX, DEV.DEPARTMENT.INT, Sent

>>> Procesando carpeta: INBOX
    [-] Carpeta vacía.

>>> Procesando carpeta: DEV.DEPARTMENT.INT
    [*] Descargando 2 correos...
    [+] Guardado: dumped_emails/DEV.DEPARTMENT.INT/msg_1.eml
    [+] Guardado: dumped_emails/DEV.DEPARTMENT.INT/msg_2.eml

>>> Procesando carpeta: Sent
    [-] Carpeta vacía.

[+] Descarga IMAP completada.
```
