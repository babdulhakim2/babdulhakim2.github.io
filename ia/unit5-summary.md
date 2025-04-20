---
layout: default
title: Unit 5 - Agent Communication
permalink: /ia/unit5-summary/
---

# Unit 5: Agent Communication

## Overview

Unit 5 explores how agents communicate with each other, focusing on the theoretical foundations of language use in agent systems. The unit examines speech act theory, agent communication languages (specifically KQML), and the role of ontologies in establishing shared understanding between agents.

## Key Concepts

- **Speech Acts**: Utterances that perform actions beyond simply conveying information
- **KQML (Knowledge Query and Manipulation Language)**: A protocol for agent communication consisting of performatives and content
- **Ontologies**: Formal representations of knowledge domains that support shared understanding
- **Correspondence Inclusion Dialogue (CID)**: A framework for agents to align ontologies without full disclosure

## Learning Outcomes

- Develop the ability to develop and work with ontologies
- Create inter-agent communications using relevant languages

## Reflection Notes

Speech act theory provides the theoretical foundation for agent communication by treating language as action. According to Searle (1969, p.16), "speaking a language is engaging in a rule-governed form of behavior," suggesting that communication is more than information transfer—it's a form of action that can change the state of the world. This perspective is particularly valuable in agent systems, where communication must facilitate goal achievement.

KQML exemplifies how speech act theory translates into practical agent communication protocols. It separates communication into performatives (the action being performed) and propositional content (what the communication is about), mirroring Searle's distinction between illocutionary force and propositional content (Searle, 1969, p.31). This separation enables agents to interpret not just the content of messages but also the intended actions those messages should trigger.

Ontologies address a fundamental challenge in agent communication: ensuring that agents share common understanding of terms. Without aligned ontologies, agents may use identical terms with different meanings or different terms for the same concepts, leading to communication failures. As Payne and Tamma (2014, p.518) note, "semantic heterogeneity can impede meaningful communication" between agents with different ontological assumptions.

The decentralized nature of multi-agent systems presents a particular challenge for ontology alignment. Traditional alignment approaches assume centralized processing, but agents often operate independently with private ontologies they may not wish to fully disclose. Correspondence Inclusion Dialogue offers one solution by allowing agents to "negotiate over ontological correspondences with asymmetric and incomplete knowledge" (Payne and Tamma, 2014, p.517), enabling partial alignment while preserving privacy.

### References

Payne, T.R. & Tamma, V. (2014) 'Negotiating over ontological correspondences with asymmetric and incomplete knowledge', _AAMAS_, 13(1), pp. 517-524.

Searle, J.R. (1969) _Speech Acts: An Essay in the Philosophy of Language_. Cambridge: Cambridge University Press.

---

[back to IA module](../../ia/)
