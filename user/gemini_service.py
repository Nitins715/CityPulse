import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import google.generativeai as genai
from django.conf import settings
import json

class GeminiService:
    """Service class for interacting with Gemini API"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Using the generic alias to route to the best available Flash model
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    def classify_issue(self, title, description, address):
        """
        Classify the civic issue using Gemini AI
        Returns: dict with issue_type, priority, and analysis
        """
        
        prompt = f"""
        You are an AI assistant helping to classify civic issues for a city management system.
        
        Analyze the following civic issue report and provide:
        1. Issue Type (choose one): POTHOLE, ELECTRICITY, WATER, GARBAGE, STREETLIGHT, DRAINAGE, ROAD, OTHER
        2. Priority Level (choose one): LOW, MEDIUM, HIGH, CRITICAL
        3. Brief Analysis (2-3 sentences explaining the issue and recommended action)
        
        Issue Details:
        Title: {title}
        Description: {description}
        Location: {address}
        
        Respond ONLY with a JSON object in this exact format:
        {{
            "issue_type": "TYPE_HERE",
            "priority": "PRIORITY_HERE",
            "analysis": "Your analysis here"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.startswith('```'):
                result_text = result_text[3:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]
            
            result_text = result_text.strip()
            
            # Parse JSON response
            result = json.loads(result_text)
            
            return {
                'issue_type': result.get('issue_type', 'OTHER'),
                'priority': result.get('priority', 'MEDIUM'),
                'analysis': result.get('analysis', 'AI analysis not available')
            }
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print("Gemini API Quota Exceeded (429)")
                return {
                    'issue_type': 'OTHER',
                    'priority': 'MEDIUM',
                    'analysis': 'AI unavailable: Rate limit exceeded. Please try again later.'
                }
            print(f"Error in Gemini classification: {error_msg}")
            return {
                'issue_type': 'OTHER',
                'priority': 'MEDIUM',
                'analysis': 'AI classification currently unavailable.'
            }
    
    def generate_authority_report(self, issues_queryset):
        """
        Generate a summary report for authority dashboard
        """
        
        # Prepare issue statistics
        total_issues = issues_queryset.count()
        pending_issues = issues_queryset.filter(status='PENDING').count()
        in_progress_issues = issues_queryset.filter(status='IN_PROGRESS').count()
        resolved_issues = issues_queryset.filter(status='RESOLVED').count()
        
        # Get issue type breakdown
        issue_types = {}
        for issue in issues_queryset:
            issue_type = issue.issue_type
            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
        
        # Get priority breakdown
        priority_breakdown = {}
        for issue in issues_queryset:
            priority = issue.priority
            priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
        
        prompt = f"""
        Generate a brief executive summary for city authorities based on the following civic issues data:
        
        Total Issues: {total_issues}
        Pending: {pending_issues}
        In Progress: {in_progress_issues}
        Resolved: {resolved_issues}
        
        Issue Types: {json.dumps(issue_types)}
        Priority Breakdown: {json.dumps(priority_breakdown)}
        
        Provide:
        1. A brief overview (2-3 sentences)
        2. Top 3 areas of concern
        3. Recommended immediate actions
        
        Keep the response concise and actionable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Report generation failed: {str(e)}"
