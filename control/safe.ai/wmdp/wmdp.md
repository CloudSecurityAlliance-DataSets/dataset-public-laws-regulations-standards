You need to enable JavaScript to run this app.

# The WMDP Benchmark: Measuring and Reducing  
Malicious Use With Unlearning

The WMDP Team

[ Paper](https://arxiv.org/abs/2403.03218)

[ GitHub](https://github.com/centerforaisafety/wmdp)

[![](images/hf-
logo.png)Collection](https://huggingface.co/collections/cais/wmdp-
benchmark-661ed0abb589122164900e0e)

[![](https://assets-global.website-
files.com/63fe96aeda6bea77ac7d3000/63fe9a72750bc67b129df210_CAIS%20Logo.svg)Blog](https://www.safe.ai/blog/wmdp-
benchmark)

## Introduction

The **W** eapons of **M** ass **D** estruction **P** roxy (WMDP) benchmark is
a dataset of 3,668 multiple-choice questions surrounding hazardous knowledge
in![Biosecurity Icon](images/bio_icon.svg)biosecurity,![Cybersecurity
Icon](images/cyber_icon.svg)cybersecurity, and![Chemical Security
Icon](images/chem_icon.svg)chemical security. WMDP serves as both a proxy
evaluation for hazardous knowledge in large language models (LLMs) and a
benchmark for unlearning methods to remove such knowledge.  
  
To guide progress on mitigating risk from LLMs, we develop RMU, a state-of-
the-art unlearning method which reduces model performance on WMDP while
maintaining general language model capabilities.

![outline](images/dataset.svg)

## Evaluating Risk From LLMs

![outline](images/three_panel.svg)

To measure risks of malicious use, government institutions and major AI labs
are developing evaluations for hazardous capabilities in LLMs. However,
current evaluations are private and are limited to a narrow range of misuse
scenarios. To fill these gaps, we publicly release WMDP, an expert-written
dataset which measures how LLMs could aid malicious actors in developing
biological, cyber, and chemical attack capabilities. To avoid releasing
sensitive and export-controlled information, we collect questions that are
precursors, neighbors, and components of the hazardous knowledge we wish to
remove.

## Mitigating Risk from LLMs

![outline](images/pipeline.svg)

On closed source API-access models, such as GPT-4 and Gemini, adversaries can
deploy adversarial attacks or harmful API-finetuning to bypass models’ refusal
training and unlock their knowledge. Fortunately, model providers have
leverage, as they may apply safety interventions before serving the model. In
particular, providers may perform machine unlearning to directly remove
hazardous knowledge from models. Unlearned models have higher inherent safety:
even if they are jailbroken, unlearned models lack the knowledge to be
repurposed for malicious use.

To guide progress on unlearning, we develop RMU, a state-of-the-art method
inspired by [representation engineering](https://www.ai-transparency.org/),
which improves unlearning precision: removing dangerous knowledge while
preserving general model capabilities. RMU significantly reduces model
performance on WMDP, while mostly retaining general capabilities on MMLU and
MT-Bench, suggesting that concrete progress in unlearning is feasible.

![outline](images/main_results.png)

#### Citation:

@misc{li2024wmdp,  

title={The WMDP Benchmark: Measuring and Reducing Malicious Use With
Unlearning},

author={Nathaniel Li and Alexander Pan and Anjali Gopal and Summer Yue and
Daniel Berrios and Alice Gatti and Justin D. Li and Ann-Kathrin Dombrowski and
Shashwat Goel and Long Phan and Gabriel Mukobi and Nathan Helm-Burger and
Rassin Lababidi and Lennart Justen and Andrew B. Liu and Michael Chen and
Isabelle Barrass and Oliver Zhang and Xiaoyuan Zhu and Rishub Tamirisa and
Bhrugu Bharathi and Adam Khoja and Zhenqi Zhao and Ariel Herbert-Voss and Cort
B. Breuer and Samuel Marks and Oam Patel and Andy Zou and Mantas Mazeika and
Zifan Wang and Palash Oswal and Weiran Liu and Adam A. Hunt and Justin
Tienken-Harder and Kevin Y. Shih and Kemper Talley and John Guan and Russell
Kaplan and Ian Steneker and David Campbell and Brad Jokubaitis and Alex
Levinson and Jean Wang and William Qian and Kallol Krishna Karmakar and Steven
Basart and Stephen Fitz and Mindy Levine and Ponnurangam Kumaraguru and Uday
Tupakula and Vijay Varadharajan and Yan Shoshitaishvili and Jimmy Ba and Kevin
M. Esvelt and Alexandr Wang and Dan Hendrycks},

year={2024},

eprint={2403.03218},

archivePrefix={arXiv},

primaryClass={cs.LG}

}

