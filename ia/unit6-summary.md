---
layout: default
title: Unit 6 - Working Together
permalink: /ia/unit6-summary/
---

# Unit 6: Working Together

## Overview

Unit 6 builds on the theoretical foundations of agent communication by focusing on practical applications of agent communication languages, specifically KQML and KIF. The unit provides hands-on experience with designing inter-agent dialogues using standard performatives and evaluates different approaches to agent communication.

## Key Concepts

- **KQML (Knowledge Query and Manipulation Language)**: The protocol layer of agent communication
- **KIF (Knowledge Interchange Format)**: The content layer for representing knowledge
- **Performatives**: Speech act types that define the intended actions of messages
- **Agent Dialogues**: Structured conversations between agents to accomplish specific tasks

## Learning Outcomes

- Develop dialogues using KQML/KIF or other appropriate agent communication languages
- Understand the use and deployment of ontologies as a means of knowledge sharing
- Evaluate the different approaches to agent communication

## Reflection Notes

KQML provides a standardized framework for agent communication that implements speech act theory in practice. According to Finin et al. (1994, p.456), KQML is "a language and protocol for exchanging information and knowledge" that allows agents to interact regardless of their internal architecture or implementation details. This standardization is crucial for open multi-agent systems where diverse agents must collaborate.

The language separates communication into three distinct layers: content, message, and communication. This separation of concerns allows agents to focus on the appropriate level of abstraction when processing messages. Particularly important is the distinction between the message layer (KQML performatives) and the content layer (typically expressed in KIF), which parallels the distinction between illocutionary force and propositional content in speech act theory (Finin et al., 1994, p.458).

KQML's performatives, such as ask, tell, achieve, and advertise, enable rich communicative interactions beyond simple information exchange. These performatives allow agents to request actions, make commitments, query knowledge bases, and establish collaborative relationships. By standardizing these speech acts, KQML creates a common language for agent interaction while remaining neutral about the internal representations used by individual agents.

Despite its strengths, KQML faces challenges in real-world deployment. Semantic ambiguity can arise when agents interpret performatives differently, and the lack of formal semantics in early versions made verification difficult. Additionally, as Finin et al. (1994, p.462) note, practical implementations must address issues of message routing, agent naming, and security that extend beyond the basic language specification.

### References

Finin, T., Fritzson, R., McKay, D. & McEntire, R. (1994) 'KQML as an agent communication language', _CIKM_, 1, pp. 456-463.

---

[back to IA module](../../ia/) | [view agent dialogue activity](../../ia/agent-dialogues/)
