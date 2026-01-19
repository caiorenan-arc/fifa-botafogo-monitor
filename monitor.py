from playwright.sync_api import sync_playwright
import requests
import os
import sys

TOKEN = "8289961206:AAEFIVO83YXHFXleEpo9_mpuyjJWGJW1yY0"
CHAT_ID = "116966232"

URL = "https://knowledge.fifa.com/registration-bans"
FLAG_FILE = "alerta_enviado.txt"

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def main():
    if os.path.exists(FLAG_FILE):
        print("Alerta já enviado. Encerrando.")
        sys.exit(0)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        page.fill('input[placeholder="Club"]', "Botafogo")
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        text = page.content()
        browser.close()

    if "We could not found what you where looking for" in text:
        msg = (
            "🚨 ALERTA FIFA 🚨\n\n"
            "A busca por *Botafogo* no campo CLUB retornou:\n"
            "'We could not found what you where looking for'\n\n"
            "✅ Isso indica que o Botafogo NÃO aparece mais na lista de transfer ban."
        )
        send_telegram(msg)
        open(FLAG_FILE, "w").write("enviado")

    else:
        print("Botafogo ainda consta na lista.")

if __name__ == "__main__":
    main()
