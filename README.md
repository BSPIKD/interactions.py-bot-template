# interactions.py šablona


**Tento kód není spustitelný bez předchozí úpravy**

Je potřeba aby bot běžel na verzi `python 3.8.6`, kterou
stáhnete [zde](https://www.python.org/downloads/release/python-386/). 
---
## Instalace

**Klon repositáře**

```bash
$ git clone git@gitlab.com:p6753/templates/interactions.py-template.git
$ git clone https://gitlab.com/p6753/templates/interactions.py-template.git
```

**Instalace knihoven**

```bash
$ pip install -r requirements.txt
```

- do souboru [.env.template](.env.template) přidej [token](https://discord.com/developers/applications) svého bota a
  nastav spojení do databáze
    - následně soubor přejmenuj z `.env.template` na `.env`
- spouštěcí soubor: [`bot.py`](bot.py)

## Ostatní
- Seznam eventů [zde](discord.com/developers/docs/topics/gateway)