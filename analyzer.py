import re

# 1. SECRETOS EXPUESTOS
PATRONES = [
    ("🔑 API Key expuesta", r'api_key\s*=\s*["\'][^"\']+["\']', "Usa variables de entorno: os.getenv('API_KEY')"),
    ("🔑 Password expuesta", r'password\s*=\s*["\'][^"\']+["\']', "Nunca dejes passwords en el código. Usa .env"),
    ("🔑 Token de GitHub", r'ghp_[a-zA-Z0-9]{20,}', "Regenera tu token, ya está comprometido"),
    ("💉 SQL Injection", r'execute\(.*\+.*\)|query.*\+.*user', "Usa queries parametrizadas: cursor.execute('... %s', (id,))"),
    ("⚠️ TODO olvidado", r'TODO|FIXME|XXX|HACK', "Resuelve esto antes de subir a producción"),
    ("🐢 Bucle lento", r'for.*:\s*\n.*for.*:', "Tienes un bucle dentro de otro bucle, esto es O(n²) - muy lento"),
    ("🖨️ Print olvidado", r'print\(|console\.log', "Quita los prints de debug antes de producción"),
]

def auditar_codigo(codigo: str, nombre_archivo: str):
    hallazgos = []
    for titulo, patron, sugerencia in PATRONES:
        for match in re.finditer(patron, codigo, re.IGNORECASE | re.MULTILINE):
            linea = codigo[:match.start()].count('\n') + 1
            hallazgos.append({
                "archivo": nombre_archivo,
                "linea": linea,
                "titulo": titulo,
                "codigo": match.group(0)[:80],
                "sugerencia": sugerencia
            })
    return hallazgos

def generar_reporte(hallazgos):
    if not hallazgos:
        return "✅ **AUDITOR-BOT: Todo limpio!**\n\nNo encontré vulnerabilidades. Puedes hacer merge."
    
    reporte = f"🚨 **AUDITOR-BOT encontró {len(hallazgos)} problema(s)**\n\n"
    for h in hallazgos:
        reporte += f"### {h['titulo']} - {h['archivo']}:{h['linea']}\n"
        reporte += f"```python\n{h['codigo']}\n```\n"
        reporte += f"**Sugerencia:** {h['sugerencia']}\n\n"
    reporte += "---\n*Revisado automáticamente por AUDITOR-BOT 🤖*"
    return reporte