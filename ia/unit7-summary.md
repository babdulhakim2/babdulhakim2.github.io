---
layout: default
title: Unit 7 - Natural Language Processing
permalink: /ia/unit7-summary/
---

# Unit 7: Natural Language Processing (NLP)

## Overview

Unit 7 examines Natural Language Processing (NLP), a rapidly evolving field enabling intelligent agents to understand and generate human language. The unit explores the theoretical foundations, technical approaches, and practical challenges of building systems that can effectively process natural language in all its complexity and ambiguity.

## Key Concepts

- **Levels of Linguistic Analysis**: Syntax (grammar structure), semantics (meaning), and pragmatics (contextual interpretation)
- **Statistical NLP**: Probabilistic approaches to language modeling, including word embeddings and vector space models
- **Formal Grammars**: Rule-based systems for parsing language structure
- **Parsing Approaches**: Constituency-based and dependency-based methods for analyzing sentence structure

## Learning Outcomes

- Evaluate the difficulties involved in developing and deploying NLP systems
- Understand the core principles of NLP technologies

## Reflection Notes

Natural Language Processing presents unique challenges due to the inherent complexity and ambiguity of human language. As Mikolov et al. (2013, p.3111) note, capturing the "distributed representations of words" is essential for meaningful language processing, yet traditional approaches struggle with issues of polysemy (multiple meanings), ambiguity, and context-sensitivity.

Statistical approaches to NLP have proven particularly effective for certain tasks. Word embedding techniques like Word2Vec, described by Mikolov et al. (2013, p.3112), represent words as dense vectors in a continuous space where semantic relationships are preserved. This enables mathematical operations on word meanings—for example, "king - man + woman ≈ queen"—capturing semantic relationships in a computationally tractable form.

For extracting structured relationships from text, pattern-based approaches remain valuable. Hearst (1992, p.539) pioneered techniques for automatically identifying hyponym relationships using lexico-syntactic patterns such as "X and other Y" or "Y such as X." These pattern-matching approaches continue to serve as the foundation for ontology learning and knowledge extraction systems.

Formal parsing techniques provide deeper structural analysis of language. Constituency parsing breaks sentences into hierarchical phrase structures, while dependency parsing, as Aqab and Tariq (2020, p.140) describe, models "the interlinking dependencies of words" as directed graphs. Each approach offers different advantages for applications ranging from question answering to sentiment analysis.

Despite significant advances, NLP systems still face substantial challenges in areas requiring world knowledge, understanding implicit meaning, or processing language that uses irony, sarcasm, or cultural references. These difficulties highlight why the Turing test remains unsolved and why NLP continues to be an active and critical area of research in intelligent agent development.

### References

Aqab, S. & Tariq, M.U. (2020) 'Handwriting recognition using artificial intelligence neural network and image processing', _International Journal of Advanced Computer Science and Applications_, 11(7), pp. 137-146.

Hearst, M.A. (1992) 'Automatic acquisition of hyponyms from large text corpora', _COLING_, 2, pp. 539-545.

Mikolov, T., Sutskever, I., Chen, K., Corrado, G.S. & Dean, J. (2013) 'Distributed representations of words and phrases and their compositionality', _Advances in neural information processing systems_, 1, pp. 3111-3119.

---

[back to IA module](../../ia/)
