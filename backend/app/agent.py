import os
import google.generativeai as genai
from vectorstore import embed_text, search_similar, upsert
from searcher import web_search
from guardrails import looks_like_math, validate_output_answer

# Configure Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def call_gemini(prompt: str, max_tokens=800) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

async def answer_question(question: str, retrieve_k=3, allow_web=True):
    if not looks_like_math(question):
        return {"ok": False, "error": "Not a math question."}
    
    qvec = await embed_text(question)
    retrieved = search_similar(qvec, top_k=retrieve_k)

    if retrieved:
        gen = await call_gemini(f"KB context + {question}")
    else:
        if allow_web:
            snippets = await web_search(question)
            context = " ".join([s.get("snippet","") for s in snippets])
            gen = await call_gemini(f"Use context: {context}\n\nQuestion: {question}")
        else:
            gen = await call_gemini(question)

    ok, reason = validate_output_answer(gen)
    print(reason)
    return {
        "ok": ok,
        # "validation_reason": reason,
        "answer": gen,
        "used_kb": bool(retrieved),
        "retrieved": retrieved,
    }
