# Reddit Analytics Utility

A lightweight analytics tool for measuring awareness and adoption of projects on Reddit over time. Query archived Reddit data month-by-month over a rolling 24-month window to track mentions and identify trends.

## Features

- **Historical Analysis**: Query up to 24 months of Reddit data
- **Granular Metrics**: Track mentions in posts only, or posts + comments
- **Monthly Breakdowns**: See trends over time with month-by-month statistics
- **Aggregate Totals**: Get overall statistics across the entire time period
- **Multiple Output Formats**: Export results as human-readable text or CSV
- **Configurable**: Adjust time windows and rate limiting

## Problem Statement

Ad-hoc Reddit searches are inconsistent, non-auditable, and don't support trend analysis. This tool provides a reliable, repeatable way to measure project awareness on Reddit over time.

## Solution

This utility queries archived Reddit data using the Pushshift API and reports:
- Mentions in posts only
- Mentions in posts + comments
- Monthly and aggregate totals

**Note**: This tool is designed for trend detection, not sentiment analysis.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/mrjcleaver/agentics-foundation-counter.git
cd agentics-foundation-counter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Search for mentions of "claude-flow" over the past 24 months:

```bash
python reddit_analytics.py claude-flow
```

### Custom Time Window

Analyze the past 12 months:

```bash
python reddit_analytics.py --months 12 claude-flow
```

### CSV Export

Export results to CSV format:

```bash
python reddit_analytics.py --format csv --output report.csv claude-flow
```

### Adjust Rate Limiting

Change the delay between API calls (default is 1 second):

```bash
python reddit_analytics.py --delay 2.0 claude-flow
```

## Command-Line Options

```
usage: reddit_analytics.py [-h] [--months MONTHS] [--format {text,csv}]
                          [--output OUTPUT] [--delay DELAY]
                          search_term

Arguments:
  search_term          Term to search for on Reddit (e.g., "claude-flow")

Options:
  -h, --help           Show help message and exit
  --months MONTHS      Number of months to analyze (default: 24)
  --format {text,csv}  Output format (default: text)
  --output OUTPUT      Output file path (default: stdout)
  --delay DELAY        Delay between API calls in seconds (default: 1.0)
```

## Example Output

### Text Format

```
======================================================================
Reddit Analytics Report: 'claude-flow'
Time Period: 24 months
======================================================================

Month              Posts Only   Posts + Comments
----------------------------------------------------------------------
2023-01                    0                  0
2023-02                    1                  3
2023-03                    2                  7
...
2024-12                    5                 18
----------------------------------------------------------------------
TOTAL                     45                156
======================================================================

Total Posts: 45
Total Comments: 111
Total Combined: 156
```

### CSV Format

```csv
Month,Posts Only,Posts + Comments
2023-01,0,0
2023-02,1,3
2023-03,2,7
...
2024-12,5,18
TOTAL,45,156
```

## Use Cases

- **Trend Analysis**: Track project awareness growth over time
- **Launch Impact**: Measure visibility changes after releases or announcements
- **Community Engagement**: Monitor discussion volume in posts vs. comments
- **Competitive Analysis**: Compare mention volumes across different projects
- **Reporting**: Generate consistent, auditable metrics for stakeholders

## Technical Details

- **Data Source**: Pushshift API (Reddit Archive)
- **Time Window**: Rolling 24-month window (configurable)
- **Rate Limiting**: Built-in delays between API calls to respect rate limits
- **Error Handling**: Graceful handling of API failures and network issues

## Limitations

- Depends on the availability of the Pushshift API
- Historical data may have gaps depending on API coverage
- Does not perform sentiment analysis
- Rate limits may slow down queries for very large time windows

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available for use.