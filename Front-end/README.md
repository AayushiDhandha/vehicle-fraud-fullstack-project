# Aegis - Vehicle Insurance Fraud Analytics Hub

A premium, highly interactive, client-side single-page application (SPA) built to explore, optimize, and analyze vehicle insurance claims and detect fraudulent patterns. The application uses the Minitab **Vehicle Insurance Fraud** dataset (1000 claims, 39 features) and provides a professional suite of visualization, statistical analysis, predictive modeling, and data preparation tools.

---

## Key Features

1. **Hub Overview (Executive Dashboard)**
   - High-level KPIs (Total Claims, Fraud Count, Fraud Rate, Avg Claim Amount) with smooth hover effects.
   - Interactive data visualizations powered by **Chart.js** including:
     - **Fraud Risk by Incident Severity** (Bar Chart - identifying "Major Damage" as the highest risk category).
     - **Claim Component Breakdown** (Doughnut Chart - splitting average claims into vehicle, injury, and property components).
     - **Top Hobbies by Fraud Rate** (Horizontal Bar Chart - revealing risk patterns associated with hobbies like Chess and Yachting).
     - **Fraud Rate vs. Incident Hour** (Line Chart - highlighting peak hourly trends).

2. **Interactive Data Explorer**
   - Paginated, searchable, and sortable data table displaying all 1000 claims.
   - Filters to narrow down claims by Fraud Status, Incident Severity, and Policy State.
   - **Inspect Drawer Panel**: Click on any claim to open a slide-over panel displaying all 39 variables organized logically into categories (Policy Details, Insured Demographics, Accident Particulars, and Financial/Fraud Verdict).

3. **Minitab Analytics Suite**
   - **One-Way ANOVA Simulator**: Evaluates if the average claim amount varies significantly across different accident severities. Computes the statistical Sum of Squares (SS), Mean Squares (MS), F-Value, and **calculates the P-value** in real-time. Includes a 95% Confidence Interval error plot.
   - **Process Capability Analysis**: Computes capability indices ($C_p$ and $C_{pk}$) for Customer Safety Ratings against specification limits ($LSL=20, USL=90$). Overlays a normal distribution density curve fit on a detailed histogram of ratings.
   - **Pearson Correlation Matrix**: Calculates correlation coefficients ($r$) between numerical features and renders a dynamic, color-coded heatmap.

4. **Fraud Risk Predictor**
   - Interactive risk calculator based on weighted heuristics tuned to the dataset's actual patterns.
   - Updates as you slide ranges or change options (Incident Severity, Hobby, Collision Type, Age, Claim Amount, Hour, etc.).
   - Includes an **animated SVG circular risk gauge** showing classification ranges (Low, Medium, High Risk) and lists specific risk factors contributing to the score.

5. **Data Prep Lab**
   - Simulates typical Minitab cleaning operations:
     1. **Standardize Missing Values**: Converts missing categorical marks (`?`) to `Unknown`.
     2. **Outlier Trimming**: Dynamically detects premium outliers ($>\pm 3\sigma$) and filters them out.
     3. **Continuous Age Binning**: Discretizes ages into Young Adult ($<30$), Adult ($30-50$), and Senior ($>50$).
   - Features a **live preview table** showing the first 5 rows changing instantly and quality metrics tracking missing count, rows remaining, and dataset state.
   - State updates propagate reactively across all tabs, updating the explorer table and analytics results in real-time.

---

## How to Run the Project

Since this is a client-side SPA built using HTML5, CSS3, and JavaScript ES6, you can run it instantly:

1. **Direct Double-Click:** 
   Double-click the [`index.html`](file:///d:/SEM-5/ML/Front-end/index.html) file to open it directly in any modern web browser.
   
2. **Local HTTP Server (Optional - recommended for custom CSV file uploading):**
   If your browser blocks certain local file actions due to security boundaries, launch a simple local server. In a terminal within this directory, run:
   - using **Node.js**:
     ```bash
     npx http-server ./
     ```
   - using **Python**:
     ```bash
     python -m http.server 8000
     ```
   Then open `http://localhost:8080` (or `http://localhost:8000`) in your browser.

---

## Technology Stack

- **Core Structure:** HTML5
- **Styling:** Custom Vanilla CSS3 (features full dark/light theme options, responsive drawer modules, grid layouts, and zero Tailwind/bootstrap dependencies for maximum control).
- **Libraries (Integrated via CDN):**
  - **Chart.js:** For high-performance visual canvas charts.
  - **PapaParse:** For fast and safe client-side CSV parsing.
  - **Lucide Icons:** For modern, SVG-based responsive iconography.
