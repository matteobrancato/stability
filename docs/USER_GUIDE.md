# Stability Dashboard - Guida Utente

## 🎯 Panoramica

Il **Stability Dashboard** è un'applicazione web interattiva che visualizza l'analisi delle cause principali (root causes) dei fallimenti nei test di automazione, permettendo di monitorare la stabilità del framework nel tempo.

---

## 🚀 Come Utilizzare il Dashboard

### Opzione 1: Utenti con OneDrive Sync (CONSIGLIATA)

Se hai OneDrive sincronizzato e il file è nella tua cartella locale:

1. **Avvia il dashboard**:
   ```bash
   streamlit run stability_dashboard.py
   ```

2. **Il dashboard si apre automaticamente** nel browser su `http://localhost:8501`

3. **Seleziona "Use local file"** nella sidebar (opzione predefinita)
   - Il file viene caricato automaticamente
   - Mostra quando è stato aggiornato l'ultima volta
   - Si aggiorna automaticamente quando OneDrive sincronizza

4. **Seleziona il Business Unit** dal menu dropdown

5. **Analizza i dati**:
   - Visualizza i grafici delle root causes
   - Monitora le soglie (thresholds)
   - Esporta i dati se necessario

---

### Opzione 2: Utenti SENZA OneDrive Sync

Se non hai il file sincronizzato localmente:

1. **Scarica il file da SharePoint**:
   - Apri il link SharePoint (fornito nella sidebar del dashboard)
   - Click su "Download"
   - Salva il file localmente

2. **Avvia il dashboard**:
   ```bash
   streamlit run stability_dashboard.py
   ```

3. **Seleziona "Upload file"** nella sidebar

4. **Carica il file Excel**:
   - Click su "Browse files"
   - Seleziona il file `KPIsStabilityTAS.xlsx` scaricato
   - Il dashboard carica automaticamente i dati

5. **Seleziona il Business Unit** e analizza

---

## 📊 Funzionalità Principali

### 1. Selezione Business Unit
- Dropdown nella sidebar
- Tutti i BU disponibili nel file Excel
- Kruidvat selezionato di default

### 2. Visualizzazioni

#### Grafici Individuali
- Un grafico per ogni root cause
- Linea dei valori attuali (blu)
- Linea della soglia (arancione tratteggiata)
- Area rossa quando si supera la soglia
- ⭐ per KPI importanti

#### Tabella Dati
- Vista tabellare dei dati raw
- Valori formattati come percentuali
- Esportazione CSV disponibile

### 3. Informazioni Visualizzate
- Fonte dei dati (locale o caricato)
- Data ultimo aggiornamento
- Numero di sheet disponibili
- KPI importanti per ogni BU

---

## ⚙️ Configurazione

Il file `config.py` contiene tutte le impostazioni:

```python
# Percorso file locale (per OneDrive sync)
EXCEL_FILE_PATH = r"C:\Users\...\Stability.xlsx"

# Link SharePoint (per download manuale)
SHAREPOINT_LINK = "https://asweu-my.sharepoint.com/..."

# Funzionalità
ENABLE_FILE_UPLOAD = True  # Abilita caricamento file
SHOW_SHAREPOINT_LINK = True  # Mostra link SharePoint
```

---

## 🔧 Risoluzione Problemi

### Dashboard non si avvia
```bash
# Verifica installazione Python
py --version

# Reinstalla dipendenze
py -m pip install -r requirements.txt

# Avvia con modalità verbose
streamlit run stability_dashboard.py --logger.level=debug
```

### File non trovato
- **Opzione 1**: Verifica che il percorso in `config.py` sia corretto
- **Opzione 2**: Usa il file uploader e carica manualmente

### Grafici non visualizzati
- Verifica che il file Excel abbia i fogli corretti
- Controlla che le colonne delle root causes esistano
- Guarda i log nel terminale per errori dettagliati

### Dati non aggiornati
- **Con file locale**: Attendi la sincronizzazione OneDrive, poi click su "🔄 Reload"
- **Con file caricato**: Scarica la nuova versione da SharePoint e ricarica

---

## 📁 Struttura File Excel Richiesta

### Sheet "Static Values"
```
Row 1: [Label]      | Thresholds
Row 2: [Root cause] | Maintenance | System Issue | ...
Row 3: [Values]     | 5%          | 3%           | ...
Row 6: [BU Names]   | Kruidvat    | Trekpleister | ...
Row 7: [Important]  | Maint,Sys   | Test Data    | ...
```

### Sheet per ogni BU (es. "Kruidvat")
```
Date/Week | Maintenance % | System Issue % | Test Data % | ...
01-01-25  | 2.5%         | 1.8%          | 0.5%        | ...
08-01-25  | 3.2%         | 2.1%          | 0.8%        | ...
...
```

---

## 🌐 Condivisione con Altri

### Per chi usa il dashboard:

1. **Clona il repository** o ricevi i file del progetto

2. **Installa le dipendenze**:
   ```bash
   py -m pip install -r requirements.txt
   ```

3. **Scegli il metodo**:
   - **Metodo A (OneDrive)**: Configura `EXCEL_FILE_PATH` in `config.py`
   - **Metodo B (Upload)**: Scarica il file da SharePoint quando necessario

4. **Avvia**:
   ```bash
   streamlit run stability_dashboard.py
   ```

### Deploy su Streamlit Cloud (Opzionale)

Per rendere il dashboard accessibile via web:

1. Push del codice su GitHub
2. Vai su [share.streamlit.io](https://share.streamlit.io)
3. Collega il repository
4. Gli utenti dovranno caricare il file tramite uploader

**Nota**: Non è possibile accedere automaticamente a file SharePoint aziendali da Streamlit Cloud per motivi di sicurezza.

---

## 📞 Supporto

### Link Utili
- **SharePoint File**: [Link configurato in `config.py`]
- **Documentazione Streamlit**: https://docs.streamlit.io
- **Repository Progetto**: [Se disponibile]

### Per Assistenza
- Controlla i log nel terminale
- Verifica `requirements.txt` sia aggiornato
- Contatta il team di sviluppo

---

## 🔄 Aggiornamenti

### Versione Attuale: 2.0
**Data**: 2025-01-08

**Novità**:
- ✅ Supporto file uploader
- ✅ Interfaccia semplificata
- ✅ Supporto sia file locale che caricato
- ✅ Link diretto a SharePoint
- ✅ Rimozione complessità autenticazione

**Versione Precedente: 1.0**
- Dashboard base con solo file locale

---

## 💡 Best Practices

### Per Performance Ottimali
- Usa file locale con OneDrive sync quando possibile
- Chiudi il file Excel se aperto (evita conflitti)
- Ricarica i dati quando necessario

### Per Condivisione
- Condividi il link SharePoint insieme al codice
- Documenta il percorso del file locale
- Usa `requirements.txt` per dipendenze

### Per Manutenzione
- Mantieni `config.py` aggiornato
- Verifica periodicamente il link SharePoint
- Aggiorna le dipendenze quando necessario

---

**Ultimo aggiornamento**: 2025-01-08
**Autore**: Team Automation
**Versione Dashboard**: 2.0
