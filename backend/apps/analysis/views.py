import requests
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Función básica de health check
def health_check(request):
    return JsonResponse({
        "status": "OK", 
        "service": "OSINT API",
        "version": "1.0"
    })

class DeepSeekAnalysisView(APIView):
    def post(self, request):
        # Validación básica
        required_fields = ['report_type', 'raw_data']
        if not all(field in request.data for field in required_fields):
            return Response(
                {"error": "Missing required fields: report_type and raw_data"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Construir prompt para DeepSeek según el tipo de reporte
        prompt = self._build_prompt(request.data)
        
        try:
            # Llamada a la API de DeepSeek (ejemplo)
            analysis = self._call_deepseek(prompt)
            
            return Response({
                "status": "success",
                "analysis": analysis,
                "metadata": {
                    "report_type": request.data['report_type'],
                    "domain": request.data['raw_data'].get('domain')
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _build_prompt(self, data):
        """Construye un prompt especializado según el tipo de reporte"""
        report_type = data['report_type']
        raw_data = data['raw_data']
        
        prompts = {
            'WHOIS': f"""
            Analiza este reporte WHOIS y genera recomendaciones de seguridad:
            Dominio: {raw_data.get('domain')}
            Registrar: {raw_data.get('registrar')}
            Fecha creación: {raw_data.get('creation_date')}
            
            Busca:
            1. Posibles intentos de typosquatting
            2. Antigüedad sospechosa del dominio
            3. Recomendaciones OWASP
            """,
            
            'NMAP': f"""
            Analiza este escaneo NMAP:
            IP: {raw_data.get('ip')}
            Puertos abiertos: {raw_data.get('ports')}
            
            Identifica:
            1. Servicios vulnerables
            2. CVEs relevantes
            3. Recomendaciones de hardening
            """
        }
        
        return prompts.get(report_type, "Analiza este reporte OSINT")

    def _call_deepseek(self, prompt):
        """Simulación de llamada a la API de DeepSeek"""
        # EN PRODUCCIÓN USARÍAS:
        # headers = {"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"}
        # response = requests.post("https://api.deepseek.com/v1/chat", json={"prompt": prompt}, headers=headers)
        
        # Respuesta simulada para pruebas
        return {
            "risk_score": 8.2,
            "recommendations": [
                "El dominio tiene más de 10 años, verificar historial de uso",
                "Registrador conocido pero monitorear cambios recientes",
                "Implementar DMARC/DKIM para protección contra phishing"
            ],
            "full_analysis": prompt  # En producción sería el análisis real
        }