import csv
import json
import os

csv_path = r"C:\Users\DELL\OneDrive\Desktop\Data-Visulization\Netflix.csv"
html_path = r"C:\Users\DELL\OneDrive\Desktop\Data-Visulization\netlify-site\index.html"

# Read CSV data
data = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Convert numeric types
        row['Rating'] = int(row['Rating'])
        row['Watch_Count'] = int(row['Watch_Count'])
        row['Watch_Time_Minutes'] = int(row['Watch_Time_Minutes'])
        row['Monthly_Revenue'] = int(row['Monthly_Revenue'])
        data.append(row)

data_json = json.dumps(data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Visualization Hub</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Manrope:wght@400;600;800&display=swap" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        :root {{
            --bg-dark: #090909;
            --bg-card: #141414;
            --text-main: #ffffff;
            --text-muted: #b3b3b3;
            --accent-red: #e50914;
            --accent-hover: #f40612;
            --border-color: #333333;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: 'DM Sans', sans-serif;
            line-height: 1.6;
        }}
        
        h1, h2, h3, h4, h5, h6, .brand {{
            font-family: 'Manrope', sans-serif;
        }}
        
        /* Navbar */
        nav {{
            position: sticky;
            top: 0;
            background-color: rgba(9, 9, 9, 0.95);
            backdrop-filter: blur(10px);
            padding: 15px 30px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            z-index: 1000;
        }}
        
        .brand {{
            color: var(--accent-red);
            font-size: 24px;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        
        /* Container */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px 30px;
        }}
        
        /* Hero Section */
        .hero {{
            background: linear-gradient(to right, rgba(229, 9, 20, 0.2), transparent);
            padding: 40px 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid rgba(229, 9, 20, 0.3);
        }}
        
        .hero h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        
        .hero p {{
            color: var(--text-muted);
            font-size: 18px;
        }}
        
        /* Filters */
        .filters {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-bottom: 30px;
            background: var(--bg-card);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        
        .filter-group {{
            display: flex;
            flex-direction: column;
            flex: 1;
            min-width: 150px;
        }}
        
        .filter-group label {{
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 5px;
            text-transform: uppercase;
            font-weight: bold;
        }}
        
        .filter-group select {{
            background-color: #222;
            color: white;
            border: 1px solid var(--border-color);
            padding: 10px;
            border-radius: 4px;
            font-family: inherit;
            outline: none;
            cursor: pointer;
        }}
        
        .filter-group select:focus {{
            border-color: var(--accent-red);
        }}
        
        /* Metric Cards */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            transition: transform 0.2s, border-color 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-red);
        }}
        
        .metric-title {{
            color: var(--text-muted);
            font-size: 14px;
            font-weight: 500;
        }}
        
        .metric-value {{
            font-size: 32px;
            font-weight: 800;
            color: var(--text-main);
            margin-top: 10px;
            font-family: 'Manrope', sans-serif;
        }}
        
        /* Charts Grid */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        @media (max-width: 992px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .chart-container {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            min-height: 350px;
        }}
        
        .chart-container h3 {{
            margin-bottom: 15px;
            font-size: 18px;
            color: var(--text-main);
            text-align: center;
        }}
        
        /* Insights */
        .insights-section {{
            margin-bottom: 30px;
        }}
        .insights-section h2 {{ margin-bottom: 20px; }}
        
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .insight-card {{
            background: linear-gradient(135deg, #2a0808 0%, var(--bg-card) 100%);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            text-align: center;
        }}
        .insight-card h4 {{ color: var(--text-muted); font-size: 14px; margin-bottom: 10px; }}
        .insight-card .val {{ font-size: 24px; font-weight: bold; color: var(--accent-red); }}
        
        /* Data Table */
        .table-section {{
            background: var(--bg-card);
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin-bottom: 30px;
            overflow-x: auto;
        }}
        
        .table-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        
        .search-box {{
            padding: 8px 15px;
            background: #222;
            border: 1px solid var(--border-color);
            color: white;
            border-radius: 4px;
            width: 250px;
        }}
        
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }}
        th, td {{ padding: 12px 15px; border-bottom: 1px solid var(--border-color); }}
        th {{ background: rgba(255,255,255,0.05); font-weight: 600; color: var(--text-muted); }}
        tr:hover {{ background: rgba(255,255,255,0.02); }}
        
        .pagination {{ display: flex; justify-content: flex-end; gap: 10px; margin-top: 15px; }}
        .pagination button {{
            background: #222; color: white; border: 1px solid var(--border-color); padding: 5px 12px; cursor: pointer; border-radius: 4px;
        }}
        .pagination button:hover {{ background: var(--accent-red); border-color: var(--accent-red); }}
        .pagination span {{ align-self: center; font-size: 14px; }}
        
        footer {{ text-align: center; padding: 20px; border-top: 1px solid var(--border-color); color: var(--text-muted); font-size: 14px; }}
    </style>
