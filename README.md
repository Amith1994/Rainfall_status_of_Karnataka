# 🌧️ KSNDMC Daily Rainfall Status Analytics App

Dedicated folder for managing, auto-updating, and displaying **Karnataka Rainfall Performance & Departure Analytics** from KSNDMC Excel reports.

---

## 📂 Folder Structure

```
Rainfall_Status_App/
│
├── rainfall status.html            <-- Main Interactive Rainfall Status Analytics Dashboard
├── rainfall_status.html            <-- Mirror copy for web hosting / shortcut compatibility
├── template_rainfall_status.html   <-- Core HTML layout template
├── data_embedded.json              <-- Extracted District & Taluk JSON datasets
├── Rainfall status.xlsx            <-- Latest KSNDMC Excel Report (District & Taluk sheets)
│
├── auto_update_rainfall.py         <-- Automated Python parser & builder script
├── Update_Rainfall_Status.bat      <-- Double-click script to update and launch HTML app
├── karnataka_svg.js                <-- High-definition Karnataka SVG map coordinates
├── manifest.json & sw.js           <-- Progressive Web App (PWA) offline support
```

---

## 🚀 How Daily Updates Work

1. Download the daily rainfall report from [KSNDMC Daily Reports Portal](https://www.ksndmc.org/).
2. Keep the downloaded `.xlsx` file in your **Downloads** folder or copy it into this `Rainfall_Status_App` folder.
3. Double-click **`Update_Rainfall_Status.bat`** (or run `python auto_update_rainfall.py`).
4. The script will automatically:
   - Find the latest Excel report.
   - Parse all 47 Districts and 240+ Taluks across 13 seasonal periods.
   - Update `data_embedded.json` and rebuild `rainfall status.html`.
   - Open the updated dashboard in your web browser!

---

## 🌐 Online Browser Upload Option
You can also open [rainfall status.html](rainfall%20status.html) directly and click **"📂 Upload Rainfall Excel"** in the top navbar to instantly load any new Excel file without running any terminal commands.
