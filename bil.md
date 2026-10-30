# Bil: Toyota Aygo 1.0 (2008, motor 1KR-FE, 3-sylinder)

Sist oppdatert: 2026-10-30

## Status

| Sak | Status |
|---|---|
| Feilkode P0301 (feiltenning sylinder 1) | Lest 29.10 med Sparco OBD2-leser. Ikke utbedret |
| Batteritest | Min. 7,78 V under start, starttid 2,5 s, ladespenning 14,0 V. Batteriet er fra 2026, så årsak er trolig småkjøring (aldri fulladet), poler/jording eller startmotor |
| Forbremser | Deler bestilt hos Thansen (ordre 116520562, 1 909,30 kr), klar til henting Vitaminveien 3, Storo |
| Bremseklosser | Gjort tidligere |

## Feilsøking P0301

Rekkefølge (billigst først):

1. **Lad batteriet fullt** med vedlikeholdslader, puss poler/klemmer/jording. Slett koden. Kommer den bare ved kaldstart, kan lav spenning være hele årsaken.
2. **Bytteprøve:** flytt tennspole 1 til sylinder 2. Slett kode, kjør noen dager.
   - Kode flytter til P0302 → tennspole defekt. Bytt (gjerne alle tre).
   - Fortsatt P0301 → sjekk/bytt tennplugg 1 (bytt alle tre).
   - Fortsatt P0301 etter ny plugg og byttet spole → injektor 1 eller ledningsnett. Verksted.
3. Les «Freeze frame» i leseren: turtall/temperatur/last da feilen kom.
4. Velg **Toyota** under «Vehicle manufacturer» i leseren for merkespesifikke koder (ABS, airbag).

Sylinder 1 er i enden mot registerkjedet (motsatt side av girkassen). Spolene sitter oppå motoren, én 10 mm-bolt og én kontakt hver.

## Batteri og lading

- Mye småkjøring → batteriet blir aldri fulladet. Lad med smartlader (CTEK MXS 5.0 / Noco Genius 5) 12–24 t første gang, deretter hver 2.–4. uke om vinteren.
- Rød på +, svart på − eller jordpunkt. Koble fra i motsatt rekkefølge.
- Friskt batteri: over ca. 9,6 V under start. Under 9 V etter fullading og pussede poler → reklamer batteriet eller sjekk startmotor.
- Mål helst med multimeter rett på polene under start; OBD-leseren måler gjennom ledningsnettet.

## Forbremser: fremgangsmåte

Bestilte deler: skiver 247 × 20 mm (2), klossesett, føringshylsesett (2), skiveskruer (2), bremserens, rustfjerner, stålbørste, bremsefett, kobberfett, strips.

1. Løsne hjulmuttere på bakken. Jekk, bukker, hjulklosser bak, håndbrekk, gir.
2. Ta ut litt bremsevæske fra beholderen (sprøyte).
3. Skru ut glidebolter, løft av caliper, heng den i fjæra (strips). Ikke belast slangen.
4. Skru ut brakettbolter, ta av brakett. Skiveskrue ut med slagskrutrekker. Bank løs skiva.
5. Rens nav til blankt metall. Ny skive + ny skrue, tynt lag kobberfett på navet.
6. Rens brakett, nye føringshylser med bremsefett, nye klosser (litt fett på bakside og glidespor, ikke på friksjonsflate).
7. Press stempel inn (stempelpresse/tvinge). Monter caliper, trekk til med moment.
8. Hjul på, senk, trekk hjulmuttere i stjerne.
9. Pump pedalen fast før kjøring. Sjekk væskenivå.
10. Kjør inn rolig 200–300 km. Ettertrekk hjulmuttere etter 50–100 km.

Gjør én side om gangen.

### Momenter (sjekk mot instruksjonsbok/Haynes)

| Del | Moment |
|---|---|
| Hjulmuttere | ca. 103 Nm (Toyota-spes. Aygo), stjerne |
| Caliper brakettbolter | typisk 80–100 Nm |
| Caliper glidebolter | typisk 25–35 Nm |
| Skiveskruer | lett, til anlegg |
| Tennplugger | 28 Nm (Thansen/Bosch-spesifikasjon) |

Hjulmuttere: 21 mm (ta med 19 mm). Caliperbolter typisk 12–14 mm (glide) og 17 mm (brakett).

## Bestillingsliste

### A. Verktøy til bremsejobben

| Vare | Spesifikasjon | Pris (anslag) |
|---|---|---|
| Garasjejekk | 2 tonn, lav | 600–1 200 |
| Støttebukker | 2 stk, 2–3 tonn | 300–500 |
| Hjulklosser | 2 stk | 100–200 |
| Momentnøkkel | 1/2", 40–210 Nm | 500–900 |
| Pipesett | 1/2" + 1/4", 8–24 mm | 800–1 500 |
| Kraftpiper | 1/2", 17/19/21 mm (Makita muttertrekker) | 200–300 |
| Bryterhåndtak | 1/2", 45–60 cm | 200–300 |
| Slagskrutrekker (hand impact) | PH2/PH3 | 200–350 |
| Stempelpresse / stor tvinge | | 150–400 |
| Bremsevæskesprøyte | | 50–100 |
| Hansker, briller, filler | | 150 |

