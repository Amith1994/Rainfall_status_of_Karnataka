# 🌧️ KSNDMC Daily Rainfall Status & Departure Analytics Application
> **GKMS AgroMet Field Unit (AMFU), ZAHRS Hiriyur — KSNUAHS Agricultural Advisory Service**

An automated, interactive web dashboard and data processing engine for monitoring **Karnataka Rainfall Performance, Departure (%DEP), and Hydro-Climatic Trends** across **31 Districts** and **240+ Taluks**.

🌐 **Live Web Application (Accessible Anywhere):**
👉 **[https://amith1994.github.io/Rainfall_status_of_Karnataka/](https://amith1994.github.io/Rainfall_status_of_Karnataka/)**

---

## ⚡ Quick Start: 1-Click Desktop Updater

You can update the dashboard anytime using the **Desktop Shortcut**:
1. Double-click the **`Rainfall Status Auto-Updater`** shortcut on your Desktop.
2. The automated script will:
   - Check the KSNDMC server for new daily rainfall reports.
   - Parse all District & Taluk data across 13 seasonal periods.
   - Extract the exact report date (e.g. `23-07-2026`).
   - Rebuild `index.html` and update the navbar **DATA UPDATED AS ON** badge.
   - **Sync and push live changes directly to GitHub Pages (`origin/main`)**.
   - Open the updated interactive dashboard in your browser.

---

## 📂 Project Architecture & Folder Structure

```
Rainfall_Status_App/
│
├── index.html                      <-- GitHub Pages root entry point for web hosting
├── rainfall_status.html            <-- Interactive Rainfall Status Analytics Dashboard
├── rainfall status.html            <-- Desktop/Browser compatible copy
├── template_rainfall_status.html   <-- Core HTML master layout template
├── data_embedded.json              <-- Extracted District & Taluk JSON datasets
├── Rainfall status.xlsx            <-- KSNDMC Daily Excel Report (District & Taluk sheets)
│
├── auto_update_rainfall.py         <-- Automated Python parser, report fetcher & GitHub sync engine
├── build_rainfall_status.py        <-- Lightweight HTML builder from embedded JSON template
├── Update_Rainfall_Status.bat      <-- 1-Click launcher script for daily update workflow
├── create_rainfall_shortcut.ps1    <-- Powershell script to manage Desktop shortcut (.lnk)
│
├── karnataka_svg.js                <-- High-definition Karnataka SVG map coordinates & centroids
├── manifest.json & sw.js           <-- Progressive Web App (PWA) offline caching & tablet optimization
└── assets/                         <-- App icons and logo assets
```

---

## 🌟 Key Application Features

* 🗺️ **High-Definition Interactive Spatial Map:** Instant visual color-coding for Large Excess (+60%), Excess (+20%), Normal (±19%), Deficient (-20%), Large Deficient (-60%), and No Rain. Hover tooltips and click district selection.
* 📅 **Prominent Data Date Badge:** Displays `DATA UPDATED AS ON: DD-MM-YYYY` right in the top navigation header.
* 📊 **Hydro-Climatic Progression Analytics:**
  * District-level monthly progression graphs (Jan to July).
  * Agro-climatic regional progression graphs (**Coastal**, **NIK**, **SIK**, **Malnad**).
  * Seasonal breakdowns for **SW Monsoon**, **NE Monsoon**, **Pre-Monsoon**, and **Annual (YTD)**.
* 🔍 **Taluk-Level Granularity:** Sortable data table supporting both District and Block/Taluk level drilldown with instant search filtering.
* 📁 **Online Excel Upload:** In addition to automated local scripts, users can open the live web app on mobile/tablet and click **"📁 UPLOAD RAINFALL STATUS.XLSX"** to parse any report in-browser.
* 📲 **PWA & Tablet Caching:** Progressive Web App (`sw.js` & `manifest.json`) support for touch devices and offline usage.

---

## 🔧 Managing Desktop Shortcut

To recreate or repair the Desktop shortcut at any time:
```powershell
powershell -ExecutionPolicy Bypass -File create_rainfall_shortcut.ps1
```
This updates `C:\Users\<User>\Desktop\Rainfall Status Auto-Updater.lnk` pointing to `Update_Rainfall_Status.bat`.

---

## 📜 Credits & Citation
Developed for **GKMS AgroMet Field Unit (AMFU), ZAHRS, Hiriyur, Chitradurga District**, under **Keladi Shivappa Nayaka University of Agricultural and Horticultural Sciences (KSNUAHS)** using KSNDMC data.
