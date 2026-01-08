# Stability Dashboard

Un'applicazione web interattiva per visualizzare e analizzare le root causes dei fallimenti nei test di automazione, permettendo di monitorare la stabilità del framework nel tempo.

---

## 🚀 Quick Start

```bash
# 1. Installa le dipendenze
pip install -r requirements.txt

# 2. Avvia il dashboard
streamlit run stability_dashboard.py

# 3. Il browser si apre automaticamente su http://localhost:8501
```

---

## 📋 Prerequisiti

- **Python 3.8+**
- **File Excel**: `KPIsStabilityTAS.xlsx` con la struttura richiesta (vedi sotto)

---

## 📁 Struttura del Repository

```
stability/
├── stability_dashboard.py      # Applicazione principale
├── config.py                    # Configurazione
├── requirements.txt             # Dipendenze Python
├── sharepoint_helper.py         # Helper SharePoint (legacy)
├── launch_dashboard.bat         # Script per avvio rapido (Windows)
├── README.md                    # Questo file
├── docs/                        # Documentazione
│   ├── USER_GUIDE.md           # Guida utente completa
│   ├── IMPLEMENTATION_SUMMARY.md # Dettagli tecnici
│   ├── RIEPILOGO_FINALE.md     # Riepilogo in italiano
│   └── archive/                # Documentazione obsoleta
└── tests/                       # Script di test
    ├── test_setup.py
    └── test_sharepoint.py
```

---

## ⚙️ Configurazione

Modifica `config.py` per personalizzare:

```python
# Percorso file locale (se hai OneDrive sync)
EXCEL_FILE_PATH = r"C:\Users\...\Stability.xlsx"

# Link SharePoint per download manuale
SHAREPOINT_LINK = "https://sharepoint.com/..."

# Funzionalità
ENABLE_FILE_UPLOAD = True      # Abilita caricamento file
SHOW_SHAREPOINT_LINK = True    # Mostra link SharePoint
```

---

## 📊 Come Funziona

### Opzione 1: File Locale (OneDrive Sync)

Se hai il file sincronizzato con OneDrive:
- ✅ Dashboard carica automaticamente il file
- ✅ Si aggiorna quando OneDrive sincronizza
- ✅ Mostra data ultimo aggiornamento

### Opzione 2: File Upload

Se non hai il file in locale:
1. Apri il dashboard
2. Click su link SharePoint nella sidebar
3. Scarica il file da SharePoint
4. Carica il file nel dashboard (drag & drop)

---

## 📈 Funzionalità

### Visualizzazioni
- **Grafici interattivi** per ogni root cause
- **Linee threshold** per monitoraggio soglie
- **Evidenziazione automatica** quando si superano i limiti
- **KPI importanti** marcati con ⭐

### Business Units
- Selezione tramite dropdown
- Supporto multi-BU (Kruidvat, Trekpleister, ecc.)
- KPI specifici per ogni BU

### Dati
- **Tabella dati** con formattazione
- **Export CSV** per analisi esterne
- **Date e timestamp** chiari

---

## 📝 Struttura File Excel Richiesta

### Sheet "Static Values"

```
Row 1: [Label]      | Thresholds
Row 2: [Root cause] | Maintenance | System Issue | ...
Row 3: [Values]     | 5%          | 3%           | ...
...
Row 6: [BU Names]   | Kruidvat    | Trekpleister | ...
Row 7: [Important]  | Maint,Sys   | Test Data    | ...
```

### Sheet per ogni BU (es. "Kruidvat")

```
Date/Week | Maintenance % | System Issue % | Test Data % | ...
01-01-25  | 2.5%         | 1.8%          | 0.5%        | ...
08-01-25  | 3.2%         | 2.1%          | 0.8%        | ...
```

---

## 🛠️ Tecnologie Utilizzate

- **[Streamlit](https://streamlit.io)** - Framework web interattivo
- **[Plotly](https://plotly.com)** - Grafici interattivi
- **[Pandas](https://pandas.pydata.org)** - Analisi dati
- **[openpyxl](https://openpyxl.readthedocs.io)** - Lettura file Excel

---

## 📚 Documentazione

- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Guida utente completa
- **[IMPLEMENTATION_SUMMARY.md](docs/IMPLEMENTATION_SUMMARY.md)** - Dettagli tecnici
- **[RIEPILOGO_FINALE.md](docs/RIEPILOGO_FINALE.md)** - Riepilogo in italiano

---

## 🔧 Risoluzione Problemi

### Dashboard non si avvia

```bash
# Verifica installazione Python
python --version

# Reinstalla dipendenze
pip install -r requirements.txt --upgrade

# Avvia con debug
streamlit run stability_dashboard.py --logger.level=debug
```

### File non trovato

- Verifica percorso in `config.py`
- Usa file uploader come alternativa
- Controlla che il file esista e sia accessibile

### Grafici non visualizzati

- Verifica struttura file Excel
- Controlla log nel terminale per errori
- Assicurati che esistano le colonne root cause

---

## 🚀 Deploy (Opzionale)

Per rendere il dashboard accessibile online:

1. Push su GitHub
2. Deploy su [Streamlit Cloud](https://share.streamlit.io)
3. Gli utenti caricano il file tramite uploader

---

## 📄 License

Uso interno - A.S. Watson Europe

---

## 👥 Supporto

Per assistenza o domande:
- Consulta la [documentazione](docs/)
- Verifica i [test](tests/) per esempi
- Contatta il team Automation

---

## 🔄 Versioni

### v2.0 (2025-01-08)
- ✅ File uploader integrato
- ✅ Supporto file locale e caricato
- ✅ UI rinnovata
- ✅ Link SharePoint per download manuale
- ✅ Documentazione completa

### v1.0 (2025-01-07)
- ✅ Dashboard base con grafici interattivi
- ✅ Supporto multi-BU
- ✅ Threshold monitoring
- ✅ Export CSV

---

**Ultimo aggiornamento**: 2025-01-08
**Versione**: 2.0
**Status**: ✅ Production Ready
