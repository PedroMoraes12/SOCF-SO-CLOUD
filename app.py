import os
import platform
import psutil
from flask import Flask, jsonify

APP = Flask(__name__)
APP.config['JSON_AS_ASCII'] = False

INTEGRANTES = [
    "Alan Filipe Reginato de França Santos",
    "Lucas Ferraz dos Santos",
    "Pedro Henrique Moraes"
]

def get_system_metrics():
    """Coleta as métricas do sistema conforme solicitado."""
    
    pid = os.getpid()
    process = psutil.Process(pid)
    
    memory_mb = process.memory_info().rss / (1024 * 1024)
    
    cpu_percent = process.cpu_percent(interval=0.1) 
    
    os_detected = f"{platform.system()} ({platform.release()})"
    
    return {
        "pid": pid,
        "memoria_usada_mb": round(memory_mb, 2),
        "uso_cpu_percent": cpu_percent,
        "sistema_operacional": os_detected
    }


@APP.route('/')
def home():
    """Página inicial que exibe todas as informações em texto."""
    metrics = get_system_metrics()
    
    nomes = "Nomes: " + " e ".join(INTEGRANTES)
    pid = f"PID: {metrics['pid']}"
    mem = f"Memória usada: {metrics['memoria_usada_mb']} MB"
    cpu = f"CPU: {metrics['uso_cpu_percent']}%"
    so = f"Sistema Operacional: {metrics['sistema_operacional']}"
    
    return f"<pre>{nomes}\n{pid}\n{mem}\n{cpu}\n{so}</pre>"

@APP.route('/info')
def info():
    """Rota /info: Mostra o nome dos integrantes em JSON [cite: 32, 48]"""
    return jsonify({"integrantes": INTEGRANTES})

@APP.route('/metricas')
def metricas():
    """Rota /metricas: Retorna todas as informações do Item 3 em JSON [cite: 33, 49]"""
    
    system_metrics = get_system_metrics()
    
    all_info = {
        "integrantes": INTEGRANTES,
        **system_metrics
    }
    
    return jsonify(all_info)

if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0', port=8080)
