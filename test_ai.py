from openrouter_ai import ask_ai

answer = ask_ai(
    "Is my infrastructure healthy?",
    25,
    60,
    10,
    "LOW RISK"
)

print(answer)