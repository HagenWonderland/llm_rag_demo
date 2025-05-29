from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .chroma_rag import rag_retrieve
import openai
import os
import json
openai.api_key = os.getenv("OPENAI_API_KEY")

def index(request):
    return render(request, "chatbot/index.html")

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_question = data.get("question")
        retrieved_docs = rag_retrieve(user_question)
        system_prompt = (
            "你是一位台灣勞動法規專家。根據以下法規內容回答問題，若無法回答可說明僅依照法規內容作答。\n\n"
            + "\n---\n".join(retrieved_docs)
        )
        chat_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        )
        answer = chat_response.choices[0].message.content
        #answer = chat_response["choices"][0]["message"]["content"]
        return JsonResponse({"answer": answer})
    return JsonResponse({"error": "POST only"}, status=400)
