# SIGNAL-CRYPTO

> ⚠️ **Advertencia de riesgo**  
> Este proyecto es solo para análisis y paper trading. **No garantiza ganancias**. El trading de criptomonedas implica alto riesgo.

## Requisitos

- Python 3.10+
- Git
- Acceso a Binance global (algunas regiones están restringidas)

## Instalación (desde cero)

```bash
git clone https://github.com/Rjriva/signal-crypto.git
cd signal-crypto
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

1. Crea tu archivo `.env` con las variables de Telegram:

```bash
TELEGRAM_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id
```

2. Copia el archivo de configuración de ejemplo y ajústalo:

```bash
cp config.example.yaml config.yaml
```

3. En `config.yaml`, para escanear **todos los futuros USDT** deja:

```yaml
scanner:
  use_all_usdt_futures: true
  timeframes: ["15m"]
```

## Ejecutar manualmente

```bash
python scripts/run_scan.py
```

## Ejecutar con systemd (recomendado)

1. Copia los archivos de systemd:

```bash
sudo cp systemd/signal-crypto.service /etc/systemd/system/
sudo cp systemd/signal-crypto.timer /etc/systemd/system/
```

2. Ajusta las rutas en `systemd/signal-crypto.service` si tu instalación no está en `/root/signal-crypto` o si tu virtualenv está en otra ruta.

3. Activa el timer:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now signal-crypto.timer
sudo systemctl status signal-crypto.timer
```

4. Ver logs del servicio:

```bash
journalctl -u signal-crypto.service -f
```

## Notas

- El escaneo de **todos los futuros USDT** puede tardar más y consumir más recursos.
- Si Binance está bloqueado en tu región, el scanner fallará.