import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scoring import calculate_task_score

@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=400)

    try:
        body = request.body.decode("utf-8")
        data = json.loads(body)
        tasks = data.get("tasks", [])
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    scored = []
    for task in tasks:
        score = calculate_task_score(task)
        task_with_score = {**task, "score": score}
        scored.append(task_with_score)

    scored_sorted = sorted(scored, key=lambda t: t["score"], reverse=True)
    return JsonResponse({"tasks": scored_sorted})
