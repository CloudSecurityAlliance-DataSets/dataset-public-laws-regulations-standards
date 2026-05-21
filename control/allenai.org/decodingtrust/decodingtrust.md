  * [Home](/)
  * [GitHub](https://github.com/AI-secure/DecodingTrust)
  * [Paper](https://arxiv.org/abs//2306.11698)
  * [Explore](/explore)
  * [Demo](/demo)
  * [Leaderboard](/leaderboard)
  * [Appendix](appendix/DT_appendix_2024.pdf)

[DecodingTrust](/)

# **DecodingTrust**

###  Comprehensive Assessment of Trustworthiness in GPT Models

# What is DecodingTrust?

DecodingTrust aims at providing a thorough assessment of trustworthiness in
GPT models.

This research endeavor is designed to help researchers and practitioners
better understand the capabilities, limitations, and potential risks involved
in deploying these state-of-the-art Large Language Models (LLMs).

This project is organized around the following eight primary perspectives of
trustworthiness, including:

  * Toxicity
  * Stereotype and bias
  * Adversarial robustness
  * Out-of-Distribution Robustness
  * Privacy
  * Robustness to Adversarial Demonstrations
  * Machine Ethics
  * Fairness

  
![Our paper received the Outstanding Paper Award at
NeurIPS'23.](crown.png)**_Our paper received the Outstanding Paper Award at
NeurIPS'23._**  
![Our paper received the Outstanding Paper Award at
NeurIPS'23.](crown.png)**_Our paper received the Best Scientific Cybersecurity
Paper Award by National Security Agency'24._**

## Trustworthiness Perspectives

⚠️ WARNING: our data contains model outputs that may be considered offensive.

  

DecodingTrust aims to provide a comprehensive trustworthiness evaluation on
the recent large language model GPT-4, in comparison to GPT-3.5, from
different perspectives, including toxicity, stereotype bias, adversarial
robustness, out-of-distribution robustness, robustness on adversarial
demonstrations, privacy, machine ethics, and fairness under different
settings.

  
![Examples of unreliable responses of GPT-4 from different trustworthiness
perspectives. GPT-4 can generate undesirable or unreliable content given
benign system prompts.](overview.png)

## Getting Started

We have built a few resources to help you get started with the dataset.

Explore our dataset (distributed under the [CC BY-SA
4.0](http://creativecommons.org/licenses/by-sa/4.0/legalcode) license):  

  * [dataset](https://github.com/AI-secure/DecodingTrust)

To evaluate your models, we have also made available the evaluation script for
different facets of trustworthiness. To replicate our evaluation, go the
corresponding subdirectories for detailed evaluation scripts.

  * [Toxicity ](https://github.com/AI-secure/DecodingTrust/tree/main/src/dt/perspectives/toxicity)
  * [Stereotype ](https://github.com/AI-secure/DecodingTrust/tree/main/src/dt/perspectives/stereotype)
  * [Adversarial Robustness ](https://github.com/AI-secure/DecodingTrust/tree/main/src/dt/perspectives/advglue)
  * [Out-of-distribution Robustness ](https://github.com/AI-secure/DecodingTrust/tree/main/src/dt/perspectives/ood)
  * [Robustness against Adversarial Demonstrations ](https://github.com/AI-secure/DecodingTrust/tree/main/src/dt/perspectives/adv_demonstration)
  * [Privacy ](https://github.com/AI-secure/DecodingTrust/tree/main/src/dt/perspectives/privacy)
  * [Machine Ethics ](https://github.com/AI-secure/DecodingTrust/tree/main/src/dt/perspectives/machine_ethics)
  * [Fairness ](https://github.com/AI-secure/DecodingTrust/tree/main/src/dt/perspectives/fairness)

While our evaluation mainly focuses on GPT-3.5 and GPT-4, once you have a
built a model that works to your expectations, you can also submit the mode
generations and their corresponding scores via submitting pull requests in
GitHub. Because DecodingTrust is an ongoing effort, we expect the dataset to
evolve.

## Have Questions?

Ask us questions at [boxinw2@illinois.edu](mailto:boxinw2@illinois.edu).

## Acknowledgements

We thank the [SQuAD team](https://rajpurkar.github.io/SQuAD-explorer/) for
allowing us to use their website template and submission tutorials.

  * [DecodingTrust](/)
  * [UIUC Secure Learning Lab](https://aisecure.github.io/)
  * [Microsoft Research](https://www.microsoft.com/en-us/research/)

