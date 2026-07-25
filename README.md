# 🌧️ KSNDMC Daily Rainfall Status Analytics App

Dedicated folder for managing, auto-updating, and displaying **Karnataka Rainfall Performance & Departure Analytics** from KSNDMC Excel reports.

🌐 **Live Dashboard (Accessible Anywhere):**
👉 **[https://amith1994.github.io/Rainfall_status_of_Karnataka/](https://amith1994.github.io/Rainfall_status_of_Karnataka/)**

---

## 📂 Folder Structure

```
Rainfall_Status_App/
│
├── index.html                      <-- GitHub Pages root entry point for web hosting
├── rainfall status.html            <-- Main Interactive Rainfall Status Analytics Dashboard
├── rainfall_status.html            <-- Mirror copy for web hosting / shortcut compatibility
├── template_rainfall_status.html   <-- Core HTML layout template
├── data_embedded.json              <-- Extracted District & Taluk JSON datasets
├── Rainfall status.xlsx            <-- Latest KSNDMC Excel Report (District & Taluk sheets)
│
├── auto_update_rainfall.py         <-- Automated Python parser, builder & GitHub sync script
├── Update_Rainfall_Status.bat      <-- Double-click script to update & push live to GitHub
├── karnataka_svg.js                <-- High-definition Karnataka SVG map coordinates
├── manifest.json & sw.js           <-- Progressive Web App (PWA) offline support
```

---

## 🚀 How Daily Updates & GitHub Sync Work

1. Download the daily rainfall report from [KSNDMC Daily Reports Portal](https://www.ksndmc.org/).
2. Keep the downloaded `.xlsx` file in your **Downloads** folder or copy it into this `Rainfall_Status_App` folder.
3. Double-click **`Update_Rainfall_Status.bat`** (or run `python auto_update_rainfall.py`).
4. The script will automatically:
   - Find the latest Excel report.
   - Parse all Districts and 240+ Taluks across 13 seasonal periods.
   - Update `data_embedded.json` and rebuild `index.html` / `rainfall_status.html`.
   - **Commit and Push changes to GitHub automatically (`origin/main`)**.
   - Open the updated dashboard locally and provide the **Live GitHub Pages URL**!

---

## 🌐 Online Browser Upload Option
You can also open [https://amith1994.github.io/Rainfall_status_of_Karnataka/](https://amith1994.github.io/Rainfall_status_of_Karnataka/) directly on any device (phone, laptop, tablet) and click **"📂 Upload Rainfall Excel"** in the top navbar to instantly load any new Excel file without running any scripts.
