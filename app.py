from fastapi import FastAPI, Request
from analyzer import auditar_codigo, generar_reporte
import uvicorn

app = FastAPI(title="AUDITOR-BOT")

@app.get("/")
def inicio():
    return {"mensaje": "AUDITOR-BOT activo 🤖", "status": "listo para auditar"}

@app.post("/webhook")
async def webhook(request: Request):
    datos = await request.json()
    # GitHub manda esto cuando hay un PR
    accion = datos.get("action")
    pr = datos.get("pull_request", {})
    
    print(f"📩 Llegó un PR: {pr.get('title')} - Acción: {accion}")
    
    # SIMULACIÓN PARA LA DEMO - en la vida real aquí bajarías el código del PR
    codigo_ejemplo = """
    api_key = "sk-12345-secreto"
    password = "admin123"
    query = "SELECT * FROM users WHERE id = " + user_id
    # TODO: arreglar esto luego
    print("debug")
    """
    
    hallazgos = auditar_codigo(codigo_ejemplo, "main.py")
    reporte = generar_reporte(hallazgos)
    
    print(reporte)
    return {"reporte": reporte, "hallazgos": len(hallazgos)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)