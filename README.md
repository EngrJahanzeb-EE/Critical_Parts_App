# ⚡ Critical Parts Logger — Sapphire Fibres Limited

A fast, clean web app to log and export critical automation components from machine panels and schematics — VFDs, Motors, PLCs, Encoders, Breakers, and more — with one-click Excel export.

---

## Features

- **10 component types** — VFD/Drive, Motor, PLC, HMI, Encoder/Resolver, Load Cell, Breaker/MCCB, Relay/Contactor, Transformer, Other
- **Smart fields per type** — Only relevant fields shown (kW, Amps, Voltage, RPM, IP rating, etc.)
- **Tag capture** — Panel tag AND schematic/SLD tag both recorded
- **Filter view** — Filter by Department, Machine, or Component Type
- **Excel export** — 3-tab workbook: full data, summary, by-department count
- **No database needed** — Session-based, export when done

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/critical-parts-logger.git
cd critical-parts-logger

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

App opens at **http://localhost:8501**

---

## Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → `app.py` → **Deploy**

That's it. Free hosting, auto-redeploys on every git push.

---

## Component Fields Reference

| Type | Key Fields |
|------|-----------|
| VFD / Drive | kW, Output A, Input V, Hz |
| Motor | kW, FLA, V, RPM, Poles, Ins. Class, IP |
| PLC | Supply V, I/O Count, Protocol |
| HMI | Supply V, Protocol, Screen Size |
| Encoder / Resolver | Supply V, PPR/Bits, Output Type |
| Load Cell | Supply V, Capacity, mV/V |
| Breaker / MCCB | Rated A, V, Breaking kA, Poles |
| Relay / Contactor | Coil V, Contact Rating A |
| Transformer | kVA, Primary V, Secondary V, Hz |
| Other | Custom rating + Supply V |

All types also capture: **Panel Tag**, **Schematic/SLD Tag**, **Make/Brand**, **Model No.**, **Notes**

---

## Excel Output

| Sheet | Contents |
|-------|----------|
| Critical Parts List | Full data, all columns, zebra-striped, frozen header |
| Summary | Count by Department → Machine → Type |
| By Department | Total components per department |

---

Built for the Electrical Department MTO, Sapphire Fibres Limited.
