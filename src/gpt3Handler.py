import openai
import os
# from random import randint

n = 0

class Gpt3Response:

    def __init__(self, useful, questions, useful_reason):
        self.useful = useful
        self.useful_reason = useful_reason
        self.questions = questions

    def __str__(self):
        return "<>".join(self.questions)

    @staticmethod
    def parse_response(resp: str):
        splt = resp.split("Question:")
        splt[0] = splt[0].strip()
        if splt[0].startswith("No"):
            return Gpt3Response(False, [], splt[0])
        else:
            return Gpt3Response(True, splt[1::],splt[0])


def get_raw_gpt3_response(prompt: str, max_tokens = 100):
    global n
    openai.api_key = os.getenv(f"OPEN_AI_API_KEY{n}");
    n += 1
    n %= 5

    return openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt,
          temperature=0.7,
          max_tokens=max_tokens,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

def get_top_response(prompt: str, abstract: str):
    return Gpt3Response.parse_response(get_raw_gpt3_response(build_prompt(prompt, abstract)).get("choices")[0]["text"])

# def build_prompt(prompt: str):
#     return f"""Would it be useful for a student studying Deep Learning to read this paragraph?
# Paragraph:
# Reverse mode AD example, with\n  y\xe2\x80\x84=\xe2\x80\x84f(x\xe2\x82\x81,x\xe2\x82\x82)\xe2\x80\x84=\xe2\x80\x84ln\xe2\x80\x86(x\xe2\x82\x81)\xe2\x80\x85+\xe2\x80\x85x\xe2\x82\x81x\xe2\x82\x82\xe2\x80\x85\xe2\x88\x92\xe2\x80\x85sin\xe2\x80\x86(x\xe2\x82\x82) evaluated at (x\xe2\x82\x81,x\xe2\x82\x82)\xe2\x80\x84=\xe2\x80\x84(2,5).\n  After the forward evaluation of the primals on the left, the adjoint\n  operations on the right are evaluated in reverse\n  (cf.\xc2\xa0Figure\xc2\xa0[FigureBackpropagation]). Note that both\n  $\\frac{{partial y}}{{\partial x_1}}$ and\n  $\\frac{{\\partial y}}{{\\partial x_2}}$ are computed in the same reverse\n  pass, starting from the adjoint\n  $\\bar{{v}}_5 = \\bar{{y}} = \\frac{{\\partial y}}{{\\partial y}} = 1$.
# Useful: No, it provides an example with no explanation.

# Would it be useful for a student studying Deep Learning to read this paragraph?
# Paragraph:
# {prompt}
# Useful:
# """


def rank_prompt(prompt: [(str, Gpt3Response)]):
    return "1." + get_raw_gpt3_response(build_rank_prompt(prompt), 2000).get("choices")[0]["text"]


def build_rank_prompt(respones: [(str, Gpt3Response)]):
    question_str = ""
    counter = 0
    for _,resp in respones:
        for question in resp.questions:
            question_str += f"{counter}. {question.strip()}\n"
            counter += 1
    return f"Ranks these questions based on quality testing a student's overall understanding of deep learning\n{question_str}Rank:\n 1."




