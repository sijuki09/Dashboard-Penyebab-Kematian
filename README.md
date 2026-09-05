# Dashboard Visualization of Causes of Death in Indonesia

> An interactive dashboard that visualizes trends and causes of death in Indonesia based on data from the Indonesian Ministry of Health's Health Profile reports covering 2000 to 2021.

## Dashboard Overview

* **Chart 1: Annual Death Trends (Line Chart)** - Visualizes the changes in total deaths over time, both overall and by category, including Diseases & Non-Natural Disasters, Natural Disasters, and Social Disasters.
* **Chart 2: Death Category Proportion (Doughnut Chart)** - Shows the percentage distribution of deaths across different cause categories.
* **Chart 3: Top 10 Causes of Death (Horizontal Bar Chart)** - Ranks the 10 specific causes of death with the highest number of reported deaths based on the selected filters.
* **Interactive Features**:

  * *Type Filter Dropdown*: Selects a specific category, including Diseases, Natural Disasters, or Social Disasters, and dynamically updates the dashboard visualizations.
  * *Text Search*: Filters causes of death based on user input.
  * *Year Range Slider*: Dynamically limits the visualization to a selected year range.
  * *Legend Toggle*: Allows individual categories to be shown or hidden directly from the Line Chart legend.
  * *Interactive Tooltips*: Displays detailed values when hovering over data points in the Chart.js visualizations.
  * *Paginated Data Table*: Provides access to detailed records with responsive pagination.
* **Animations**:

  * *Chart.js Entrance Animation*: Charts load with smooth built-in transition animations.
  * *Count-up Numbers*: KPI values, including Total Deaths, animate from zero to their final values when the dashboard loads or filters are changed.
  * *CSS Fade-in*: Dashboard elements are introduced with smooth CSS fade-in animations using `@keyframes`.

## Data Source

* **Dataset**: Causes of Death in Indonesia (2000 - 2021) by Hendratno.
* **Source**: [Kaggle - Causes of Death in Indonesia](https://www.kaggle.com/datasets/hendratno/cause-of-death-in-indonesia)
* The dataset was compiled from the Indonesian Ministry of Health's *Health Profile of Indonesia* reports.

## Running Locally

### Option A: Static

1. Open `index.html` directly in a modern web browser such as Google Chrome, Firefox, Safari, or Microsoft Edge.
2. Alternatively, open the project in Visual Studio Code and use the **Live Server** extension for automatic browser reloading.

### Option B: Static Server

The dashboard can also be served using a simple local static server:

```bash
npm install -g serve
serve .
```

Then open the local address provided by the server in a web browser.

## Technology

* **Chart.js**: Interactive data visualization through CDN
* **HTML5 & CSS3**: Responsive grid layout, CSS variables, and glassmorphic UI
* **Vanilla JavaScript**: Dashboard state management, data aggregation, filtering, and count-up animations
