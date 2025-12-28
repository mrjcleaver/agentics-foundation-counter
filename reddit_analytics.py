#!/usr/bin/env python3
"""
Reddit Analytics Utility
Measures awareness and adoption of projects on Reddit over time.
Queries archived Reddit data month-by-month over a rolling 24-month window.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import time
from typing import Dict, List, Tuple


class RedditAnalytics:
    """Analytics utility for tracking project mentions on Reddit."""
    
    def __init__(self, search_term: str, use_reddit_api: bool = False):
        """
        Initialize the analytics utility.
        
        Args:
            search_term: The term to search for in Reddit posts and comments
            use_reddit_api: If True, use Reddit's official API instead of Pushshift
        """
        self.search_term = search_term
        self.use_reddit_api = use_reddit_api
        
        if use_reddit_api:
            # Reddit's official API endpoints
            self.base_url = "https://www.reddit.com"
        else:
            # Pushshift API (archived data - may be unavailable)
            # Note: Pushshift API was discontinued in 2023
            # This is kept for historical compatibility
            self.base_url = "https://api.pushshift.io/reddit"
        
    def get_month_timestamps(self, months_back: int = 24) -> List[Tuple[int, int, str]]:
        """
        Generate timestamps for each month in the rolling window.
        
        Args:
            months_back: Number of months to go back (default: 24)
            
        Returns:
            List of tuples (start_timestamp, end_timestamp, month_label)
        """
        timestamps = []
        end_date = datetime.now()
        
        for i in range(months_back):
            month_end = end_date - relativedelta(months=i)
            month_start = month_end - relativedelta(months=1)
            
            # Convert to Unix timestamps
            start_ts = int(month_start.timestamp())
            end_ts = int(month_end.timestamp())
            
            # Format label as YYYY-MM
            label = month_start.strftime("%Y-%m")
            
            timestamps.append((start_ts, end_ts, label))
        
        # Reverse to show oldest first
        return list(reversed(timestamps))
    
    def search_submissions(self, after: int, before: int) -> int:
        """
        Search for mentions in Reddit submissions (posts) for a time period.
        
        Args:
            after: Start timestamp
            before: End timestamp
            
        Returns:
            Count of submissions mentioning the search term
        """
        if self.use_reddit_api:
            return self._search_reddit_api_submissions(after, before)
        else:
            return self._search_pushshift_submissions(after, before)
    
    def _search_pushshift_submissions(self, after: int, before: int) -> int:
        """Search using Pushshift API (may be unavailable)."""
        url = f"{self.base_url}/search/submission/"
        params = {
            'q': self.search_term,
            'after': after,
            'before': before,
            'size': 0,  # We only want the count
            'metadata': 'true'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract total count from metadata
            if 'metadata' in data and 'total_results' in data['metadata']:
                return data['metadata']['total_results']
            return 0
        except requests.exceptions.RequestException as e:
            print(f"Warning: Error fetching submissions: {e}", file=sys.stderr)
            return 0
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Warning: Error parsing response: {e}", file=sys.stderr)
            return 0
    
    def _search_reddit_api_submissions(self, after: int, before: int) -> int:
        """
        Search using Reddit's official API.
        Note: This requires authentication for production use.
        """
        # Reddit's search API endpoint
        url = f"{self.base_url}/search.json"
        params = {
            'q': self.search_term,
            'type': 'link',
            'limit': 100,
            'sort': 'new'
        }
        headers = {
            'User-Agent': 'Reddit Analytics Utility/1.0'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Filter by time range and count
            count = 0
            if 'data' in data and 'children' in data['data']:
                for post in data['data']['children']:
                    created_utc = post['data'].get('created_utc', 0)
                    if after <= created_utc <= before:
                        count += 1
            
            return count
        except requests.exceptions.RequestException as e:
            print(f"Warning: Error fetching submissions: {e}", file=sys.stderr)
            return 0
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Warning: Error parsing response: {e}", file=sys.stderr)
            return 0
    
    def search_comments(self, after: int, before: int) -> int:
        """
        Search for mentions in Reddit comments for a time period.
        
        Args:
            after: Start timestamp
            before: End timestamp
            
        Returns:
            Count of comments mentioning the search term
        """
        if self.use_reddit_api:
            return self._search_reddit_api_comments(after, before)
        else:
            return self._search_pushshift_comments(after, before)
    
    def _search_pushshift_comments(self, after: int, before: int) -> int:
        """Search comments using Pushshift API (may be unavailable)."""
        url = f"{self.base_url}/search/comment/"
        params = {
            'q': self.search_term,
            'after': after,
            'before': before,
            'size': 0,  # We only want the count
            'metadata': 'true'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract total count from metadata
            if 'metadata' in data and 'total_results' in data['metadata']:
                return data['metadata']['total_results']
            return 0
        except requests.exceptions.RequestException as e:
            print(f"Warning: Error fetching comments: {e}", file=sys.stderr)
            return 0
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Warning: Error parsing response: {e}", file=sys.stderr)
            return 0
    
    def _search_reddit_api_comments(self, after: int, before: int) -> int:
        """
        Search comments using Reddit's official API.
        Note: Reddit's API doesn't provide direct comment search,
        so this returns 0 (comments would need to be fetched from posts).
        For full comment search, consider using PRAW or other Reddit libraries.
        """
        # Reddit's API doesn't support direct comment search
        # This would require fetching posts and then comments from each
        # For now, return 0 as a placeholder
        print(f"Note: Comment search not available with Reddit API", file=sys.stderr)
        return 0
    
    def analyze(self, months_back: int = 24, delay: float = 1.0) -> Dict:
        """
        Analyze Reddit mentions over the specified time period.
        
        Args:
            months_back: Number of months to analyze (default: 24)
            delay: Delay between API calls in seconds (default: 1.0)
            
        Returns:
            Dictionary containing monthly and aggregate statistics
        """
        print(f"Analyzing Reddit mentions of '{self.search_term}' over {months_back} months...")
        print()
        
        month_timestamps = self.get_month_timestamps(months_back)
        monthly_data = []
        
        total_posts = 0
        total_comments = 0
        
        for start_ts, end_ts, label in month_timestamps:
            print(f"Fetching data for {label}...", end='', flush=True)
            
            # Get post mentions
            posts_count = self.search_submissions(start_ts, end_ts)
            time.sleep(delay)  # Rate limiting
            
            # Get comment mentions
            comments_count = self.search_comments(start_ts, end_ts)
            time.sleep(delay)  # Rate limiting
            
            combined_count = posts_count + comments_count
            
            monthly_data.append({
                'month': label,
                'posts_only': posts_count,
                'posts_and_comments': combined_count
            })
            
            total_posts += posts_count
            total_comments += comments_count
            
            print(f" Posts: {posts_count}, Total: {combined_count}")
        
        return {
            'search_term': self.search_term,
            'time_period': f"{months_back} months",
            'monthly_data': monthly_data,
            'aggregate': {
                'total_posts': total_posts,
                'total_comments': total_comments,
                'total_combined': total_posts + total_comments
            }
        }
    
    def format_report(self, results: Dict, output_format: str = 'text') -> str:
        """
        Format the analysis results for output.
        
        Args:
            results: Analysis results dictionary
            output_format: Output format ('text' or 'csv')
            
        Returns:
            Formatted report string
        """
        if output_format == 'csv':
            return self._format_csv(results)
        else:
            return self._format_text(results)
    
    def _format_text(self, results: Dict) -> str:
        """Format results as human-readable text."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"Reddit Analytics Report: '{results['search_term']}'")
        lines.append(f"Time Period: {results['time_period']}")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"{'Month':<12} {'Posts Only':>12} {'Posts + Comments':>18}")
        lines.append("-" * 70)
        
        for month_data in results['monthly_data']:
            lines.append(
                f"{month_data['month']:<12} "
                f"{month_data['posts_only']:>12} "
                f"{month_data['posts_and_comments']:>18}"
            )
        
        lines.append("-" * 70)
        agg = results['aggregate']
        lines.append(
            f"{'TOTAL':<12} "
            f"{agg['total_posts']:>12} "
            f"{agg['total_combined']:>18}"
        )
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Total Posts: {agg['total_posts']}")
        lines.append(f"Total Comments: {agg['total_comments']}")
        lines.append(f"Total Combined: {agg['total_combined']}")
        
        return '\n'.join(lines)
    
    def _format_csv(self, results: Dict) -> str:
        """Format results as CSV."""
        lines = []
        lines.append("Month,Posts Only,Posts + Comments")
        
        for month_data in results['monthly_data']:
            lines.append(
                f"{month_data['month']},"
                f"{month_data['posts_only']},"
                f"{month_data['posts_and_comments']}"
            )
        
        agg = results['aggregate']
        lines.append(f"TOTAL,{agg['total_posts']},{agg['total_combined']}")
        
        return '\n'.join(lines)


def main():
    """Main entry point for the Reddit analytics utility."""
    parser = argparse.ArgumentParser(
        description='Analyze Reddit mentions of a project over time',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s claude-flow
  %(prog)s --months 12 --format csv claude-flow
  %(prog)s --output report.csv --format csv claude-flow
        """
    )
    
    parser.add_argument(
        'search_term',
        help='Term to search for on Reddit (e.g., "claude-flow")'
    )
    
    parser.add_argument(
        '--months',
        type=int,
        default=24,
        help='Number of months to analyze (default: 24)'
    )
    
    parser.add_argument(
        '--format',
        choices=['text', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: stdout)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between API calls in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '--use-reddit-api',
        action='store_true',
        help='Use Reddit\'s official API instead of Pushshift (limited functionality)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.months < 1 or args.months > 60:
        print("Error: months must be between 1 and 60", file=sys.stderr)
        sys.exit(1)
    
    # Run analysis
    try:
        analyzer = RedditAnalytics(args.search_term, use_reddit_api=args.use_reddit_api)
        results = analyzer.analyze(months_back=args.months, delay=args.delay)
        report = analyzer.format_report(results, output_format=args.format)
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"\nReport saved to {args.output}")
        else:
            print()
            print(report)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
