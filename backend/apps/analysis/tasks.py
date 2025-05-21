from celery import shared_task
import requests
from django.conf import settings
from jinja2 import Template

@shared_task(bind=True, max_retries=3)
def analyze_with_deepseek(self, report_type, raw_data):
    try:
        with open("prompts/cybersecurity.j2") as f:
            prompt_template = Template(f.read())
        
        prompt = prompt_template.render(
            report_type=report_type,
            data=raw_data
        )
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "prompt": prompt,
                "model": "deepseek-cyber",
                "temperature": 0.3
            },
            headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        self.retry(exc=e)