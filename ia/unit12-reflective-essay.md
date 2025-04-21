---
layout: default
title: Unit 12 - Reflective Essay
permalink: /ia/unit12-reflective-essay/
---

# Unit 12: Reflective Essay on Intelligent Agents

## Introduction

This reflective essay examines my journey through the Intelligent Agents module using Rolfe et al.'s (2001) reflective model (What? So what? Now what?). As a software engineer transitioning to AI engineering, this module has significantly reshaped my understanding of agent-based systems and their applications in modern AI contexts.

## What? The Learning Experience

### Initial Expectations and Knowledge Base

Approaching this module with a background in software engineering, I anticipated a heavy focus on reinforcement learning given its prominence in current AI discussions. My knowledge was primarily shaped by exposure to modern AI applications like large language models (LLMs). I had minimal understanding of intelligent agents' historical foundations dating back to the 1980s, including agent communication languages like KQML, agent architectures, and their philosophical underpinnings.

The literature on agent communication languages, particularly Finin et al.'s (1994) seminal work on KQML, opened my eyes to how early researchers had formalized agent interaction patterns. As they explain, KQML provides "a language and protocol for exchanging information and knowledge" (p.456) that standardizes communication regardless of agents' internal architectures – a principle still relevant in today's AI ecosystems.

### Development Team Project Experience

In Unit 6, our team developed an [AI-Based Performance Monitoring and Fitness Data Analysis System](/assets/docs/Development Team Project - Project Report.pdf) that applied multi-agent system principles to fitness tracking. Initially, collaboration presented challenges due to varying perspectives – one team member prioritized security aspects while another focused on AI analysis components.

Our solution employed five specialized agents handling distinct responsibilities (Tomasino, 2025):

- Data Retrieval Agent for extracting Fitbit data
- Data Validation Agent for ensuring data integrity
- AI Analysis Agent for pattern recognition
- Reporting Agent for archiving records
- Security Agent for managing encryption

This collaborative process taught me the importance of clearly defined agent roles and communication protocols. I often found myself frustrated when discussions became circular, but these moments ultimately led to deeper understanding. When team members proposed solutions that didn't align with agent-based principles, I had to practice patience while guiding discussions back to the module's core concepts.

### Individual Implementation

Building on our team design, I developed "FitnessMAS," a working implementation that explored agent architectures and communication in greater depth. This hands-on experience transformed abstract concepts into concrete implementation challenges as I created:

1. Three agent types (reactive, deliberative, and hybrid)
2. A BDI architecture with explicit beliefs, desires, and intentions
3. Speech act-based communication with KQML-inspired performatives
4. A domain ontology for fitness concepts

The coding process was both challenging and rewarding. I particularly struggled with implementing the BDI reasoning cycle but felt immense satisfaction when my agents successfully communicated and coordinated their actions – a moment that crystallized my understanding of agency and autonomy.

## So What? Analysis and Significance

### Bridging Historical Foundations with Modern Applications

This module revealed how many challenges in modern AI systems were anticipated decades ago. As Russell and Norvig (2021, p.34) note, "the agent-based view of AI is now widely accepted," yet many practitioners work with these systems without appreciating their conceptual origins.

Working with edge computing concepts in our fitness system highlighted fascinating parallels with agent autonomy. As Satyanarayanan (2017, p.33) states, edge computing "enables real-time analytics and decision making" – directly applicable to autonomous agents. This insight helped me recognize that modern AI applications, despite their sophisticated neural architectures, still operate within established agent paradigms.

The module's exploration of deep learning in Units 9-11 further contextualized how modern neural approaches relate to agent systems. While analyzing technologies like GPT models, I was struck by how these architectures, despite their statistical foundations, ultimately serve agent-like functions when deployed in real systems. They maintain beliefs (trained weights), pursue goals (minimize loss functions), and execute plans (inference processes) – effectively mapping to BDI components despite their different implementation paradigm.

### Ethical Dimensions and AI Alignment

A significant shift in my thinking concerned AI alignment. Before this module, I viewed alignment primarily as a technical optimization problem. Studying agent communication revealed that alignment fundamentally involves values, communication, and social dynamics.

This perspective became evident in our fitness system through careful consideration of data validation and anomaly detection. As Ravinder et al. (2024) discuss, effective anomaly detection requires not just technical sophistication but considerations of what constitutes "normal" versus "anomalous" behavior – a fundamentally value-laden distinction.

The module coincided with my growing interest in AI alignment research, particularly through Bostrom's (2014) work on superintelligence. His warning that "the first superintelligence may shape the future of Earth-originating life" (p.157) underscores the importance of agent goal system design – a perspective that has profoundly influenced my approach to AI development.

## Now What? Future Applications and Development

### Professional Practice Enhancement

As I transition to AI engineering, the knowledge gained from this module provides critical foundations. I plan to incorporate BDI architectural principles when designing systems using LLMs, maintaining clear separation between belief systems, desires, and intentions to address the goal alignment challenges I've encountered in professional work.

For communication between AI components, I'll draw inspiration from speech act theory, creating more robust and interpretable interactions. As George and Thampi (2019) note, effective communication protocols are essential for managing vulnerability in distributed systems – directly applicable to modern AI architectures.

### Continued Learning Focus

Moving forward, I'll explore reinforcement learning's relationship to classical agent architectures. The unexpected connections between speech act theory and modern prompt engineering suggest fertile ground for innovation in my work with LLMs.

The ethical dimensions of AI development will remain central to my professional growth. Bostrom's work on superintelligence has prompted me to join communities focused on responsible AI development. As I noted in our Unit 9-11 discussion, "technical expertise must be paired with ethical reasoning to ensure AI systems remain beneficial as they grow more capable."

## Conclusion

This module has transformed my understanding of AI systems through its progression from theoretical concepts to collaborative design to individual implementation. The knowledge gained from studying agent architectures, communication protocols, and ethical considerations has provided a comprehensive perspective that bridges my software engineering experience with AI research traditions.

As AI technologies advance, intelligent agent design principles remain invaluable. Understanding these foundations has enhanced my technical capabilities and deepened my appreciation for creating truly intelligent systems aligned with human values.

## References

Bostrom, N. (2014) _Superintelligence: Paths, Dangers, Strategies_. Oxford: Oxford University Press.

Finin, T., Fritzson, R., McKay, D. & McEntire, R. (1994) 'KQML as an agent communication language', _CIKM_, 1, pp. 456-463.

George, G. and Thampi, S.M. (2019) 'Vulnerability-based risk assessment and mitigation strategies for edge devices in the Internet of Things', _Pervasive and Mobile Computing_, 59, p.101068.

Ravinder, M., Kulkarni, V., Shah, P.R., Shah, K. and Rao, A. (2024) 'Optimization of energy management and anomaly detection in smart grid analytics using deep learning', _International Conference on Integrated Circuits, Communication, and Computing Systems_, 1, pp. 1-6.

Rolfe, G., Freshwater, D. & Jasper, M. (2001) _Critical reflection in nursing and the helping professions: a user's guide_. Basingstoke: Palgrave Macmillan.

Russell, S. & Norvig, P. (2021) _Artificial Intelligence: A Modern Approach_. 4th edn. Hoboken: Pearson.

Satyanarayanan, M. (2017) 'The emergence of edge computing', _Computer_, 50(1), pp.30-39.

Tomasino, A. (2025) 'Knowledge-Based Coordination in cyber-physical systems via distributed ledger technologies'.

Wooldridge, M. (2020) _An Introduction to MultiAgent Systems_. 2nd edn. Chichester: John Wiley & Sons.

---

[back to IA module](../../ia/)
