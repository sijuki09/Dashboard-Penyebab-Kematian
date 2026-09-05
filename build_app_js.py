import json

def build_app_js():
    # Read the clean JSON data
    with open('data_kematian_clean.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Serialize it to a JS variable
    data_js_str = json.dumps(data, ensure_ascii=False, indent=2)
    
    # JavaScript code body
    js_code_body = """// Cause of Death in Indonesia Dashboard Controller
// Sourced dynamically from clean Kaggle dataset based on Kemenkes RI Profil Kesehatan (2000-2021)

// Dashboard State
let activeType = 'all';
let searchQuery = '';
let minYear = 2000;
let maxYear = 2021;
let currentPage = 1;
const itemsPerPage = 8;

// Chart Instances
let lineChart = null;
let doughnutChart = null;
let barChart = null;

// DOM Elements
const elTotalDeaths = document.getElementById('total-deaths');
const elTopCause = document.getElementById('top-cause');
const elTopCategory = document.getElementById('top-category');
const elTypeFilter = document.getElementById('type-filter');
const elSearchInput = document.getElementById('search-input');
const elYearSlider = document.getElementById('year-slider');
const elYearDisplay = document.getElementById('year-display');
const elTableBody = document.getElementById('table-body');
const elPrevPage = document.getElementById('prev-page');
const elNextPage = document.getElementById('next-page');
const elPageInfo = document.getElementById('page-info');

// Theme Colors
const COLORS = {
  cyan: '#06b6d4',
  blue: '#3b82f6',
  emerald: '#10b981',
  rose: '#f43f5e',
  amber: '#f59e0b',
  bgsecondary: '#0f172a',
  textPrimary: '#f8fafc',
  textSecondary: '#94a3b8',
  border: 'rgba(255, 255, 255, 0.08)',
  gridLine: 'rgba(255, 255, 255, 0.04)'
};

// Count-up animation for numbers
function animateCountUp(element, endVal, duration = 1200) {
  if (!element) return;
  const startVal = 0;
  const startTime = performance.now();
  
  function updateNumber(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // EaseOutQuad function
    const easeProgress = progress * (2 - progress);
    const currentVal = Math.floor(startVal + (endVal - startVal) * easeProgress);
    
    element.textContent = currentVal.toLocaleString('id-ID');
    
    if (progress < 1) {
      requestAnimationFrame(updateNumber);
    } else {
      element.textContent = endVal.toLocaleString('id-ID');
    }
  }
  requestAnimationFrame(updateNumber);
}

// Initialize Dashboard
function init() {
  // Get range of years in dataset
  const years = mortalityData.map(d => d.year);
  minYear = Math.min(...years);
  maxYear = Math.max(...years);
  
  // Set slider min, max, value
  elYearSlider.min = minYear;
  elYearSlider.max = maxYear;
  elYearSlider.value = maxYear;
  elYearDisplay.textContent = maxYear;
  
  // Initialize Chart.js
  initCharts();
  
  // Setup Event Listeners
  elTypeFilter.addEventListener('change', (e) => {
    activeType = e.target.value;
    currentPage = 1;
    updateDashboard();
  });
  
  elSearchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    currentPage = 1;
    updateDashboard();
  });
  
  elYearSlider.addEventListener('input', (e) => {
    maxYear = parseInt(e.target.value);
    elYearDisplay.textContent = maxYear;
    currentPage = 1;
    updateDashboard();
  });
  
  elPrevPage.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      renderTable();
    }
  });
  
  elNextPage.addEventListener('click', () => {
    currentPage++;
    renderTable();
  });
  
  // Initial Render
  updateDashboard(true);
}

// Initialize Charts
function initCharts() {
  // 1. Line Chart: Trends over time
  const ctxLine = document.getElementById('lineChart').getContext('2d');
  lineChart = new Chart(ctxLine, {
    type: 'line',
    data: {
      labels: [],
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: COLORS.textPrimary,
            font: { family: 'Plus Jakarta Sans', size: 11 }
          }
        },
        tooltip: {
          padding: 12,
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          titleColor: '#fff',
          titleFont: { family: 'Plus Jakarta Sans', weight: 'bold' },
          bodyFont: { family: 'Plus Jakarta Sans' },
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1
        }
      },
      scales: {
        x: {
          grid: { color: COLORS.gridLine },
          ticks: { color: COLORS.textSecondary, font: { family: 'JetBrains Mono' } }
        },
        y: {
          grid: { color: COLORS.gridLine },
          ticks: { color: COLORS.textSecondary, font: { family: 'JetBrains Mono' } }
        }
      }
    }
  });

  // 2. Doughnut Chart: Death Category Distribution
  const ctxDoughnut = document.getElementById('doughnutChart').getContext('2d');
  doughnutChart = new Chart(ctxDoughnut, {
    type: 'doughnut',
    data: {
      labels: [],
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: COLORS.textPrimary,
            font: { family: 'Plus Jakarta Sans', size: 10 },
            padding: 15
          }
        },
        tooltip: {
          padding: 12,
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          titleColor: '#fff',
          bodyFont: { family: 'Plus Jakarta Sans' }
        }
      },
      cutout: '65%'
    }
  });

  // 3. Bar Chart: Top Causes of Death
  const ctxBar = document.getElementById('barChart').getContext('2d');
  barChart = new Chart(ctxBar, {
    type: 'bar',
    data: {
      labels: [],
      datasets: []
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          padding: 12,
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          bodyFont: { family: 'Plus Jakarta Sans' }
        }
      },
      scales: {
        x: {
          grid: { color: COLORS.gridLine },
          ticks: { color: COLORS.textSecondary, font: { family: 'JetBrains Mono' } }
        },
        y: {
          grid: { display: false },
          ticks: { color: COLORS.textPrimary, font: { family: 'Plus Jakarta Sans', size: 11 } }
        }
      }
    }
  });
}

// Filter and Aggregate Data
let currentFilteredData = [];
function updateDashboard(isInitial = false) {
  // Filter core data
  currentFilteredData = mortalityData.filter(d => {
    const matchType = activeType === 'all' || d.type === activeType;
    const matchSearch = searchQuery === '' || d.cause.toLowerCase().includes(searchQuery);
    const matchYear = d.year <= maxYear;
    return matchType && matchSearch && matchYear;
  });
  
  // Calculate Totals & Stats
  let totalDeaths = 0;
  const deathsByCause = {};
  const deathsByType = {};
  
  // Initialize type aggregators
  deathsByType['Bencana Non Alam dan Penyakit'] = 0;
  deathsByType['Bencana Alam'] = 0;
  deathsByType['Bencana Sosial'] = 0;

  currentFilteredData.forEach(d => {
    totalDeaths += d.deaths;
    
    // Aggregate by specific cause
    deathsByCause[d.cause] = (deathsByCause[d.cause] || 0) + d.deaths;
    
    // Aggregate by type
    deathsByType[d.type] = (deathsByType[d.type] || 0) + d.deaths;
  });
  
  // Render KPI Metrics
  animateCountUp(elTotalDeaths, totalDeaths);
  
  // Top Category
  let topCatName = '-';
  let topCatVal = 0;
  for (const [cat, val] of Object.entries(deathsByType)) {
    if (val > topCatVal) {
      topCatVal = val;
      topCatName = cat;
    }
  }
  // Shorten name if too long for display
  let topCatDisplay = topCatName;
  if (topCatName === 'Bencana Non Alam dan Penyakit') topCatDisplay = 'Penyakit & Non-Alam';
  elTopCategory.textContent = totalDeaths > 0 ? topCatDisplay : '-';
  
  // Top Specific Cause
  let topCauseName = '-';
  let topCauseVal = 0;
  for (const [cause, val] of Object.entries(deathsByCause)) {
    if (val > topCauseVal) {
      topCauseVal = val;
      topCauseName = cause;
    }
  }
  // Limit string length for top cause KPI card
  if (topCauseName.length > 22) topCauseName = topCauseName.substring(0, 20) + '...';
  elTopCause.textContent = totalDeaths > 0 ? topCauseName : '-';
  
  // Update Charts
  updateLineChart();
  updateDoughnutChart(deathsByType);
  updateBarChart(deathsByCause);
  
  // Render Table
  renderTable();
}

// 1. Update Line Chart (Trends)
function updateLineChart() {
  // Group deaths by year and category
  const yearsSet = new Set();
  const yearlyData = {};
  
  // We want to show the years from minYear to maxYear
  for (let yr = minYear; yr <= maxYear; yr++) {
    yearsSet.add(yr);
    yearlyData[yr] = {
      total: 0,
      disease: 0,
      natural: 0,
      social: 0
    };
  }
  
  currentFilteredData.forEach(d => {
    if (yearlyData[d.year]) {
      yearlyData[d.year].total += d.deaths;
      if (d.type === 'Bencana Non Alam dan Penyakit') yearlyData[d.year].disease += d.deaths;
      else if (d.type === 'Bencana Alam') yearlyData[d.year].natural += d.deaths;
      else if (d.type === 'Bencana Sosial') yearlyData[d.year].social += d.deaths;
    }
  });
  
  const sortedYears = Array.from(yearsSet).sort((a, b) => a - b);
  
  const totalSeries = sortedYears.map(yr => yearlyData[yr].total);
  const diseaseSeries = sortedYears.map(yr => yearlyData[yr].disease);
  const naturalSeries = sortedYears.map(yr => yearlyData[yr].natural);
  const socialSeries = sortedYears.map(yr => yearlyData[yr].social);
  
  lineChart.data.labels = sortedYears;
  
  // Define datasets
  lineChart.data.datasets = [
    {
      label: 'Total Kematian',
      data: totalSeries,
      borderColor: COLORS.cyan,
      backgroundColor: 'rgba(6, 182, 212, 0.1)',
      borderWidth: 3,
      pointRadius: 4,
      pointHoverRadius: 6,
      fill: true,
      tension: 0.3
    },
    {
      label: 'Penyakit & Non-Alam',
      data: diseaseSeries,
      borderColor: COLORS.blue,
      backgroundColor: 'transparent',
      borderWidth: 2,
      pointRadius: 2,
      pointHoverRadius: 4,
      tension: 0.3,
      hidden: activeType !== 'all' && activeType !== 'Bencana Non Alam dan Penyakit'
    },
    {
      label: 'Bencana Alam',
      data: naturalSeries,
      borderColor: COLORS.amber,
      backgroundColor: 'transparent',
      borderWidth: 2,
      pointRadius: 2,
      pointHoverRadius: 4,
      tension: 0.3,
      hidden: activeType !== 'all' && activeType !== 'Bencana Alam'
    },
    {
      label: 'Bencana Sosial',
      data: socialSeries,
      borderColor: COLORS.rose,
      backgroundColor: 'transparent',
      borderWidth: 2,
      pointRadius: 2,
      pointHoverRadius: 4,
      tension: 0.3,
      hidden: activeType !== 'all' && activeType !== 'Bencana Sosial'
    }
  ];
  
  lineChart.update();
}

// 2. Update Doughnut Chart (Distribution)
function updateDoughnutChart(deathsByType) {
  const labels = ['Penyakit & Non-Alam', 'Bencana Alam', 'Bencana Sosial'];
  const dataValues = [
    deathsByType['Bencana Non Alam dan Penyakit'] || 0,
    deathsByType['Bencana Alam'] || 0,
    deathsByType['Bencana Sosial'] || 0
  ];
  
  doughnutChart.data.labels = labels;
  doughnutChart.data.datasets = [{
    data: dataValues,
    backgroundColor: [COLORS.blue, COLORS.amber, COLORS.rose],
    borderColor: COLORS.bgsecondary,
    borderWidth: 2,
    hoverOffset: 10
  }];
  
  doughnutChart.update();
}

// 3. Update Bar Chart (Top 10 Causes)
function updateBarChart(deathsByCause) {
  // Sort causes descending
  const sortedCauses = Object.entries(deathsByCause)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
    
  const labels = sortedCauses.map(c => {
    let name = c[0];
    return name.length > 25 ? name.substring(0, 23) + '...' : name;
  });
  const dataValues = sortedCauses.map(c => c[1]);
  
  barChart.data.labels = labels;
  barChart.data.datasets = [{
    data: dataValues,
    backgroundColor: 'rgba(6, 182, 212, 0.75)',
    hoverBackgroundColor: COLORS.cyan,
    borderRadius: 6,
    borderWidth: 0,
    barPercentage: 0.65
  }];
  
  barChart.update();
}

// Render paginated data table
function renderTable() {
  elTableBody.innerHTML = '';
  
  const totalItems = currentFilteredData.length;
  const totalPages = Math.ceil(totalItems / itemsPerPage) || 1;
  
  // Guard current page
  if (currentPage > totalPages) currentPage = totalPages;
  if (currentPage < 1) currentPage = 1;
  
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = Math.min(startIndex + itemsPerPage, totalItems);
  
  const pageItems = currentFilteredData.slice(startIndex, endIndex);
  
  if (pageItems.length === 0) {
    elTableBody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 2rem;">Tidak ada data yang cocok dengan filter</td></tr>`;
    elPageInfo.textContent = 'Halaman 0 dari 0';
    elPrevPage.disabled = true;
    elNextPage.disabled = true;
    return;
  }
  
  pageItems.forEach((d, idx) => {
    const tr = document.createElement('tr');
    
    // Category Badge style
    let badgeClass = 'disease';
    let typeDisplay = 'Penyakit & Non-Alam';
    if (d.type === 'Bencana Alam') {
      badgeClass = 'natural';
      typeDisplay = 'Bencana Alam';
    } else if (d.type === 'Bencana Sosial') {
      badgeClass = 'social';
      typeDisplay = 'Bencana Sosial';
    }
    
    tr.innerHTML = `
      <td style="font-weight: 500;">DOLLAR_OPEN{d.cause}</td>
      <td><span class="badge-type DOLLAR_OPEN{badgeClass}">DOLLAR_OPEN{typeDisplay}</span></td>
      <td class="td-year">DOLLAR_OPEN{d.year}</td>
      <td class="td-deaths">DOLLAR_OPEN{d.deaths.toLocaleString('id-ID')}</td>
      <td>
        <a class="source-link" href="DOLLAR_OPEN{d.url}" target="_blank">
          <svg style="width: 14px; height: 14px;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
          </svg>
          DOLLAR_OPEN{d.source.length > 28 ? d.source.substring(0, 25) + '...' : d.source}
        </a>
      </td>
    `;
    elTableBody.appendChild(tr);
  });
  
  // Update Pagination Controls
  elPageInfo.textContent = `Halaman DOLLAR_OPEN{currentPage} dari DOLLAR_OPEN{totalPages} (Total: DOLLAR_OPEN{totalItems.toLocaleString('id-ID')} baris)`;
  elPrevPage.disabled = currentPage === 1;
  elNextPage.disabled = currentPage === totalPages;
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', init);
"""

    # Replace DOLLAR_OPEN with actual $ sign
    js_code_body = js_code_body.replace('DOLLAR_OPEN', '$')

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write("const mortalityData = ")
        f.write(data_js_str)
        f.write(";\n\n")
        f.write(js_code_body)
        
    print("app.js has been compiled and saved successfully with embedded clean dataset!")

if __name__ == '__main__':
    build_app_js()
