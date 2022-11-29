import openai
import os
openai.api_key = os.getenv("OPEN_AI_API_KEY")

def get_raw_gpt3_response(prompt):
    return openai.Completion.create(
          model="text-davinci-002",
          prompt=prompt,
          temperature=0.7,
          max_tokens=100,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

def get_top_response(prompt):
    return get_raw_gpt3_response(prompt).get("choices")[0]["text"]


def build_prompt(prompt):
    return f"""Given the Context what is a good question?
Context:
{prompt}

Question:"""


# fake unit tests
if __name__ == "__main__":
    built_prompt = build_prompt("""In order to utilize search techniques, a search space that contains promising candidate activation functions must be designed. An important challenge in designing search spaces is balancing the size and expressivity of the search space. An overly constrained search space will not contain novel activation functions, whereas a search space that is too large will be difficult to effectively search. To balance the two criteria, we design a simple search space inspired by the optimizer search space of Bello et al. (2017) that composes unary and binary functions to construct the activation function. Figure 1: An example activation function structure. The activation function is composed of multiple repetitions of the "core unit", which consists of two inputs, two unary functions, and one binary function. Unary functions take in a single scalar input and return a single scalar output, such u(x) = x^2 or u(x) = o(x). Binary functions take in two scalar inputs and return a single scalar output,such as b(x1, ×2) = x1 • ×2 or b(x1, ×2) = exp(- (x1 - ×2)^2).""")
    print(f"built prompt: {built_prompt}")
    print(get_top_response(built_prompt))
