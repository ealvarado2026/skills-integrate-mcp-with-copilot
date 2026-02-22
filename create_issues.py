#!/usr/bin/env python3
"""
Script to create GitHub issues for new features.
Requires GITHUB_TOKEN environment variable to be set.

Usage:
    export GITHUB_TOKEN="your_github_token"
    python3 create_issues.py
"""

import os
import json
import urllib.request
import urllib.error
import sys

# Configuration
OWNER = "ealvarado2026"
REPO = "skills-integrate-mcp-with-copilot"
TOKEN = os.getenv("GITHUB_TOKEN")

# Issues to create
ISSUES = [
    {
        "title": "User Registration & Authentication System",
        "body": """Add user registration and login system with:
- User registration with role selection (Student, Club Leader, Administrator)
- Login/logout functionality
- Password management and password recovery
- User profile management with personal information
- Student-specific fields (course, year, department, phone)
- Session management
- Password change functionality with validation"""
    },
    {
        "title": "Club & Organization Management",
        "body": """Implement club/organization management features:
- Create and manage multiple clubs/organizations
- Club profiles with descriptions, categories, and locations
- Team creation within clubs
- Member role assignment (President, Manager, Member)
- Member invitation and addition to teams
- Display detailed member information
- Member status tracking"""
    },
    {
        "title": "Enhanced Event Management System",
        "body": """Expand event management beyond simple signup:
- Event type categorization (meetings, workshops, competitions, fundraisers, etc.)
- Event status tracking (draft, published, ongoing, completed, cancelled)
- Registration deadlines for events
- Event fee/payment collection (support amounts up to $9,999)
- Attendance capacity management with max participant limits
- Location tracking for events
- RSVP and attendance tracking (more detailed than current signup)
- Event scheduling with detailed date/time information"""
    },
    {
        "title": "Financial & Budget Management",
        "body": """Add financial tracking features:
- Transaction tracking (income/expenses categorization)
- Multiple payment method support (cash, bank transfer, card, cheque, online)
- Receipt file uploads for documentation
- Budget monitoring and forecasting
- Financial reporting and approval workflows
- Transaction status tracking (pending, approved, rejected)
- Financial metrics and analytics"""
    },
    {
        "title": "Communication & Notification System",
        "body": """Implement club communication features:
- Messaging system between club members
- Announcements/notifications for club activities
- Email notification capabilities
- Activity alerts and reminders
- Communication hub for member engagement
- Notification preferences per user"""
    },
    {
        "title": "Analytics & Reporting Dashboard",
        "body": """Create comprehensive dashboard and reporting:
- Dashboard with system statistics
- Real-time analytics on club activities
- Financial reports and visualizations
- Activity tracking and metrics
- Member engagement analytics
- Charts and graphs for data visualization
- Exportable reports (PDF, CSV)"""
    },
    {
        "title": "Role-Based Access Control (RBAC)",
        "body": """Implement permission system based on user roles:
- Admin: Full system access, manage all clubs and users
- Club Manager/President: Manage club members, create events, handle finances
- Member: View club info, register for events, view announcements
- Permission-based operations and data access
- Role hierarchy and inheritance"""
    },
    {
        "title": "Professional UI/UX Redesign",
        "body": """Upgrade user interface to enterprise-grade:
- Modern dark theme with gradient accents
- Responsive mobile design (desktop, tablet, mobile)
- Professional animations and transitions
- Polished component design
- Glassmorphism effects
- Improved accessibility
- Consistent design system
- Cross-browser compatibility"""
    },
    {
        "title": "Database & Data Persistence",
        "body": """Replace in-memory storage with persistent database:
- Implement database schema (Users, Clubs, Members, Events, Tasks, Finances)
- Data relationships and foreign keys
- Query optimization with proper indexing
- Database migration support
- Backup and recovery functionality
- Data validation and integrity checks"""
    }
]


def create_issue(issue_title, issue_body):
    """Create a GitHub issue using the REST API."""
    if not TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable not set!")
        print("Please set your GitHub token: export GITHUB_TOKEN='your_token'")
        return False

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    
    data = {
        "title": issue_title,
        "body": issue_body
    }
    
    json_data = json.dumps(data).encode('utf-8')
    
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "GitHub-Issue-Creator"
    }
    
    try:
        req = urllib.request.Request(url, data=json_data, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            issue_number = result.get('number')
            issue_url = result.get('html_url')
            print(f"✅ Created issue #{issue_number}: {issue_title}")
            print(f"   URL: {issue_url}\n")
            return True
    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8'))
        error_message = error_data.get('message', str(e))
        print(f"❌ Failed to create issue: {issue_title}")
        print(f"   Error: {error_message}\n")
        return False
    except Exception as e:
        print(f"❌ Error creating issue: {issue_title}")
        print(f"   Exception: {str(e)}\n")
        return False


def main():
    """Main function to create all issues."""
    if not TOKEN:
        print("=" * 60)
        print("GitHub Issue Creator")
        print("=" * 60)
        print("\nERROR: GITHUB_TOKEN environment variable is not set!")
        print("\nTo use this script:")
        print("1. Generate a GitHub personal access token")
        print("   (https://github.com/settings/tokens)")
        print("2. Set it as an environment variable:")
        print("   export GITHUB_TOKEN='your_token_here'")
        print("3. Run this script again:")
        print("   python3 create_issues.py")
        sys.exit(1)
    
    print("=" * 60)
    print("GitHub Issue Creator")
    print("=" * 60)
    print(f"Repository: {OWNER}/{REPO}")
    print(f"Total issues to create: {len(ISSUES)}\n")
    
    successful = 0
    failed = 0
    
    for issue in ISSUES:
        if create_issue(issue["title"], issue["body"]):
            successful += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"Results: {successful} created, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
