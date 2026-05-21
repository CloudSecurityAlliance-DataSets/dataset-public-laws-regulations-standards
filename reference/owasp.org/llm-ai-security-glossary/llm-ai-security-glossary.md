# OWASP LLM & Generative AI Security Glossary

Source: https://genai.owasp.org/glossary/

Total terms: 35

## Adversarial Attacks

Deliberate attempt to manipulate or compromise the functionality of AI systems, particularly machine learning models. These attacks exploit vulnerabilities in AI systems to cause malfunctions, incorrect outputs, or unintended behaviors. Source NIST

*status: standard*

## Artificial Intelligence, AI

According to 15 U.S. Code § 9401 , artificial intelligence is defined as “a machine-based system that can, for a given set of human-defined objectives, make predictions, recommendations or decisions influencing real or virtual environments.” Source Cornell

*status: approved*

## AI Cybersecurity Incident

An occurrence that actually or imminently jeopardizes, without lawful authority, the confidentiality, integrity, or availability of the AI system, any other system enabled and/or created by the AI system, or information stored on any of these systems. Source CISA

*status: approved*

## AI system

Machine-based system that, for a given set of human-defined objectives, makes predictions, recommendations, or decisions that influence real or virtual environments. These AI systems use both machine- and human-based inputs to perceive environments, abstract those perceptions into models through automated analysis, and use model inference to provide options for information or action. Source 15 U.S.C. 9401(3).

*status: approved*

## Chain of Thought (COT)

Method for unlocking reasoning capabilities in large language models. By encouraging step-by-step thinking. CoT prompting allows models to perform complex reasoning tasks effectively without needing additional training data. The benefits are particularly pronounced in large models (e.g., models with over 100 billion parameters), which exhibit improved reasoning capacities as they follow these structured reasoning prompts. Source Paper

*status: approved*

## Confabulation

A term originating in psychiatry, where it is used to refer to a patient’s tendency to create false narratives either with the intent to deceive, or because they actually believe what they are saying is true. This definition closely aligns to what LLMs do when they generate output that is not based on real-world input or information. An LLM may confabulate output for a variety of reasons. When they do, the resulting output may be false, nonsensical, offensive, dangerous, or contain references to things that do not exist. Often the LLM will present such information confidently despite the fact that it is incorrect. Using the term confabulation to refer to this behavior is preferred to the term hallucinate among AI scientists and researchers, as it avoids anthropomorphizing the underlying technology. Source Wikipedia

*status: approved*

## Context Window

The maximum amount of text or information that an AI model can process and consider at one time when generating a response or performing a task. It represents the AI’s “working memory” or “short-term memory,” allowing it to maintain coherence and relevance in its outputs, especially during complex interactions. It represents the AI’s “working memory” or “short-term memory,” allowing it to maintain coherence and relevance in its outputs, especially during complex interactions.The context window is typically measured in tokens, which are the smallest units of text that the model can process. These tokens can represent words, parts of words, or even punctuation marks. For example, a model with a context window of 4,096 tokens can process and “remember” approximately 3,000 words of English text at once. Source Blog

*status: approved*

## Data Augmentation

In the process of artificially generating new data from existing data, primarily to train machine learning models. It involves creating modified copies of a dataset by making small changes to the original data, such as geometric transformations for images or word replacements for text. Source MITRE

*status: standard*

## Dataset Contamination

The unintended overlap between training data and evaluation datasets. It occurs when parts or characteristics of a test set leak into a training set, compromising the separation between the two datasets. The negative consequences can include: Dataset/Model Contamination is different from the similarly named Data Model Poisoning LLM04 which describes intentionally manipulating the dataset to compromise the model’s security, effectiveness or ethical behavior. Source Academic Paper

*status: approved*

## Deep Learning

A subset of machine learning that employs neural networks with multiple layers to automatically learn hierarchical representations of data. Source NIST

*status: standard*

## Embeddings

Embeddings are numerical representations of data, typically in the form of vectors, that capture the relationships and features of the data in a lower-dimensional space. They are commonly used to encode high-dimensional or complex data, such as words, images, or graphs, into a form that machine learning models can more efficiently process. Source IEEE Paper

*status: approved*

## Few-Shot Learning

Since LLMs are autoregressive predictors, their performance in applications can be improved by providing examples of the inputs and outputs expected for the application in the model’s context that is prepended to the user query before evaluation by the LLM. This allows the model to more naturally complete the autoregressive tasks. Source NIST

*status: standard*

## Fine-Tuning

Refers to the process of adapting a pre-trained model to perform specific tasks or to specialize in a particular domain. This phase follows the initial pre-training phase and involves training the model further on task-specific data. This is often a supervised learning task. Source NIST

*status: standard*

## Foundation Model

Also known as large X model (LxM), is a machine learning or deep learning model that is trained on vast datasets so it can be applied across a wide range of use cases. Source Wikipedia

*status: approved*

## Generative

