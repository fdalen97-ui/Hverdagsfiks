#!/usr/bin/env python3
"""Pristracker: følger prisen på utvalgte produktsider i nettbutikker og varsler når noe blir billig.

Kjør:   python3 pristracker/tracker.py
Konfig: pristracker/watchlist.json
Utdata: pristracker/RAPPORT.md, pristracker/data/priser.csv og pristracker/data/varsler.md (bare når det er varsler)

Regler skriptet følger:
- Henter bare produktsider du selv har lagt inn, én om gangen, med pause mellom kall.
- Sjekker robots.txt for hver butikk og hopper over sider butikken ikke tillater.
- Henter aldri fra FINN eller Prisjakt. Begge forbyr automatisk innsamling i vilkårene sine.
  Bruk deres egne varsler i stedet (se README.md).
- Omgår ikke blokkering. Svarer en side med 403/429, logges det og siden hoppes over denne runden.

Bare standardbiblioteket brukes, så skriptet kjører uten installasjon (også i GitHub Actions).
"""
from __future__ import annotations

import csv
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from pathlib import Path

ROT = Path(__file__).resolve().parent
DATA = ROT / "data"
WATCHLIST = ROT / "watchlist.json"
PRISER_CSV = DATA / "priser.csv"
VARSLER = DATA / "varsler.md"
RAPPORT = ROT / "RAPPORT.md"

UA = "Mozilla/5.0 (compatible; Hverdagsfiks-pristracker/1.0; personlig prisovervaking)"
UA_NAVN = "Hverdagsfiks-pristracker"
CSV_FELT = ["tid", "vare", "butikk", "url", "pris", "status", "tittel"]
FORBUDTE_DOMENER = ("finn.no", "prisjakt.no", "prisjagt.dk", "pricespy", "hintaopas")


