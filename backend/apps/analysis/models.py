from django.db import models

class OSINTReport(models.Model):
    REPORT_TYPES = [
        ('DNS', 'DNS Report'),
        ('WHOIS', 'WHOIS Report'),
        ('NMAP', 'NMAP Scan'),
    ]
    
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    raw_data = models.JSONField()  # Almacena el JSON crudo del reporte
    analysis_result = models.JSONField(null=True, blank=True)  # Respuesta de DeepSeek
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} Report - {self.created_at}"