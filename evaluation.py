def evaluate():
    test_questions = [
        "What is AI?",
        "Define Machine Learning"
    ]

    expected_answers = [
        "simulation of human intelligence",
        "subset of AI"
    ]

    score = 0

    for q, exp in zip(test_questions, expected_answers):
        # mock response check
        if exp.lower() in q.lower():
            score += 1

    print(f"Accuracy: {score/len(test_questions)*100}%")

if __name__ == "__main__":
    evaluate()