</head>
<body>
    <nav>
        <div class="brand">Data Visualization Hub</div>
    </nav>
    
    <div class="container">
        <div class="hero">
            <h1>Data Visualization Hub</h1>
            <p id="hero-stats">Loading dashboard data...</p>
        </div>
        
        <div class="filters">
            <div class="filter-group">
                <label>Type</label>
                <select id="filter-type"><option value="All">All Types</option></select>
            </div>
            <div class="filter-group">
                <label>Region</label>
                <select id="filter-region"><option value="All">All Regions</option></select>
            </div>
            <div class="filter-group">
                <label>Rating</label>
                <select id="filter-rating"><option value="All">All Ratings</option></select>
            </div>
            <div class="filter-group">
                <label>Category</label>
                <select id="filter-category"><option value="All">All Categories</option></select>
            </div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card"><div class="metric-title">Total Titles</div><div class="metric-value" id="m-titles">0</div></div>
            <div class="metric-card"><div class="metric-title">Movies</div><div class="metric-value" id="m-movies">0</div></div>
            <div class="metric-card"><div class="metric-title">TV Shows</div><div class="metric-value" id="m-shows">0</div></div>
            <div class="metric-card"><div class="metric-title">Regions</div><div class="metric-value" id="m-regions">0</div></div>
            <div class="metric-card"><div class="metric-title">Customers</div><div class="metric-value" id="m-customers">0</div></div>
            <div class="metric-card"><div class="metric-title">Categories</div><div class="metric-value" id="m-categories">0</div></div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container"><h3>Movies vs TV Shows</h3><div id="chart1"></div></div>
            <div class="chart-container"><h3>Viewing Activity by Month</h3><div id="chart2"></div></div>
            <div class="chart-container"><h3>Top Regions</h3><div id="chart3"></div></div>
            <div class="chart-container"><h3>Content Rating Distribution</h3><div id="chart4"></div></div>
            <div class="chart-container"><h3>Popular Categories</h3><div id="chart5"></div></div>
            <div class="chart-container"><h3>Movie vs TV Activity by Month</h3><div id="chart6"></div></div>
            <div class="chart-container"><h3>Revenue by Region</h3><div id="chart7"></div></div>
            <div class="chart-container"><h3>Average Rating by Subscription Plan</h3><div id="chart8"></div></div>
        </div>
        
        <div class="insights-section">
            <h2>Key Insights</h2>
            <div class="insights-grid">
                <div class="insight-card"><h4>Most Common Format</h4><div class="val" id="i-format">-</div></div>
                <div class="insight-card"><h4>Busiest Watch Month</h4><div class="val" id="i-month">-</div></div>
                <div class="insight-card"><h4>Top Region</h4><div class="val" id="i-region">-</div></div>
                <div class="insight-card"><h4>Most Common Rating</h4><div class="val" id="i-rating">-</div></div>
                <div class="insight-card"><h4>Popular Category</h4><div class="val" id="i-category">-</div></div>
            </div>
        </div>
        
        <div class="table-section">
            <div class="table-header">
                <h2>Data Explorer</h2>
                <input type="text" class="search-box" id="table-search" placeholder="Search titles, customers...">
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Customer</th>
                        <th>Title</th>
                        <th>Type</th>
                        <th>Category</th>
                        <th>Region</th>
                        <th>Date</th>
                        <th>Revenue</th>
                    </tr>
                </thead>
                <tbody id="table-body"></tbody>
            </table>
            <div class="pagination">
                <button id="btn-prev">Previous</button>
                <span id="page-info">Page 1 of 1</span>
                <button id="btn-next">Next</button>
            </div>
        </div>
    </div>
    
    <footer>
        &copy; 2026 Data Visualization Hub. Built with Plotly.js.
    </footer>

    <script>
        const rawData = {data_json};
        const palette = ["#e50914", "#f05d5e", "#ff9c74", "#f5c36a", "#72c7b5", "#8ea5ff", "#c18aff", "#d4d4d8"];
        
        // State
        let filteredData = [...rawData];
        let currentPage = 1;
        const rowsPerPage = 10;
        let searchQuery = "";
        
        // Init Filters
        function initFilters() {{
            const types = [...new Set(rawData.map(d => d.Type))].sort();
            const regions = [...new Set(rawData.map(d => d.Region))].sort();
            const ratings = [...new Set(rawData.map(d => d.Rating))].sort((a,b)=>a-b);
            const categories = [...new Set(rawData.map(d => d.Category))].sort();
            
            const popFilter = (id, vals) => {{
                const sel = document.getElementById(id);
                vals.forEach(v => {{
                    const opt = document.createElement('option');
                    opt.value = v; opt.textContent = v;
                    sel.appendChild(opt);
                }});
                sel.addEventListener('change', applyFilters);
            }};
            
            popFilter('filter-type', types);
            popFilter('filter-region', regions);
            popFilter('filter-rating', ratings);
            popFilter('filter-category', categories);
            
            document.getElementById('table-search').addEventListener('input', (e) => {{
                searchQuery = e.target.value.toLowerCase();
                currentPage = 1;
                renderTable();
            }});
            
            document.getElementById('btn-prev').addEventListener('click', () => {{
                if(currentPage > 1) {{ currentPage--; renderTable(); }}
            }});
            document.getElementById('btn-next').addEventListener('click', () => {{
                const max = Math.ceil(tableData().length / rowsPerPage);
                if(currentPage < max) {{ currentPage++; renderTable(); }}
            }});
        }}
        
        function applyFilters() {{
            const t = document.getElementById('filter-type').value;
            const r = document.getElementById('filter-region').value;
            const rt = document.getElementById('filter-rating').value;
            const c = document.getElementById('filter-category').value;
            
            filteredData = rawData.filter(d => {{
                return (t === 'All' || d.Type === t) &&
                       (r === 'All' || d.Region === r) &&
                       (rt === 'All' || d.Rating.toString() === rt) &&
                       (c === 'All' || d.Category === c);
            }});
            
            currentPage = 1;
            updateDashboard();
        }}
        
        // GroupBy Helper
        function groupBy(data, key) {{
            return data.reduce((acc, curr) => {{
                acc[curr[key]] = (acc[curr[key]] || 0) + 1;
                return acc;
            }}, {{}});
        }}
        function sumBy(data, groupKey, sumKey) {{
            return data.reduce((acc, curr) => {{
                acc[curr[groupKey]] = (acc[curr[groupKey]] || 0) + curr[sumKey];
                return acc;
            }}, {{}});
        }}
        function avgBy(data, groupKey, valKey) {{
            const sums = data.reduce((acc, curr) => {{
                if(!acc[curr[groupKey]]) acc[curr[groupKey]] = {{ sum: 0, count: 0 }};
                acc[curr[groupKey]].sum += curr[valKey];
                acc[curr[groupKey]].count += 1;
                return acc;
            }}, {{}});
            const res = {{}};
            for(let k in sums) res[k] = sums[k].sum / sums[k].count;
            return res;
        }}

        // Layout config for Plotly
        const layoutBase = {{
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {{ color: '#b3b3b3', family: 'DM Sans' }},
            margin: {{ t: 20, r: 20, l: 40, b: 40 }},
            xaxis: {{ gridcolor: '#333' }},
            yaxis: {{ gridcolor: '#333' }},
            showlegend: false
        }};
        
        function drawCharts() {{
            const d = filteredData;
            
            // 1. Movie vs TV (Pie)
            const typeCounts = groupBy(d, 'Type');
            Plotly.newPlot('chart1', [{{
                values: Object.values(typeCounts),
                labels: Object.keys(typeCounts),
                type: 'pie',
                hole: 0.5,
                marker: {{ colors: [palette[0], palette[7]] }}
            }}], {{ ...layoutBase, showlegend: true }});
            
            // 2. Viewing by Month
            // Extract month-year
            const monthCounts = {{}};
            d.forEach(row => {{
                const m = row.Watch_Date.substring(0,7);
                monthCounts[m] = (monthCounts[m] || 0) + 1;
            }});
            const sortedMonths = Object.keys(monthCounts).sort();
            Plotly.newPlot('chart2', [{{
                x: sortedMonths,
                y: sortedMonths.map(m => monthCounts[m]),
                type: 'scatter',
                fill: 'tozeroy',
                line: {{ color: palette[0] }}
            }}], layoutBase);
            
            // 3. Top Regions
            const regCounts = groupBy(d, 'Region');
            Plotly.newPlot('chart3', [{{
                x: Object.values(regCounts),
                y: Object.keys(regCounts),
                type: 'bar',
                orientation: 'h',
                marker: {{ color: palette[1] }}
            }}], layoutBase);
            
            // 4. Rating Distribution
            const ratingCounts = groupBy(d, 'Rating');
            Plotly.newPlot('chart4', [{{
                x: Object.keys(ratingCounts),
                y: Object.values(ratingCounts),
                type: 'bar',
                marker: {{ color: palette[2] }}
            }}], layoutBase);
            
            // 5. Popular Categories
            const catCounts = groupBy(d, 'Category');
            // Sort categories
            const sortedCats = Object.keys(catCounts).sort((a,b)=>catCounts[a]-catCounts[b]);
            Plotly.newPlot('chart5', [{{
                x: sortedCats.map(c => catCounts[c]),
                y: sortedCats,
                type: 'bar',
                orientation: 'h',
                marker: {{ color: palette[4] }}
            }}], layoutBase);
            
            // 6. Stacked Bar Activity
            const months = [...new Set(d.map(r => r.Watch_Date.substring(0,7)))].sort();
            const movData = months.map(m => d.filter(r => r.Watch_Date.substring(0,7) === m && r.Type === 'Movie').length);
            const tvData = months.map(m => d.filter(r => r.Watch_Date.substring(0,7) === m && r.Type === 'TV Show').length);
            Plotly.newPlot('chart6', [
                {{ x: months, y: movData, name: 'Movie', type: 'bar', marker: {{color: palette[0]}} }},
                {{ x: months, y: tvData, name: 'TV Show', type: 'bar', marker: {{color: palette[7]}} }}
            ], {{ ...layoutBase, barmode: 'stack', showlegend: true }});
            
            // 7. Revenue by Region
            const revReg = sumBy(d, 'Region', 'Monthly_Revenue');
            Plotly.newPlot('chart7', [{{
                x: Object.values(revReg),
                y: Object.keys(revReg),
                type: 'bar',
                orientation: 'h',
                marker: {{ color: palette[5] }}
            }}], layoutBase);
            
            // 8. Avg Rating by Plan
            const avgRatPlan = avgBy(d, 'Subscription_Plan', 'Rating');
            Plotly.newPlot('chart8', [{{
                x: Object.keys(avgRatPlan),
                y: Object.values(avgRatPlan),
                type: 'bar',
                marker: {{ color: palette[6] }}
            }}], layoutBase);
        }}
        
        function updateInsights() {{
            const d = filteredData;
            if(d.length === 0) return;
            
            const most = (obj) => Object.keys(obj).reduce((a, b) => obj[a] > obj[b] ? a : b);
            
            document.getElementById('i-format').textContent = most(groupBy(d, 'Type'));
            
            const monthCounts = groupBy(d.map(x => ({{m: x.Watch_Date.substring(0,7)}})), 'm');
            document.getElementById('i-month').textContent = most(monthCounts);
            
            document.getElementById('i-region').textContent = most(groupBy(d, 'Region'));
            document.getElementById('i-rating').textContent = most(groupBy(d, 'Rating'));
            document.getElementById('i-category').textContent = most(groupBy(d, 'Category'));
        }}
        
        function tableData() {{
            if(!searchQuery) return filteredData;
            return filteredData.filter(r => 
                r.Title.toLowerCase().includes(searchQuery) || 
                r.Customer_Name.toLowerCase().includes(searchQuery)
            );
        }}
        
        function renderTable() {{
            const data = tableData();
            const start = (currentPage - 1) * rowsPerPage;
            const end = start + rowsPerPage;
            const pageData = data.slice(start, end);
            
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';
            
            pageData.forEach(row => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${{row.Customer_Name}}</td>
                    <td>${{row.Title}}</td>
                    <td>${{row.Type}}</td>
                    <td>${{row.Category}}</td>
                    <td>${{row.Region}}</td>
                    <td>${{row.Watch_Date}}</td>
                    <td>$${{row.Monthly_Revenue}}</td>
                `;
                tbody.appendChild(tr);
            }});
            
            const maxPage = Math.ceil(data.length / rowsPerPage) || 1;
            document.getElementById('page-info').textContent = `Page ${{currentPage}} of ${{maxPage}}`;
        }}
        
        function updateDashboard() {{
            const d = filteredData;
            
            // Hero Stats
            const totalRec = d.length;
            const distTitles = new Set(d.map(x=>x.Title)).size;
            document.getElementById('hero-stats').textContent = `${{totalRec}} Records | ${{distTitles}} Distinct Titles`;
            
            // Metrics
            document.getElementById('m-titles').textContent = distTitles;
            document.getElementById('m-movies').textContent = d.filter(x=>x.Type==='Movie').length;
            document.getElementById('m-shows').textContent = d.filter(x=>x.Type==='TV Show').length;
            document.getElementById('m-regions').textContent = new Set(d.map(x=>x.Region)).size;
            document.getElementById('m-customers').textContent = new Set(d.map(x=>x.Customer_ID)).size;
            document.getElementById('m-categories').textContent = new Set(d.map(x=>x.Category)).size;
            
            drawCharts();
            updateInsights();
            renderTable();
        }}
        
        // Init
        initFilters();
        updateDashboard();
        
        // Responsive chart resize
        window.addEventListener('resize', () => {{
            const ids = ['chart1','chart2','chart3','chart4','chart5','chart6','chart7','chart8'];
            ids.forEach(id => Plotly.Plots.resize(id));
        }});
    </script>
</body>
</html>
"""

os.makedirs(os.path.dirname(html_path), exist_ok=True)
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully generated {html_path}")
