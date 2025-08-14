from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def test_postman(request):
    return JsonResponse({"message": "Hello Postman"})


@csrf_exempt
def test_postman_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON invalide"}, status=400)
        
        # On renvoie simplement les données reçues
        return JsonResponse({"received": data})
    else:
        return JsonResponse({"error": "Seule la méthode POST est autorisée"}, status=405)