Type of machine learning methods which learn from the data distribution and can generate new examples from distribution. Source NIST

*status: standard*

## Generative Pre-Trained Transformer

An artificial neural network based on the transformer architecture, pre-trained on large data sets of unlabelled text, and able to generate novel human-like content. Today, this is the predominant architecture for natural language processing tasks. Source NIST

*status: standard*

## Hallucinate

An incorrect response from an AI system, or false information in an output that is presented as factual information. Source Singapore Companion Guide On Securing AI Systems

*status: standard*

## Inference Engine

A component of the system that applies logical rules to the knowledge base to deduce new information. Source Wikipedia

*status: approved*

## Large Language Model (LLM)

A type of AI model that processes and generates human-like text. LLMs are specifically trained on large data sets of natural language to generate human like output. Source Singapore Companion Guide On Securing AI Systems

*status: standard*

## LLM Agent

An advanced AI system which uses Large Language Models (LLMs) to perform complex tasks, make decisions, and interact autonomously with users or other systems. Agents are designed to understand, generate, and process human language in sophisticated ways, going beyond simple text generation. LLM Agents typically consist of four main components:

*status: approved*

## Machine Learning

A subset of AI that incorporates aspects of computer science, mathematics, and coding. Machine learning focuses on developing algorithms and models that can learn from data, and make predictions and decisions about new data. Source Singapore Companion Guide On Securing AI Systems

*status: standard*

## Model Card

Model cards are short documents accompanying trained machine learning (ML) models that provide benchmarked evaluation in a variety of conditions, such as across different cultural, demographic, or phenotypic groups and intersectional groups that are relevant to the intended application domains. Model cards also disclose the context in which models are intended to be used, details of the performance evaluation procedures, and other relevant information. This framework can be used to document any trained ML model. Source OECD

*status: standard*

## NLP (Natural Language Processing:)

A subset of AI that enables computers to understand spoken and written human language. NLP enables features like text and speech recognition on devices. Source Singapore Companion Guide On Securing AI Systems

*status: standard*

## One-shot learning

A technique where a model is trained to recognize and categorize new objects or patterns after being exposed to just a single example. It leverages the idea that once a model has learned how to generalize features effectively, it can apply this knowledge to new instances with minimal data. Source Blog

*status: approved*

## Reinforcement Learning

Type of machine learning in which an agent interacts with the environment and learns to take actions which optimize a reward function. Source NIST

*status: standard*

## Reinforcement Learning Policy

A mapping from states to actions. It determines what action an agent should take when in a particular state of the environment. The primary goal of a policy is to maximize cumulative rewards over time1. It serves as a strategy for the agent to make optimal decisions. Types of Policies:

*status: approved*

## Red Teaming

A group of people authorized and organized to emulate a potential adversary’s attack or exploitation capabilities against an enterprise’s security posture. The Red Team’s objective is to improve enterprise cybersecurity by demonstrating the impacts of successful attacks and by demonstrating what works for the defenders (i.e., the Blue Team) in an operational environment.” (CNSS 2015 [80]) Traditional red-teaming might combine physical and cyber attack elements, attack multiple systems, and aims to evaluate the overall security posture of an organization. Penetration testing (pen testing), in contrast, tests the security of a specific application or system. In AI discourse, red-teaming has come to mean something closer to pen testing, where the model may be rapidly or continuously tested by a set of evaluators and under conditions other than normal operation. Source NIST

*status: standard*

## Self-supervised learning (SSL)

A paradigm in machine learning where a model is trained on a task using the data itself to generate supervisory signals, rather than relying on externally-provided labels. Self-supervised learning more closely imitates the way humans learn to classify objects. Source Wikipedia

*status: approved*

## Sentient AI

Artificial consciousness also known as machine consciousness, synthetic consciousness or digital consciousness is the consciousness hypothesized to be possible in artificial intelligence. Source Wikipedia

*status: approved*

## Supervised learning

Type of machine learning methods based on labeled data. Source NIST

*status: standard*

## Transformer

A type of deep learning architecture that exploits a multi-head attention mechanism. Transformers address some of the limitations of long short-term memory, and became widely used in natural language processing, although it can also process other types of data such as images in the case of vision transformers. Source Wikipedia

*status: approved*

## Transfer learning

A machine learning technique in which knowledge learned from a task is reused in order to boost performance on a related task. For example, for image classification, knowledge gained while learning to recognize cars could be applied when trying to recognize trucks. Source Wikipedia

*status: approved*

## Turing Test

A test of a machine’s ability to exhibit intelligent behaviour equivalent to, or indistinguishable from, that of a human, developed by Alan Turing in 1950. Source Wikipedia

*status: approved*

## Unsupervised learning

Type of machine learning methods based on unlabeled data. Source NIST

*status: standard*

## Zero-shot learning

( ZSL ): a problem setup in deep learning where, at test time, a learner observes samples from classes which were not observed during training, and needs to predict the class that they belong to. Source Academic Paper

*status: approved*

