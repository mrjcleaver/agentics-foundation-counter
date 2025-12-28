# Reddit Analytics Quick Start Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Basic usage (24 months of data):**
   ```bash
   python reddit_analytics.py claude-flow
   ```

3. **Custom time range (e.g., 12 months):**
   ```bash
   python reddit_analytics.py --months 12 claude-flow
   ```

4. **Export to CSV:**
   ```bash
   python reddit_analytics.py --format csv --output report.csv claude-flow
   ```

## Common Use Cases

### Monthly Trend Analysis
Track mentions over the past year:
```bash
python reddit_analytics.py --months 12 claude-flow
```

### Quick Check (Last 3 Months)
```bash
python reddit_analytics.py --months 3 --delay 0.5 claude-flow
```

### Data Export for Spreadsheet Analysis
```bash
python reddit_analytics.py --months 24 --format csv --output claude_flow_2025.csv claude-flow
```

### Compare Multiple Projects
Run the tool for different projects and compare:
```bash
python reddit_analytics.py --format csv --output project_a.csv project-a
python reddit_analytics.py --format csv --output project_b.csv project-b
```

## Understanding the Output

### Text Format
```
======================================================================
Reddit Analytics Report: 'claude-flow'
Time Period: 24 months
======================================================================

Month          Posts Only   Posts + Comments
----------------------------------------------------------------------
2023-12                 5                 18
2024-01                 8                 25
...
----------------------------------------------------------------------
TOTAL                 120                456
======================================================================

Total Posts: 120
Total Comments: 336
Total Combined: 456
```

- **Posts Only**: Number of Reddit posts mentioning the search term
- **Posts + Comments**: Total mentions (posts + comments)
- **TOTAL**: Aggregate counts across all months

### CSV Format
```csv
Month,Posts Only,Posts + Comments
2023-12,5,18
2024-01,8,25
TOTAL,120,456
```

Easily imported into Excel, Google Sheets, or data analysis tools.

## Tips

1. **Rate Limiting**: Use `--delay` to control API request frequency
   - Default: 1 second between requests
   - For faster results: `--delay 0.5`
   - For conservative rate limiting: `--delay 2.0`

2. **Search Terms**: Use exact phrases for more accurate results
   - Good: `claude-flow`
   - Also works: `"claude flow"` (with quotes in shell)

3. **Data Limitations**: 
   - Pushshift API (default) may be unavailable (discontinued in 2023)
   - Reddit official API (--use-reddit-api) has limited comment search
   - Results show 0 when API is unavailable - this is expected behavior

4. **Long Running Queries**: 24-month analysis can take 1-2 minutes
   - Be patient
   - Progress shown for each month
   - Use Ctrl+C to interrupt if needed

## Troubleshooting

### No Results / All Zeros
- API may be unavailable (Pushshift discontinued)
- Check internet connectivity
- Try `--use-reddit-api` flag for alternative data source

### Slow Performance
- Increase delay: `--delay 2.0`
- Reduce time window: `--months 12`
- Check network connectivity

### API Errors
- Script handles errors gracefully
- Returns 0 for unavailable data
- Check warnings in stderr output

## Next Steps

For production use with full functionality, consider:
1. Using PRAW (Python Reddit API Wrapper) library
2. Implementing Reddit OAuth authentication
3. Setting up scheduled analysis runs
4. Creating visualizations from CSV output