def build_prompt(prompt: str, abstract: str):
    return f"""
Would it be useful for a student studying Deep Learning and Machine Learning to read this paragraph? What question would they be able to answer after reading this? What question they have about how this relates to the key claim of the paper?
Abstract:
Derivatives, mostly in the form of gradients and Hessians, are ubiquitous in machine learning. Automatic differentiation (AD), also called algorithmic differentiation or simply "autodiff", is a family of techniques similar to but more general than backpropagation for efficiently and accurately evaluating derivatives of numeric functions expressed as computer programs. AD is a small but established field with applications in areas including computational fluid dynamics, atmospheric sciences, and engineering design optimization. Until very recently, the fields of machine learning and AD have largely been unaware of each other and, in some cases, have independently discovered each other's results. Despite its relevance, general-purpose AD has been missing from the machine learning toolbox, a situation slowly changing with its ongoing adoption under the names "dynamic computational graphs" and "differentiable programming". We survey the intersection of AD and machine learning, cover applications where AD has direct relevance, and address the main implementation techniques. By precisely defining the main differentiation techniques and their interrelationships, we aim to bring clarity to the usage of the terms "autodiff", "automatic differentiation", and "symbolic differentiation" as these are encountered more and more in machine learning settings.
Paragraph:
Reverse mode AD example, with\n  y\xe2\x80\x84=\xe2\x80\x84f(x\xe2\x82\x81,x\xe2\x82\x82)\xe2\x80\x84=\xe2\x80\x84ln\xe2\x80\x86(x\xe2\x82\x81)\xe2\x80\x85+\xe2\x80\x85x\xe2\x82\x81x\xe2\x82\x82\xe2\x80\x85\xe2\x88\x92\xe2\x80\x85sin\xe2\x80\x86(x\xe2\x82\x82) evaluated at (x\xe2\x82\x81,x\xe2\x82\x82)\xe2\x80\x84=\xe2\x80\x84(2,5).\n  After the forward evaluation of the primals on the left, the adjoint\n  operations on the right are evaluated in reverse\n  (cf.\xc2\xa0Figure\xc2\xa0[FigureBackpropagation]). Note that both\n  $\\frac{{partial y}}{{\partial x_1}}$ and\n  $\\frac{{\\partial y}}{{\\partial x_2}}$ are computed in the same reverse\n  pass, starting from the adjoint\n  $\\bar{{v}}_5 = \\bar{{y}} = \\frac{{\\partial y}}{{\\partial y}} = 1$.
Useful: No, it provides an example with no explanation.

Would it be useful for a student studying Deep Learning and Machine Learning to read this paragraph? What question would they be able to answer after reading this? What question they have about how this relates to the key claim of the paper?
Abstract:
Derivatives, mostly in the form of gradients and Hessians, are ubiquitous in machine learning. Automatic differentiation (AD), also called algorithmic differentiation or simply "autodiff", is a family of techniques similar to but more general than backpropagation for efficiently and accurately evaluating derivatives of numeric functions expressed as computer programs. AD is a small but established field with applications in areas including computational fluid dynamics, atmospheric sciences, and engineering design optimization. Until very recently, the fields of machine learning and AD have largely been unaware of each other and, in some cases, have independently discovered each other's results. Despite its relevance, general-purpose AD has been missing from the machine learning toolbox, a situation slowly changing with its ongoing adoption under the names "dynamic computational graphs" and "differentiable programming". We survey the intersection of AD and machine learning, cover applications where AD has direct relevance, and address the main implementation techniques. By precisely defining the main differentiation techniques and their interrelationships, we aim to bring clarity to the usage of the terms "autodiff", "automatic differentiation", and "symbolic differentiation" as these are encountered more and more in machine learning settings.
Paragraph:
The term \xe2\x80\x9cautomatic\xe2\x80\x9d in AD can be a source of confusion, causing machine\nlearning practitioners to put the label \xe2\x80\x9cautomatic differentiation\xe2\x80\x9d, or\njust \xe2\x80\x9cautodiff\xe2\x80\x9d, on any method or tool that does not involve manual\ndifferentiation, without giving due attention to the underlying\nmechanism. We would like to stress that AD as a technical term refers to\na specific family of techniques that compute derivatives through\naccumulation of values during code execution to generate numerical\nderivative evaluations rather than derivative expressions. This allows\naccurate evaluation of derivatives at machine precision with only a\nsmall constant factor of overhead and ideal asymptotic efficiency. In\ncontrast with the effort involved in arranging code as closed-form\nexpressions under the syntactic and semantic constraints of symbolic\ndifferentiation, AD can be applied to regular code with minimal change,\nallowing branching, loops, and recursion. Because of this generality, AD\nhas been applied to computer simulations in industry and academia and\nfound applications in fields including engineering design optimization ,\ncomputational fluid dynamics , physical modeling , optimal control ,\nstructural mechanics , atmospheric sciences , and computational finance\n.
Useful: Yes.
Question: Compare and contrast symbolic, numeric, and automatic differentiation?
Question: Why is automatic differentiation used in deep learning?

Would it be useful for a student studying Deep Learning and Machine Learning to read this paragraph? What question would they be able to answer after reading this? What question would they have about how this relates to the key claim of the paper?
Abstract:
{abstract}
Paragraph:
{prompt}
Useful:
"""


# fake unit tests
if __name__ == "__main__":
    built_prompt = """In order to utilize search techniques, a search space that contains promising candidate activation functions must be designed. An important challenge in designing search spaces is balancing the size and expressivity of the search space. An overly constrained search space will not contain novel activation functions, whereas a search space that is too large will be difficult to effectively search. To balance the two criteria, we design a simple search space inspired by the optimizer search space of Bello et al. (2017) that composes unary and binary functions to construct the activation function. Figure 1: An example activation function structure. The activation function is composed of multiple repetitions of the "core unit", which consists of two inputs, two unary functions, and one binary function. Unary functions take in a single scalar input and return a single scalar output, such u(x) = x^2 or u(x) = o(x). Binary functions take in two scalar inputs and return a single scalar output,such as b(x1, ??2) = x1 ??? ??2 or b(x1, ??2) = exp(- (x1 - ??2)^2)."""
    print(get_top_response(built_prompt))
