# lkod-validator
Validátor LKOD je utilita, ktorá načíta Lokálny katalóg otvorených údajov poskytovateľa, a pomocou [Povinných vlastností otvorených údajov](https://github.com/slovak-egov/centralny-model-udajov/blob/main/tbox/national/dcat-ap-sk-2.0-shapes-2023b.02.ttl), vykoná ich validáciu a vráti výsledok. Výstupom je vytvorenie troch súborov: rdf_graph (obsahuje celý LKOD), shacl_graph (obsahuje definíciu povinných vlastností údajov) a report_graph (výsledok validácie).

Použitie:

```shell
python3 validateLKOD.py [URI] [FORMAT]
```

Príklad:

```shell
python3 validateLKOD.py https://opendata.trnava.sk/opendata/set/lkod ttl
```

```shell
python3 validateLKOD.py https://opendata.levoca.sk/set/catalog/lkod json-ld
```