### B. Diagnose og batteri

| Vare | Spesifikasjon | Pris (anslag) |
|---|---|---|
| Vedlikeholdslader | CTEK MXS 5.0 / Noco Genius 5, 12 V 5 A | 1 000–1 300 |
| Multimeter | Digitalt, DC | 150–300 |
| Batteripolbørste | | 50–100 |
| Polfett | | 50–100 |
| Dielektrisk fett | Spolekontakter | 50–100 |
| Tennpluggpipe | 16 mm, 3/8", magnet/gummi | 100–200 |

### C. Deler som bør byttes uansett

| Vare | Spesifikasjon | Pris |
|---|---|---|
| Tennplugger × 3 | Thansen varenr. 999628000218, Bosch Double Iridium, NV 16, 28 Nm. **OBS: Thansen oppgir «årsmodell fra 05/2011». Bekreft med regnr at den passer 2008, ellers velg varianten merket 2005–2011.** Storo hadde 6 på lager 30.10 | 269 kr/stk |

### D. Etter diagnose

| Vare | Når | Pris (anslag) |
|---|---|---|
| Tennspole | Hvis kode flytter til P0302. OE Toyota/Denso eller Bosch/NGK. 1 eller 3 stk | 300–700/stk |
| Batteri | Bare hvis < 9,5 V etter lading og pussing. Ca. 40–45 Ah, 330+ A | 1 000–1 600 |
| Injektor | Bare etter at plugg og spole er utelukket. Verksted | – |

### Hvor
Thansen Storo/Vitaminveien (A, B, plugger, spoler), Biltema/Jula (jekk, bukker, pipesett, momentnøkkel), Clas Ohlson/Elkjøp (CTEK), Mekonomen/Bilxtra (deler med regnr-søk).

## Grunnutstyr for å fikse bilen selv (prioritert)

1. Jekk, bukker, klosser, momentnøkkel, pipesett
2. OBD2-leser (har: Sparco) og multimeter
3. Makita muttertrekker + kraftpiper
4. Slagskrutrekker, stempelpresse
5. Etter behov: oljefilterverktøy, oljeoppsamler, Torx-sett, plastverktøy til interiør, vinkelsliper m/stålbørste, arbeidslampe

Overlat til verksted: airbag, bremserør/-slanger, styring/hjuloppheng ved tvil, klimaanlegg, registerkjede, clutch.

Kunnskap: Haynes-manual Toyota Aygo / Citroën C1 / Peugeot 107 (2005–2014), YouTube («Aygo C1 107» + jobb), aygoclub.co.uk.

## Ordliste norsk–engelsk

| Norsk | Engelsk |
|---|---|
| Tennplugg | Spark plug |
| Tennspole | Ignition coil (coil pack, coil-on-plug) |
| Injektor | Fuel injector |
| Feiltenning sylinder 1 | Cylinder 1 misfire (P0301) |
| Bremseskive | Brake disc (UK) / rotor (US) |
| Bremsekloss | Brake pad |
| Caliper | Brake caliper |
| Caliperbrakett | Caliper bracket / carrier |
| Glidebolt | Caliper slide pin / guide pin |
| Føringshylse | Guide sleeve / slide pin bushing |
| Skiveskrue | Disc retaining screw |
| Stempel | Caliper piston |
| Nav | Hub |
| Hjulmutter | Wheel nut / lug nut |
| Batteripol, klemme | Battery terminal, clamp |
| Jording | Ground strap / earth strap |
| Startmotor | Starter motor |
| Dynamo | Alternator |
| Bremsevæske | Brake fluid |
| Jekk | Floor jack / trolley jack |
| Støttebukk | Axle stand / jack stand |
| Hjulkloss | Wheel chock |
| Momentnøkkel | Torque wrench |
| Pipesett | Socket set |
| Kraftpipe | Impact socket |
| Bryterhåndtak | Breaker bar |
| Muttertrekker | Impact wrench |
| Slagtrekker | Impact driver |
| Slagskrutrekker (manuell) | Hand impact driver |
| Pluggpipe | Spark plug socket |
| Stempelpresse | Caliper piston tool |
| Tvinge | G-clamp / C-clamp |
| Stålbørste | Wire brush |
| Vedlikeholdslader | Battery maintainer / smart charger |
| Feilkodeleser | OBD2 scanner / code reader |
| Polfett | Terminal grease |
| Kobberfett | Copper grease / anti-seize |
| Bremsefett | Caliper grease |
| Bremserens | Brake cleaner |
| Rustløser | Penetrating oil |

Søk på YouTube: `Toyota Aygo 1.0 spark plug replacement`, `Aygo C1 107 ignition coil replacement`, `Aygo front brake discs and pads replacement`, `1KR-FE misfire P0301`, `how to clean battery terminals ground strap`. Aygo, C1 og 107 (2005–2014) er samme bil.
