# Pristracker

Pristrackeren følger prisene på utstyret du vil kjøpe, og gir beskjed når noe blir billig nok. Den består av tre deler:

1. **Automatisk prissjekk av nettbutikker** (dette skriptet). Den kjører to ganger om dagen i GitHub Actions.
2. **Prisjakt-prisvarsel**, som du setter opp selv i appen eller på nettsiden.
3. **Lagrede søk på FINN med varsling**, som du også setter opp selv.

FINN og Prisjakt forbyr automatisk innsamling i vilkårene sine. Derfor henter skriptet aldri noe derfra, og du bruker i stedet de gratis varslene deres. De er raskere enn et skript uansett, fordi de varsler med en gang noe endrer seg.

## 1. Automatisk prissjekk (GitHub Actions)

- Kjører kl. 06.17 og 16.17 hver dag. Du kan også starte den manuelt: **Actions → Pristracker → Run workflow**.
- Henter prisen fra produktsidene i `watchlist.json`. Den leser de strukturerte prisdataene (schema.org) som butikkene selv publiserer.
- Følger butikkens `robots.txt` og venter 3 sekunder mellom hvert kall. Den prøver ikke å komme rundt blokkering.
- Lagrer historikken i `data/priser.csv` og skriver en oversikt i **`RAPPORT.md`**.
- **Varsler** ved målpris, prisfall på mer enn 3 % eller ny laveste pris. Varselet blir et GitHub-issue, så du får e-post eller push i GitHub-appen. Sjekk at varslinger er slått på under *Watch → All activity* eller *Custom → Issues* på repoet.

### Legge til en vare

Åpne `watchlist.json` (du kan redigere direkte på github.com) og legg til:

```json
{
  "navn": "Staver Leki Helicon Lite",
  "kategori": "Topptur",
  "prioritet": 1,
  "maalpris": 900,
  "notat": "valgfritt",
  "kilder": [
    {"butikk": "Fjellsport", "url": "https://www.fjellsport.no/..."},
    {"butikk": "XXL", "url": "https://www.xxl.no/..."}
  ]
}
```

- Lim inn **produktsiden**, ikke en søkeside.
- Flere butikker per vare er lurt, fordi rapporten viser den billigste.
- Priser i euro og andre valutaer regnes om med kursene i `innstillinger`. Utenlandske priser er uten norsk mva og frakt, så legg til ca. 25 %.
- Gir en side «fant ikke pris», publiserer ikke butikken strukturerte prisdata. Bruk en annen butikk, eller følg varen med Prisjakt-varsel.

### Kjøre lokalt

```bash
python3 pristracker/tracker.py
```

Skriptet trenger bare Python 3.9 eller nyere, uten ekstra pakker.

## 2. Prisjakt-prisvarsel (anbefalt for alt)

1. Lag en gratis konto på prisjakt.no, eller logg inn i appen.
2. Åpne produktet og trykk **«Prisvarsel»** / bjellen.
3. Sett ønsket pris. Du får e-post eller push når en butikk går under den.

| Vare | Prisjakt-produkt | Foreslått varsel |
|---|---|---|
| Sweet Protection Ascender MIPS | prisjakt.no/product.php?p=5191960 | 1 500 kr |
| Salomon MTN Lab | prisjakt.no/product.php?p=3349204 | 1 700 kr |
| Black Diamond Traverse (teleskopstav) | prisjakt.no/product.php?p=276095 | 900 kr |
| Petzl Actik Core (rødt lys) | prisjakt.no/product.php?p=16164158 | 650 kr |
| Arc'teryx Beta AR (herre) | prisjakt.no/product.php?p=674130 | 4 000 kr |
| Arc'teryx Rush (herre) | prisjakt.no/product.php?p=967889 | 6 000 kr |
| Norrøna lofoten GTX Pro (herre) | prisjakt.no/product.php?p=17332876 | 6 500 kr |

Prisjakt viser laveste pris på tvers av størrelser og farger. Sjekk alltid at **din størrelse** finnes til den prisen, og se på prishistorikken før Black Friday.

## 3. FINN: lagrede søk med varsling

1. Søk på FINN Torget, for eksempel `gore-tex pro jakke`.
2. Filtrer på pris, og på størrelse L der det finnes.
3. Trykk **«Lagre søk»** og slå på varsling (push eller e-post).

| Søk | Makspris | Tips |
|---|---|---|
| `arc'teryx rush` / `arcteryx beta ar` / `arcteryx alpha` | 4 000 kr | Str. L |
| `lofoten gore-tex pro` / `trollveggen` | 4 000 kr | Herre L. Prøv også XL, fordi Lofoten er smal |
| `gore-tex pro jakke` | 3 800 kr | Bred fangst. Tittelen sier ofte størrelsen |
| `sweet protection ascender` | 1 500 kr | Str. M/L |
| `teleskopstaver topptur` / `black diamond traverse` | 700 kr | |
| `skredsekk` | 3 500 kr | Lav prioritet. Hopp over utleieannonser |

Bruk **«Fiks ferdig»**. Da har du 24 timer til å se over varen og få pengene tilbake hvis noe er galt.

## Kjøpsregler (fra Black Week-rapporten)

- Den reelle snittrabatten på Black Friday var bare 5,9 % i 2024, og omtrent 1 av 6–7 tilbud var en lurepris. Sammenlign med «Lavest sett» i rapporten.
- Førpris skal være den laveste prisen de siste 30 dagene. Medlemspriser teller også.
- Åpent kjøp og angrerett virker som prisgaranti: kjøp når prisen er god, og returner hvis den blir lavere. Fjellsport gir 100 dager, og netthandel gir alltid 14 dagers angrerett.
- Anton Sport-bonus (1 462 kr, gyldig til november 2027): bruk den hos Anton, Sportsnett eller Milslukern på verkstedtjenester eller varer som er nede på markedspris.
