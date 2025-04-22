<h1>Prompt Engineering</h1>

> Prompt Engineering is the art and science of crafting effective inputs for Large Language Models (LLMs) to produce desired outputs. It's a crucial skill in GenAI related tasks, allowing users to harness the full potential of LLMs for various tasks.

<h2>📖 Fundamentals of Prompt Design</h2>

- **Clarity**: Be specific and unambiguous in your instructions.
- **Context**: Porvider relevant background information.
- **Constraints**: Set boundaries for the AI's response.
- **Examples**: Include sample inputs and outputs when possible.
- **Format**: Specify the desired structure of the response.

<h2>📌 Important Prompt Techniques</h2>

1. **Chain of Thought (CoT)**: A strategy to enhance reasoning by articulating intermediate steps.
2. **Zero-Shot Chain of Thought (Zero-Shot-CoT)**: Applying CoT without prior examples or training on similar tasks.
3. **Few-Shot Chain of Thought (Few-Shot-CoT)**: Using a few examples to guide the reasoning process.
4. **ReAct (Reasoning and Acting)**: Combining reasoning with action to improve responses.
5. **Tree of Thoughts (ToT)**: Organizing thoughts hierarchically for better dicision-making.
6. **Self-Consistency**: Ensuring responses are stable and consistent across queries.
7. **Hypothetical Document Embeddings (HyDE)**: Leveraging embeddings to represent potential documents for reasoning.
8. **Least-to-Most Prompting**: Starting with simpler prompts and gradually increasing complexity.
9. **Prompt Chaining**: Connecting multiple prompts to create a coherent narrative.
10. **Graph Prompting**: Using graph structures to represent complex relationships.
11. **Recursive Prompting**: Iteratively refining prompts to enhance results.
12. **Generated Knowledge**: Utilizing generated content as a basis for further reasoning.
13. **Automatic Reasoning and Tool-Use (ART)**: Automating reasoning processes and tool interactions.
14. **Automatic Prompt Engineer (APE)**: Tools to automatically generate and refine prompts.
15. **Additional Prompt Techniques**:
    - **Reflexion**: Reflecting on past reponses to improve future prompts.
    - **Prompt Ensembling**: Combining multiple prompts for enhanced results.
    - **Directional Stimulus Prompting**: Guiding responses with targeted prompts.

<h2>🔎 Prompt Optimization Techniques</h2>

1. **Iterative refinement**: Start with a basic prompt and gradually improve it based on the results.
2. **A/B testing**: Compare different versions of a prompt to see which performs better.
3. **Prompt libraries**: Create and maintain a collection of effective prompts for reuse.
4. **Collaborative prompting**: Combine insights from multiple team members to create stronger prompts.

<h2>⚖️ Ethical Considerations in Prompt Engineering</h2>

1. **Bias mitigation**: Be aware of and actively work to reduce biases in prompts and outputs.
2. **Content safety**: Implement safeguards against generating harmful or inappropriate content.
3. **Data privacy**: Avoid including sensitive information in prompts.

<h2>✅ Evaluating Prompt Effectiveness</h2>

1. **Relevance**: Does the output address the intended task or question?
2. **Accuracy**: Is the information provided correct and up-to-date?
3. **Coherence**: Is the response well-structured and logical?
4. **Creativity**: For open-ended tasks, does the output demonstrate originality?
5. **Efficiency**: Does the prompt produce the desired result with minial back-and-forth?

<h2>🧩 LLM Parameters</h2>

1. `temperature`

    This parameter controls the randomness of the model's output. A lower temperature (closer to 0) makes the output more deterministic and focused, while a higher temparature (closer to 1) makes it more random and creative.

    - **Range**: Usually 0 to 1
    - **Default**: Often around 0.7, but this can vary
    - **Use cases**: Lower for factual or precise task, higher for creative tasks

2. `max_output_token`

    This sets the maximum length of the generated text in tokens. A token is generally a word or a part of a word.

    - **Range**: Model-dependent, but often up to several thousand
    - **Default**: Varies, but often around 1024 to 2048
    - **Use cases**: Adjust based on the desired length of the response

3. `top_p (nucleus sampling)`

    This parameter sets a probability threshold for token selection. The model will only consider tokens whose cumulative probability exceeds this threshold. Let's visualize.
    ![alt_text](../assets/images/top_p_sampling.png)

    Having set p = 0.92, *top_p* sampling picks the *minimum* number of words to exceed together p = 92% of the probability mass. In the first example, this included the 9 most likely words, whereas it only has to pick the top 3 words in the second example to exceed 92%. Quite simple actually! It can be seem that it keeps a wide range of words where the next word is arguably less predictable ("The"), and only a few words when the next word seems more predictable ("The", "car"). 

    - **Range**: 0 to 1
    - **Default**: Often around 0.9
    - **Use cases**: Lower values make output more focused, higher values allow for more diversity

4. `top_k`

    This parameter limits the number of highest probability tokens to consider at each step of generation. In top_k, the *k* most likely next words are filtered and the probability mass is redistributed among only those *k* next words.
    ![alt_text](../assets/images/top_k_sampling.png)

    Having set top_k = 6, in both sampling steps we limit out sampling pool to 6 words. In the 6 most likely words, two-thirds of the whole probability in the first step, it includes almost all of the probability mass in the second step. Nevertheless, we see that it successfully eliminates the rather weird candidates ("not", "the", "small", "told") in the second sampling step.

    - **Range**: Positive integers, often up to 100 or more
    - **Default**: Often around 40
    - **Use cases**: Lower values make output more predictable output, higher for more variety


Explore at read more at [How to generate text: using different decoding methods for language generation with Transformers](https://huggingface.co/blog/how-to-generate)