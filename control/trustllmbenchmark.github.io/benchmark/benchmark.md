![](https://raw.githubusercontent.com/TrustLLMBenchmark/TrustLLM-
Website/main/img/logo.png)

[ ![](img/menu.png) ](javascript:void\(0\))

[Overview](index.html) [Leaderboard](leaderboard.html) [Submit](submit.html)
[Paper](https://arxiv.org/abs/2401.05561)
[GitHub](https://github.com/HowieHwong/TrustLLM)

![](img/website-background_00.png)

A Comprehensive Study of Trustworthiness in Large Language Models.

# Introduction

  

* * *

![Rank Card](img/benchmark_arch_00.png)

In this work, we introduce TrustLLM which thoroughly explores the
trustworthiness of LLMs. Specifically, there are three-fold major
contributions of TrustLLM: (1) Firstly, we have proposed a set of guidelines
based on a wide range of literature reviews for evaluating the trustworthiness
of LLMs, which is a taxonomy encompassing eight aspects, including
truthfulness, safety, fairness, robustness, privacy, machine ethics,
transparency, and accountability. (2) Secondly, we have established a
benchmark for six of these aspects due to the difficulty of benchmarking
transparency and accountability. This is the first comprehensive and
integrated benchmark comprising over 18 subcategories, covering more than 30
datasets and 16 mainstream LLMs, including both proprietary and open-weight
LLMs. (3) Last but not least, drawing from extensive experimental results , we
have derived insightful findings. Our evaluation of trustworthiness in LLMs
takes into account both the overall observation and individual findings based
on each dimension, emphasizing the relationship between effectiveness and
trustworthiness, the prevalent lack of real alignment in most LLMs, the
disparity between proprietary and open-weight LLMs, and the opacity of current
trustworthiness-related technologies. We aim to provide valuable insights for
future research in this field, contributing to a more nuanced understanding of
the trustworthiness landscape in large language models.

# Empirical Findings

  

## Overall Perspective

## Trustworthiness Linked with Utility

_Trustworthiness is closely related to utility._ We have observed a close
relationship between trustworthiness and utility, and they often have a
positive relation in specific tasks. For example, in tasks like moral behavior
classification and stereotype recognition, LLMs generally need to possess
strong utility to understand the task's meaning and make correct choices.
Additionally, the trustworthiness ranking of LLMs is often closely related to
their ranking on utility-focused leaderboards.

## LLMs' Alignment Shortfall

_We have found that many LLMs exhibit a certain degree of over-alignment
(i.e., exaggerated safety), which can compromise the trustworthiness of LLMs._
LLMs may identify many innocuous prompt contents as harmful, impacting their
utility. For instance, Llama2-7b obtained a 57% of refusing to answer when the
prompt is not harmful. Therefore, it is crucial to make LLMs aware of the real
intent of the prompt itself in the alignment process instead of simply
memorizing examples. This contributes to reducing the false positive rate when
recognizing harmful content.

## Trust Disparity: Closed vs. Open LLMs

_Generally, proprietary LLMs outperform most open-weight LLMs in
trustworthiness. However, a few open-source LLMs can compete with proprietary
ones._ We found a gap in the performance of open-weight and proprietary LLMs
regarding trustworthiness. Generally, proprietary LLMs (e.g., ChatGPT, GPT-4)
tend to perform much better than the majority of open-weight LLMs. This is a
serious concern because open-weight models can be widely downloaded. Once
integrated into application scenarios, they may pose severe risks. However, we
were surprised to discover that Llama2, a series of open-weight LLMs,
surpasses proprietary LLMs in trustworthiness in many tasks. This indicates
that open-weight models can demonstrate excellent trustworthiness even without
adding external auxiliary modules (such as a moderator). This finding provides
a significant reference value for relevant open-weight developers.

## Imperative for Transparency in Trustworthy AI Technology

_Both the model itself and trustworthiness-related technology should be
transparent (e.g., open-source)._ The performance gap among different LLMs
highlights the need for transparency in both the models and trustworthy
technologies. Understanding the training mechanisms is fundamental in
researching LLMs. While some proprietary LLMs show high trustworthiness, the
lack of transparency in their technologies is a concern. Open sourcing
trustworthy technologies can enhance LLM reliability and foster AI's benign
development.

## Section Perspective

  

## Truthfulness

Truthfulness means the accurate representation of information, facts, and
results by an AI system. We have found that:

  1. Proprietary LLMs like GPT-4 and open-source LLMs like LLama2 struggle to provide truthful responses when relying solely on their internal knowledge. This challenge can primarily be attributed to noise in their training data, including misinformation or outdated information, and the lack of knowledge generalization capability in the underlying Transformer architecture.
  2. Moreover, all LLMs encounter challenges in zero-shot commonsense reasoning tasks. This highlights that LLMs may struggle with relatively straightforward tasks for humans to perform.
  3. Conversely, when assessing the performance of LLMs with augmented external knowledge, they exhibit significantly improved results, surpassing the state-of-the-art performance reported in the original datasets.
  4. We note a significant discrepancy among different hallucination tasks. Most LLMs exhibit fewer hallucinations in multiple-choice question-answering tasks than in more open-ended tasks like knowledge-grounded dialogue, likely attributed to prompt sensitivity.
  5. We also identify a positive correlation between sycophancy and adversarial actuality. Models exhibiting lower levels of sycophancy demonstrate an ability to identify factual errors in user input and highlight them effectively.

## Safety

Safety ensures the outputs from LLMs should only engage users in a safe and
healthy conversation. In our experiments, we have found that:

  1. The safety of most open-source LLMs still raises concerns and lags significantly behind proprietary LLMs. For the most part, the safety of open-source LLMs is lower than that of proprietary LLMs in terms of jailbreak, toxicity, and misuse.
  2. Importantly, LLMs cannot effectively resist various jailbreak attacks equally. We observed that different jailbreak attacks have varying success rates against LLMs, with leetspeak attacks having the highest success rate. Therefore, LLM developers should consider a comprehensive approach to defend against different types of attacks.
  3. Most LLMs struggle to balance regular and excessive safety. LLMs with strong safety often exhibit severely exaggerated safety, as seen in the Llama2 series and ERNIE, which suggests that most LLMs are not really aligned and they may only memorize shallow alignment knowledge.

## Fairness

Fairness is the quality or state of being fair, especially fair or impartial
treatment. In our experiments, we have found that:

  1. The performance of most LLMs in identifying stereotypes is not satisfactory, with even the best-performing GPT-4 having an overall accuracy of only 65%. When presented with sentences containing stereotypes, the percentage of agreement of different LLMs varies widely, with the best performance at only 0.5% agreement rate and the worst-performing one approaching an agreement rate of nearly 60%. 
  2. Only a few LLMs, such as Oasst-12b and Vicuna-7b, exhibit fairness in handling disparagement; most LLMs still display biases towards specific attributes when dealing with questions containing disparaging tendencies.
  3. Regarding preferences, most LLMs perform very well on the plain baseline, maintaining objectivity and neutrality or refusing to answer directly. However, when forced to choose an option, the performance of LLMs significantly decreases.

## Robustness

Robustness is the ability of a system to maintain its level of performance
under a variety of circumstances. In our experiments, we have found that:

  1. The Llama2 series and most proprietary LLMs outperform other open-source models in traditional downstream tasks.
  2. There is a significant variation in LLMs' performance in open-ended tasks. The worst-performing model has an average semantic similarity of only 88% before and after perturbation, which is far below the top performer at 97.64%.
  3. Regarding OOD robustness, LLMs also exhibit considerable variability in performance. The leading model, GPT-4, shows a RtA (Refuse to Answer) rate of over 80% in OOD detection and an F1 score averaging over 92% in OOD generalization. In contrast, the least effective models register a mere 0.4% in RtA and F1 score of around 30%.

## Privacy

Privacy is the norms and practices that help to safeguard human autonomy,
identity, and dignity. In our experiments, we have found that:

  1. Most LLMs possess a certain level of privacy awareness, as the probability of LLMs refusing to answer inquiries about private information dramatically increases when they are informed that they must adhere to privacy policies.
  2. Pearson's correlation between humans and LLMs of agreement on privacy information usage varies a lot. The best-performed ChatGPT archives a 0.665 correlation, however, the correlation of Oass-12b is surprisingly less than zero, indicating a negative correlation with humans.
  3. We have observed that nearly all LLMs exhibit some information leakage on Enron Email Dataset.

## Machine Ethics

Machine ethics ensure the moral behaviors of man-made machines that use
artificial intelligence, otherwise known as artificial intelligent agents. In
our experiments, we have found that:

  1. LLMs have already formed a particular set of moral values, but there is still a significant gap in aligning completely with human ethics. The accuracy of most LLMs on implicit tasks with low-ambiguity scenarios is below 70%, regardless of the dataset. When given a high-ambiguity scenario, the performance varies a lot between different LLMs as the Llama2 series reaches an RtA of 99.9%, and some are less than 70%.
  2. Regarding emotional awareness, LLMs demonstrate higher accuracy, with the best-performing LLMs being GPT-4, which exceeds an accuracy rate of 94%.

  

# Models

  

Model | Model Size | Open-Weight | Version | Creator | Source | Link  
---|---|---|---|---|---|---  
GPT-3.5-turbo (ChatGPT) | unknown |  No  | - | OpenAI | OpenAI API |  [ ![](img/openai.png) ](https://openai.com/blog/chatgpt)  
GPT-4 | unknown |  No  | - | OpenAI | OpenAI API |  [ ![](img/openai.png) ](https://openai.com/research/gpt-4)  
ERNIE-3.5-turbo | unknown |  No  | - | Baidu Inc. | ERNIE API |  [ ![](img/ernie.png) ](https://yiyan.baidu.com/)  
text-bison-001 (PaLM 2) | unknown |  No  | - | Google | Google API |  [ ![](img/palm2.png) ](https://ai.google/discover/palm2/)  
Llama2-7b | 7b |  Yes  | - | Meta | HuggingFace |  [ ![](img/meta.png) ](https://ai.meta.com/llama/)  
Llama2-13b | 13b |  Yes  | - | Meta | HuggingFace |  [ ![](img/meta.png) ](https://ai.meta.com/llama/)  
Llama2-70b | 70b |  Yes  | - | Meta | HuggingFace |  [ ![](img/meta.png) ](https://ai.meta.com/llama/)  
Mistral-7b | 7b |  Yes  | v0.1 | Mistral AI | HuggingFace |  [ ![](img/mistral.jpeg) ](https://mistral.ai/)  
Vicuna-33b | 33b |  Yes  | v1.3 | LMSYS | HuggingFace |  [ ![](img/vicuna.jpeg) ](https://lmsys.org/blog/2023-03-30-vicuna/)  
Vicuna-13b | 13b |  Yes  | v1.3 | LMSYS | HuggingFace |  [ ![](img/vicuna.jpeg) ](https://lmsys.org/blog/2023-03-30-vicuna/)  
Vicuna-7b | 7b |  Yes  | v1.3 | LMSYS | HuggingFace |  [ ![](img/vicuna.jpeg) ](https://lmsys.org/blog/2023-03-30-vicuna/)  
Koala-13b | 13b |  Yes  | - | UCB | HuggingFace |  [ ![](img/huggingface.png) ](https://huggingface.co/TheBloke/koala-13B-HF)  
ChatGLM2 | 6b |  Yes  | v1.0 | Tsinghua & Zhipu | HuggingFace |  [ ![](img/chatglm.png) ](https://chatglm.cn/)  
Baichuan-13b | 13b |  Yes  | - | Baichuan Inc. | HuggingFace |  [ ![](img/baichuan.png) ](https://www.baichuan-ai.com/home)  
Wizardlm-13b | 13b |  Yes  | v1.2 | Microsoft | HuggingFace |  [ ![](img/huggingface.png) ](https://huggingface.co/WizardLM/WizardLM-13B-V1.2)  
Oasst-12b | 12b |  Yes  | - | LAION | HuggingFace |  [ ![](img/huggingface.png) ](https://huggingface.co/OpenAssistant/oasst-sft-1-pythia-12b)  
  
# Task & Dataset

##  Datasets and metrics

  

Datasets and metrics in TrustLLM. ✓ means the dataset exists and ✗ means the dataset is first proposed in the TrustLLM benchmark. Dataset | Description | Num. | Exist? | Section  
---|---|---|---|---  
SQuAD2.0 | It combines questions in SQuAD1.1 with over 50,000 unanswerable questions.  | 100 | ✓ | Misinformation  
CODAH | It contains 28,000 commonsense questions. | 100 | ✓ | Misinformation  
HotpotQA | It contains 113k Wikipedia-based question-answer pairs for complex multi-hop reasoning. | 100 | ✓ | Misinformation  
AdversarialQA | It contains 30,000 adversarial reading comprehension question-answer pairs.  | 100 | ✓ | Misinformation  
Climate-FEVER | It contains 7,675 climate change-related claims manually curated by human fact-checkers. | 100 | ✓ | Misinformation  
SciFact | It contains 1,400 expert-written scientific claims pairs with evidence abstracts. | 100 | ✓ | Misinformation  
COVID-Fact | It contains 4,086 real-world COVID claims. | 100 | ✓ | Misinformation  
HealthVer | It contains 14,330 health-related claims against scientific articles. | 100 | ✓ | Misinformation  
TruthfulQA | The multiple-choice questions to evaluate whether a language model is truthful in generating answers to questions. | 352 | ✓ | Hallucination  
HaluEval | It contains 35,000 generated and human-annotated hallucinated samples. | 300 | ✓ | Hallucination  
LM-exp-sycophancy | A dataset consists of human questions with one sycophancy response example and one non-sycophancy response example. | 179 | ✓ | Sycophancy  
Opinion pairs | It contains 120 pairs of opposite opinions. | 240 | ✗ | Sycophancy  
WinoBias | It contains 3,160 sentences, split for development and testing, created by researchers familiar with the project. | 734 | ✓ | Stereotype  
StereoSet | It contains the sentences that measure model preferences across gender, race, religion, and profession. | 734 | ✓ | Stereotype  
Adult | The dataset, containing attributes like sex, race, age, education, work hours, and work type, is utilized to predict salary levels for individuals. | 810 | ✓ | Disparagement  
Jailbraek Trigger | The dataset contains the prompts based on 13 jailbreak attacks. | 1300 | ✗ | Jailbreak, Toxicity  
Misuse (additional) | This dataset contains prompts crafted to assess how LLMs react when confronted by attackers or malicious users seeking to exploit the model for harmful purposes. | 261 | ✗ | Misuse  
Do-Not-Answer | It is curated and filtered to consist only of prompts to which responsible LLMs do not answer. | 344 + 95 | ✓ | Misuse, Stereotype  
AdvGLUE | A multi-task dataset with different adversarial attacks. | 912 | ✓ | Natural Noise  
AdvInstruction | 600 instructions generated by 11 perturbation methods. | 1200 | ✗ | Natural Noise  
ToolE | A dataset with the users' queries which may trigger LLMs to use external tools. | 241 | ✓ | Out of Domain (OOD)  
Flipkart | A product review dataset, collected starting from December 2022. | 400 | ✓ | Out of Domain (OOD)  
DDXPlus | A 2022 medical diagnosis dataset comprising synthetic data representing about 1.3 million patient cases. | 100 | ✓ | Out of Domain (OOD)  
ETHICS | It contains numerous morally relevant scenarios descriptions and their moral correctness. | 500 | ✓ | Implicit Ethics  
Social Chemistry 101 | It contains various social norms, each consisting of an action and its label.  | 500 | ✓ | Implicit Ethics  
MoralChoice | It consists of different contexts with morally correct and wrong actions. | 668 | ✓ | Explicit Ethics  
ConfAIde | It contains the description of how information is used. | 196 | ✓ | Privacy Awareness  
Privacy Awareness | It includes different privacy information queries about various scenarios.  | 280 | ✗ | Privacy Awareness  
Enron Email | It contains approximately 500,000 emails generated by employees of the Enron Corporation. | 400 | ✓ | Privacy Leakage  
Xstest | It's a test suite for identifying exaggerated safety behaviors in LLMs. | 200 | ✓ | Exaggerated Safety  
  
  
  

##  Task Overview

  

Task Overview. ○ means automatic evaluation, ● means manual evaluation, and ◐ means semi-automatic evaluation. More trustworthy LLMs are expected to have a higher value of the metrics with ↑ and a lower value of the metrics with ↓.  Task Name | Metrics | Type | Eval | Section  
---|---|---|---|---  
Closed-book QA | Accuracy (↑) | Generation | ○ | Misinformation(Internal)  
Fact-Checking | Macro F-1 (↑) | Classification | ● | Misinformation(External)  
Multiple Choice QA | Accuracy (↑) | Classification | ● | Hallucination  
Hallucination Classification | Accuracy (↑) | Classification | ● | Hallucination  
Persona Sycophancy | Embedding similarity (↑) | Generation | ◐ | Sycophancy  
Opinion Sycophancy | Percentage change (↓) | Generation | ○ | Sycophancy  
Factuality Correction | Percentage change (↑) | Generation | ○ | Adversarial Factuality  
Jailbreak Attack Evaluation | RtA (↑) | Generation | ○ | Jailbreak  
Toxicity Measurement | Toxicity Value (↓) | Generation | ● | Toxicity  
Misuse Evaluation | RtA (↑) | Generation | ○ | Misuse  
Exaggerated Safety Evaluation | RtA (↓) | Generation | ○ | Exaggerated Safety  
Agreement on Stereotypes | Accuracy (↑) | Generation | ◐ | Stereotype  
Recognition of Stereotypes | Agreement Percentage (↓) | Classification | ◐ | Stereotype  
Stereotype Query Test | RtA (↑) | Generation | ○ | Stereotype  
Preference Selection | RtA (↑) | Generation | ○ | Preference  
Salary Prediction | p-value (↑) | Generation | ● | Disparagement  
Adversarial Perturbation in Downstream Tasks | ASR (↓), RS (↑) | Generation | ◐ | Natural Noise  
Adversarial Perturbation in Open-Ended Tasks | Embedding similarity (↑) | Generation | ◐ | Natural Noise  
OOD Detection | RtA (↑) | Generation | ○ | Out of Domain (OOD)  
OOD Generalization | Micro F1 (↑) | Classification | ○ | Out of Domain (OOD)  
Agreement on Privacy Information | Pearson’s correlation (↑) | Classification | ● | Privacy Awareness  
Privacy Scenario Test | RtA (↑) | Generation | ○ | Privacy Awareness  
Probing Privacy Information Usage | RtA (↑), Accuracy (↓) | Generation | ◐ | Privacy Leakage  
Moral Action Judgement | Accuracy (↑) | Classification | ◐ | Implicit Ethics  
Moral Reaction Selection (Low-Ambiguity) | Accuracy (↑) | Classification | ◐ | Explicit Ethics  
Moral Reaction Selection (High-Ambiguity) | RtA (↑) | Generation | ○ | Explicit Ethics  
Emotion Classification | Accuracy (↑) | Classification | ● | Emotional Awareness  
  
# Ranking Card

  

![Rank Card](img/rank_card_00.png)

# Citation

  

    
    
        @inproceedings{huang2024position,
      title={Position: TrustLLM: Trustworthiness in large language models},
      author={Huang, Yue and Sun, Lichao and Wang, Haoran and Wu, Siyuan and Zhang, Qihui and Li, Yuan and Gao, Chujie and Huang, Yixin and Lyu, Wenhan and Zhang, Yixuan and others},
      booktitle={International Conference on Machine Learning},
      pages={20166--20270},
      year={2024},
      organization={PMLR}
    }
        

  

# TrustLLM Team

  

![School 1](img/logos/Lehigh-University-logo.png) ![School
3](img/logos/W&M.png) ![School 3](img/logos/stanford.png) ![School
3](img/logos/UCLA.jpeg) ![School 3](img/logos/CMU.png) ![School
3](img/logos/UIUC.png) ![School 2](img/logos/MIT.png) ![School
2](img/logos/ND.png) ![School 2](img/logos/duke.png) ![School
3](img/logos/harvard.png) ![School 2](img/logos/UMD.png) ![School
2](img/logos/JHU.jpeg) ![School 2](img/logos/UIC.png) ![School
2](img/logos/UGA.png) ![School 3](img/logos/TAMU.png) ![School
3](img/logos/UNC.png) ![School 2](img/logos/MBZUAI.jpeg) ![School
2](img/logos/yale.png) ![School 2](img/logos/Columbia.png) ![School
2](img/logos/UCB.png) ![School 3](img/logos/UPenn.png) ![School
2](img/logos/UWM.png) ![School 2](img/logos/UCSB.png) ![School
2](img/logos/vt.png) ![School 2](img/logos/IIT.gif) ![School
2](img/logos/USC.png) ![School 2](img/logos/CISPA.png) ![School
2](img/logos/MGH.png) ![School 2](img/logos/MSU.png) ![School
2](img/logos/FIU.png) ![School 2](img/logos/drexel.png) ![School
3](img/logos/tenne.png) ![School
2](img/logos/Lawrence_Livermore_National_Lab.png) ![School
2](img/logos/samsung.webp) ![School 3](img/logos/Microsoft.png) ![School
2](img/logos/IBM.png) ![School 2](img/logos/Salesforce.png)

© 2024 TrustLLM  
Contact Us:
[trustllm.benchmark@gmail.com](mailto:trustllm.benchmark@gmail.com), [
lis221@lehigh.edu](mailto:lis221@lehigh.edu),
[howiehwong@gmail.com](mailto:howiehwong@gmail.com)  
Website developed based on the [yenchiah project-website-
template](https://github.com/yenchiah/project-website-template?tab=readme-ov-
file).

