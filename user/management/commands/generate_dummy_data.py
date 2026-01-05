from django.core.management.base import BaseCommand
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from user.models import CivicIssue


class Command(BaseCommand):
    help = 'Generate dummy civic issues for testing'

    def handle(self, *args, **kwargs):
        # Create test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@citypulse.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()

        areas = [
            'Connaught Place', 'Karol Bagh', 'Lajpat Nagar', 'Saket', 'Dwarka',
            'Rohini', 'Pitampura', 'Janakpuri', 'Rajouri Garden', 'Nehru Place',
            'Vasant Kunj', 'Greater Kailash', 'Cyber City', 'Sohna Road', 'Udyog Vihar',
            'Sector 29 Gurugram', 'Golf Course Road', 'MG Road', 'DLF Phase 3', 'Palam Vihar'
        ]

        issue_types = ['POTHOLE', 'GARBAGE', 'WATER', 'STREETLIGHT', 'ROAD_OBSTRUCTION']
        issue_type_names = {
            'POTHOLE': 'Potholes',
            'GARBAGE': 'Garbage overflow',
            'WATER': 'Water leakage',
            'STREETLIGHT': 'Broken streetlights',
            'ROAD_OBSTRUCTION': 'Road obstruction'
        }

        statuses = ['PENDING', 'IN_PROGRESS', 'RESOLVED', 'REJECTED']
        status_weights = [0.4, 0.3, 0.25, 0.05]

        priorities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        priority_weights = [0.2, 0.4, 0.3, 0.1]

        descriptions = {
            'POTHOLE': ['Large pothole causing traffic issues', 'Deep pothole damaging vehicles'],
            'GARBAGE': ['Overflowing garbage bins', 'Garbage not collected for days'],
            'WATER': ['Water pipe burst', 'Continuous water leakage'],
            'STREETLIGHT': ['Street light not working', 'Broken street light pole'],
            'ROAD_OBSTRUCTION': ['Fallen tree blocking road', 'Construction material blocking traffic']
        }

        self.stdout.write('Clearing existing issues...')
        CivicIssue.objects.all().delete()

        self.stdout.write('Generating 60 dummy issues for Delhi & Gurugram...')
        created_count = 0

        for i in range(60):
            issue_type = random.choice(issue_types)
            area = random.choice(areas)
            
            # Midpoint between Delhi and Gurugram
            base_lat, base_lng = 28.53, 77.11
            lat = round(base_lat + random.uniform(-0.15, 0.15), 6)
            lng = round(base_lng + random.uniform(-0.15, 0.15), 6)
            
            status = random.choices(statuses, weights=status_weights)[0]
            priority = random.choices(priorities, weights=priority_weights)[0]
            description = random.choice(descriptions[issue_type])
            title = f"{issue_type_names[issue_type]} reported in {area}"
            
            days_ago = random.randint(0, 30)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            issue = CivicIssue.objects.create(
                title=title,
                description=description,
                issue_type=issue_type,
                latitude=lat,
                longitude=lng,
                address=f"Main Road, {area}",
                area=area,
                city='New Delhi',
                status=status,
                priority=priority,
                reported_by=user,
                reporter_name=f"{user.first_name} {user.last_name}",
                reporter_phone=f"+91-{random.randint(7000000000, 9999999999)}",
                reporter_email=user.email,
                created_at=created_at,
                ai_classification=issue_type,
                ai_priority=priority,
                ai_analysis=f"AI Analysis: {priority} priority {issue_type_names[issue_type]} issue."
            )
            
            if status == 'RESOLVED':
                issue.resolved_at = created_at + timedelta(days=random.randint(1, days_ago) if days_ago > 0 else 1)
                issue.save()
            
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Created {created_count} dummy issues!'))
        self.stdout.write(f'Total: {CivicIssue.objects.count()}')
