from django.shortcuts import render
from django.http import HttpResponse
import requests

def index(request):
    weather = []
    error = None
    if request.method == "POST":
        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
            res = requests.get(url)
            data = res.json()
            if "hourly" in data:
                times = data["hourly"]["time"][:3]
                temps = data["hourly"]["temperature_2m"][:3]
                weather = zip(times, temps)
            else:
                error = "Не вдалося отримати погодні дані. Перевірте координати."
        except Exception as e:
            error = f"Помилка під час запиту: {str(e)}"
    return render(request, "index.html", {"weather": weather, "error": error})


def info(request):
    login = request.GET.get("login")
    if login == "vladyslav.kiselar":
        return HttpResponse(f"""
        <html><body>
        <h1>Дані користувача: {login}</h1>
        <p>Прізвище: Кіселар</p>
        <p>Ім'я: Владислав</p>
        <p>Курс: 3</p>
        <p>Група: ІС-32</p>
        </body></html>
        """)
    return HttpResponse("Login не вказано або невірний", status=400)
