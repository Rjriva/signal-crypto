# CRYPTO-SIGNAL-VOLUME-LAB

> ⚠️ **Advertencia de riesgo**  
> Este proyecto es solo para análisis y paper trading. **No garantiza ganancias**. El trading de criptomonedas implica alto riesgo.

## Instalación

```bash
git clone <repo>
cd crypto-signal-volume-lab
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

1. Copia `.env.example` → `.env`
2. Copia `config.example.yaml` → `config.yaml`

## Ejecutar

```bash
python scripts/run_scan.py
python scripts/run_backtest.py
uvicorn app.main:app --reload
```