# --------------------------------------------------------------------------- nett
def hent(url: str, timeout: int = 30) -> tuple[int, str]:
    """Returnerer (statuskode, tekst). Statuskode 0 betyr nettverksfeil."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "nb-NO,nb;q=0.9,no;q=0.8,en;q=0.5",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


_robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}


def tillatt(url: str) -> bool:
    """Sjekker butikkens robots.txt. Mangler filen, regnes alt som tillatt."""
    p = urllib.parse.urlparse(url)
    base = f"{p.scheme}://{p.netloc}"
    if base not in _robots:
        kode, tekst = hent(base + "/robots.txt", timeout=20)
        if kode == 200 and tekst:
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(tekst.splitlines())
            _robots[base] = rp
        else:
            _robots[base] = None
    rp = _robots[base]
    return True if rp is None else rp.can_fetch(UA_NAVN, url)


# --------------------------------------------------------------------------- parsing
def _tall(v) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("\xa0", "").replace(" ", "")
    s = re.sub(r"[^\d,.]", "", s)
    if not s:
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _ld_objekter(side: str):
    for blokk in re.findall(r"<script[^>]*application/ld\+json[^>]*>(.*?)</script>", side, re.S | re.I):
        try:
            data = json.loads(blokk.strip())
        except Exception:
            continue
        stakk = [data]
        while stakk:
            o = stakk.pop()
            if isinstance(o, list):
                stakk.extend(o)
            elif isinstance(o, dict):
                yield o
                for k in ("@graph", "itemListElement", "item", "mainEntity", "hasVariant"):
                    if k in o:
                        stakk.append(o[k])


def _er_produkt(o: dict) -> bool:
    t = o.get("@type")
    t = t if isinstance(t, list) else [t]
    return any(str(x).lower() in ("product", "productgroup", "individualproduct") for x in t)


def pris_fra_ld(side: str) -> dict | None:
    """Laveste pris i schema.org Product/Offer/AggregateOffer (strukturerte data butikken publiserer)."""
    beste = None
    for o in _ld_objekter(side):
        if not _er_produkt(o):
            continue
        tilbud = o.get("offers") or []
        tilbud = tilbud if isinstance(tilbud, list) else [tilbud]
        for t in tilbud:
            if not isinstance(t, dict):
                continue
            p = _tall(t.get("lowPrice")) or _tall(t.get("price"))
            if p is None:
                ps = t.get("priceSpecification")
                if isinstance(ps, dict):
                    p = _tall(ps.get("price"))
            if p is None or p <= 0:
                continue
            valuta = str(t.get("priceCurrency", "NOK")).upper()
            tilgj = str(t.get("availability", "")).rsplit("/", 1)[-1]
            kand = {"pris": p, "valuta": valuta, "tittel": html.unescape(str(o.get("name", ""))).strip(),
                    "tilgjengelig": tilgj}
            if beste is None or (tilgj not in ("OutOfStock", "SoldOut") and p < beste["pris"]):
                beste = kand
    return beste


def pris_fra_meta(side: str) -> float | None:
    for mønster in (
        r'(?:property|name)="(?:product:price:amount|og:price:amount)"[^>]*content="([^"]+)"',
        r'content="([^"]+)"[^>]*(?:property|name)="(?:product:price:amount|og:price:amount)"',
        r'itemprop="price"[^>]*content="([^"]+)"',
    ):
        m = re.search(mønster, side, re.I)
        if m:
            p = _tall(m.group(1))
            if p:
                return p
    return None


def sidetittel(side: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", side, re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()[:120] if m else ""


# --------------------------------------------------------------------------- kilder
def sjekk_side(kilde: dict, kurs: dict) -> dict:
    url = kilde["url"]
    butikk = kilde.get("butikk") or urllib.parse.urlparse(url).netloc.replace("www.", "")
    res = {"url": url, "butikk": butikk, "pris": None, "status": "", "tittel": ""}
    vert = urllib.parse.urlparse(url).netloc.lower()
    if any(d in vert for d in FORBUDTE_DOMENER):
        res["status"] = "hoppet over: nettstedet forbyr automatisk innsamling (bruk deres egne varsler)"
        return res
    if not tillatt(url):
        res["status"] = "hoppet over: ikke tillatt i butikkens robots.txt"
        return res
    kode, side = hent(url)
    if kode != 200 or not side:
        res["status"] = {0: "nettverksfeil", 403: "blokkert (403)", 404: "fjernet/ikke funnet (404)",
                         410: "fjernet (410)", 429: "for mange kall (429)"}.get(kode, f"HTTP {kode}")
        return res
    ld = pris_fra_ld(side)
    if ld:
        faktor = 1.0 if ld["valuta"] == "NOK" else kurs.get(ld["valuta"])
        if faktor is None:
            res.update(status=f"ukjent valuta {ld['valuta']}", tittel=ld["tittel"])
            return res
        res.update(pris=round(ld["pris"] * faktor), tittel=ld["tittel"])
        if ld["valuta"] != "NOK":
            res["butikk"] += f" ({ld['pris']:.0f} {ld['valuta']})"
        res["status"] = "utsolgt" if ld["tilgjengelig"] in ("OutOfStock", "SoldOut", "Discontinued") else "ok"
        return res
    p = pris_fra_meta(side)
    res.update(pris=p, status="ok" if p else "fant ikke pris på siden", tittel=sidetittel(side))
    return res


# --------------------------------------------------------------------------- lagring
def les_historikk() -> list[dict]:
    if not PRISER_CSV.exists():
        return []
    with PRISER_CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def skriv_rader(rader: list[dict]):
    ny = not PRISER_CSV.exists()
    with PRISER_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FELT)
        if ny:
            w.writeheader()
        for r in rader:
            w.writerow({k: r.get(k, "") for k in CSV_FELT})


def kr(p) -> str:
    if p in (None, ""):
        return "–"
    return f"{float(p):,.0f}".replace(",", " ") + " kr"


def norsk_tid() -> str:
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("Europe/Oslo")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return dt.datetime.now(dt.timezone(dt.timedelta(hours=1))).strftime("%Y-%m-%d %H:%M")


# --------------------------------------------------------------------------- hovedløp
def main() -> int:
    cfg = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    innst = cfg.get("innstillinger", {})
    pause = float(innst.get("pause_sek", 3))
    kurs = {k.upper(): float(v) for k, v in innst.get("valutakurs_til_nok", {}).items()}
    DATA.mkdir(exist_ok=True)
    nå = norsk_tid()

    laveste: dict[str, tuple[float, str]] = {}
    siste: dict[tuple[str, str], float] = {}
    for r in les_historikk():
        p = _tall(r.get("pris"))
        if p is None:
            continue
        v = r["vare"]
        if v not in laveste or p < laveste[v][0]:
            laveste[v] = (p, r["tid"][:10])
        siste[(v, r["url"])] = p

    nye_rader, feil, varsler, tabell = [], [], [], []
    for vare in cfg.get("varer", []):
        navn, mål = vare["navn"], vare.get("maalpris")
        resultater = []
        for kilde in vare.get("kilder", []):
            r = sjekk_side(kilde, kurs)
            time.sleep(pause)
            resultater.append(r)
            nye_rader.append({"tid": nå, "vare": navn, "butikk": r["butikk"], "url": r["url"],
                              "pris": r["pris"] if r["pris"] is not None else "", "status": r["status"],
                              "tittel": r["tittel"]})
            if r["pris"] is None:
                feil.append(f"{navn}: {r['butikk']} – {r['status']} ({r['url']})")
            forrige = siste.get((navn, r["url"]))
            if r["pris"] is not None and forrige and r["pris"] < forrige * 0.97:
                varsler.append(f"📉 **{navn}** falt fra {kr(forrige)} til **{kr(r['pris'])}** hos {r['butikk']} – {r['url']}")
        gyldige = [r for r in resultater if r["pris"] is not None and r["status"] == "ok"]
        beste = min(gyldige, key=lambda r: r["pris"]) if gyldige else None
        tidl = laveste.get(navn)
        if beste:
            if mål and beste["pris"] <= mål:
                varsler.append(f"🎯 **{navn}** er på/under målpris {kr(mål)}: **{kr(beste['pris'])}** hos {beste['butikk']} – {beste['url']}")
            if tidl and beste["pris"] < tidl[0]:
                varsler.append(f"🏆 **{navn}**: ny laveste pris {kr(beste['pris'])} (før: {kr(tidl[0])}, {tidl[1]})")
        kandidater = [x for x in (beste["pris"] if beste else None, tidl[0] if tidl else None) if x is not None]
        lavest = min(kandidater) if kandidater else None
        lavest_dato = nå[:10] if beste and (not tidl or beste["pris"] < tidl[0]) else (tidl[1] if tidl else "")
        tabell.append({"prioritet": vare.get("prioritet", 9), "kategori": vare.get("kategori", ""), "navn": navn,
                       "naa": beste["pris"] if beste else None, "hvor": beste["butikk"] if beste else "–",
                       "url": beste["url"] if beste else "", "maal": mål, "lavest": lavest,
                       "lavest_dato": lavest_dato, "notat": vare.get("notat", "")})

    skriv_rader(nye_rader)

    tabell.sort(key=lambda x: (x["prioritet"], x["kategori"], x["naa"] or 1e9))
    L = ["# Prisrapport", "", f"Sist oppdatert: **{nå}**. Oppdateres automatisk av GitHub Actions.", "",
         "## Varsler denne runden", ""]
    L += [f"- {v}" for v in varsler] or ["- Ingen nye varsler."]
    L += ["", "## Beste pris per vare", "",
          "| Pri | Kategori | Vare | Beste pris nå | Hvor | Målpris | Lavest sett | Under mål? | Notat |",
          "|---|---|---|---|---|---|---|---|---|"]
    for t in tabell:
        under = "✅" if t["naa"] is not None and t["maal"] and t["naa"] <= t["maal"] else ""
        hvor = f"[{t['hvor']}]({t['url']})" if t["url"] else t["hvor"]
        dato = f" ({t['lavest_dato']})" if t["lavest_dato"] else ""
        L.append(f"| {t['prioritet']} | {t['kategori']} | {t['navn']} | **{kr(t['naa'])}** | {hvor} | {kr(t['maal'])} | "
                 f"{kr(t['lavest'])}{dato} | {under} | {t['notat']} |")
    L += ["", "## Sider som ikke ga pris denne runden", ""]
    L += [f"- {f}" for f in feil] or ["- Alle sider svarte."]
    L += ["", "## Husk før du kjøper", "",
          "- Sammenlign med «Lavest sett». Black Friday-tilbud er ofte ikke ekte (snitt reell rabatt 5,9 % i 2024).",
          "- Førpris skal være laveste pris siste 30 dager. Ser det for godt ut, sjekk prishistorikken på Prisjakt manuelt.",
          "- Prisen gjelder ofte laveste variant. Sjekk at din størrelse finnes til den prisen.",
          "- Bruk åpent kjøp/angrerett (14 dager på nett) som prisgaranti: kjøp, og returner hvis det blir billigere.",
          "- FINN og Prisjakt følges med deres egne varsler, se README.md.", ""]
    RAPPORT.write_text("\n".join(L), encoding="utf-8")

    if varsler:
        VARSLER.write_text(f"Prisvarsler {nå}\n\n" + "\n".join(f"- {v}" for v in varsler) +
                           "\n\nSe hele rapporten i pristracker/RAPPORT.md\n", encoding="utf-8")
    elif VARSLER.exists():
        VARSLER.unlink()

    print(f"{len(nye_rader)} sider sjekket, {len(varsler)} varsler, {len(feil)} uten pris")
    for v in varsler:
        print("VARSEL:", v)
    for f in feil:
        print("FEIL:", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
