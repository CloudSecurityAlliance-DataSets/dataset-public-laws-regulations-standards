[JailbreakBench](./index.html)

  * [Leaderboards](#leaderboard)
  * [Paper](https://arxiv.org/abs/2404.01318)
  * [Contribute](https://github.com/JailbreakBench/jailbreakbench/blob/main/CONTRIBUTING.md)
  * [Library](https://github.com/JailbreakBench/jailbreakbench)
  * [Behaviors](/behaviors)
  * [Jailbreak artifacts](https://github.com/JailbreakBench/artifacts)

![logo](./images/jbb_logo_white.png)

JailbreakBench

Jailbreak attacks cause large language models (LLMs) to generate harmful,
unethical, or otherwise unwanted content. Evaluating these attacks presents a
number of challenges, and the current landscape of benchmarks and evaluation
techniques is fragmented. First, assessing whether LLM responses are indeed
harmful requires open-ended evaluations which are not yet standardized.
Second, existing works compute attacker costs and success rates in
incomparable ways. Third, some works lack reproducibility as they withhold
adversarial prompts or code, and rely on changing proprietary APIs for
evaluation. Consequently, navigating the current literature and tracking
progress can be challenging.  
  
To address this, we introduce JailbreakBench, a centralized benchmark with the
following components:

  1. **Repository of jailbreak artifacts.** An evolving dataset of state-of-the-art adversarial prompts at <https://github.com/JailbreakBench/artifacts>, referred to as jailbreak artifacts, which are explicitly required for submissions to our benchmark to ensure reproducibility.
  2. **Standardized evaluation framework.** Our library at <https://github.com/JailbreakBench/jailbreakbench> that includes a clearly defined threat model, system prompts, chat templates, and scoring functions.
  3. **Leaderboard.** Our leaderboards here (<https://jailbreakbench.github.io/>) that track the performance of attacks and defenses for various LLMs.
  4. **Dataset.** A representative dataset named _JBB-Behaviors_ at <https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors> composed of 100 distinct misuse behaviors (with 55% original examples and the rest sourced from [AdvBench](https://github.com/llm-attacks/llm-attacks/blob/main/data/advbench/harmful_behaviors.csv) and [TDC](https://trojandetection.ai/)/[HarmBench](https://www.harmbench.org/)) divided into ten broad categories corresponding to [OpenAI's usage policies](https://openai.com/policies/usage-policies). Moreover, now it is complemented with 100 benign behaviors that can be used to quickly evaluate overrefusal rates for new models and defenses.

We have carefully considered the potential ethical implications of releasing
this benchmark, and believe that it will be a net positive for the community.
Our jailbreak artifacts can expedite safety training for future models. Over
time, we will expand and adapt the benchmark to reflect technical and
methodological advances in the research community.

_Available Leaderboards_

[Open-Source Models](#div_table_open_source_heading) [Closed-Source
Models](#div_table_closed_source_heading)

Leaderboard: Open-Source Models

Leaderboard: Closed-Source Models

Contribute to JailbreakBench

We welcome contributions in terms of both new attacks and defenses. Please
check
[here](https://github.com/JailbreakBench/jailbreakbench/tree/main#submitting-
a-new-attack-to-the-jailbreakbench-leaderboard) and
[here](https://github.com/JailbreakBench/jailbreakbench/tree/main#submitting-
a-new-defense-to-jailbreakbench) for more details. Feel free to contact us for
any questions or suggestions.

Citation

If you use the JBB-Behaviors dataset, we ask you consider citing the following
works:

  * [AdvBench](https://github.com/llm-attacks/llm-attacks?tab=readme-ov-file#citation)
  * [The Trojan Detection Challenge 2023 Red Teaming Track](https://trojandetection.ai/)/[HarmBench](https://github.com/centerforaisafety/HarmBench#-acknowledgements-and-citation-)
  * [Scalable and Transferable Black-Box Jailbreaks for Language Models via Persona Modulation](https://arxiv.org/abs/2311.03348) by Shah et al.

Moreover, consider citing our whitepaper if you use the datasets, reference
our leaderboard, or if you are using our evaluation library:

    
    
    @inproceedings{chao2024jailbreakbench,
            title={JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models},
            author={Patrick Chao and Edoardo Debenedetti and Alexander Robey and Maksym Andriushchenko and Francesco Croce and Vikash Sehwag and Edgar Dobriban and Nicolas Flammarion and George J. Pappas and Florian Tramèr and Hamed Hassani and Eric Wong},
            booktitle={NeurIPS Datasets and Benchmarks Track},
            year={2024}
    }

* * *

© 2024, JailbreakBench

