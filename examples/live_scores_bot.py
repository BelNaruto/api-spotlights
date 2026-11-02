"""Live scores alerts for NBA, NFL and MLB. Uses the Sports Information API on RapidAPI.
Optional: set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID to also send alerts to Telegram."""
import os, sys, time
import requests

HOST = "sports-information.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def today(leagues):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/today", headers=HEADERS,
                         params={"leagues": leagues}, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def notify(text):
    print(text, flush=True)
    token, chat = os.environ.get("TELEGRAM_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      data={"chat_id": chat, "text": text}, timeout=30)


def line(ev):
    away, home = ev["away"], ev["home"]
    return f"{away['team']['abbreviation']} {away['score']} - {home['score']} {home['team']['abbreviation']}"


def main(leagues="nba,nfl,mlb", every=60):
    seen = {}  # event id to (state, score text)
    while True:
        for lg in today(leagues):
            for ev in lg["events"]:
                state, score = ev["status"]["state"], line(ev)
                old = seen.get(ev["id"])
                if old is None and state == "pre":
                    pass  # baseline only
                elif old != (state, score):
                    if state == "in":
                        notify(f"LIVE {lg['name']}: {score}  ({ev['status']['shortDetail']})")
                    elif state == "post":
                        notify(f"FINAL {lg['name']}: {score}")
                seen[ev["id"]] = (state, score)
        time.sleep(every)


if __name__ == "__main__":
    main(sys.argv[1] if sys.argv[1:] else "nba,nfl,mlb")
