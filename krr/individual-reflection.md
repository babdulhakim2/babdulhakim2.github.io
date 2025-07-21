---
layout: default
title: "Individual Reflection: Knowledge Representation and Reasoning Module"
---

# Individual Reflection: Knowledge Representation and Reasoning Module

## Introduction

This reflective essay examines my journey through the Knowledge Representation and Reasoning (KRR) module using Rolfe et al.'s (2001) framework. As a software developer with machine learning experience, this module reshaped my understanding of how humans organize knowledge and how these principles guide modern AI systems toward interpretability and safety.

## What? The Learning Experience

### Historical Awakening and Philosophical Foundations

Approaching from a machine learning background, I expected focus on modern AI techniques. Instead, discovering knowledge representation's roots in Aristotle's logic proved eye-opening. The progression from cave paintings to formal ontologies revealed humanity's persistent need to externalize knowledge (Weststeijn, 2011).

*[Image 1: Timeline visualization showing evolution of knowledge representation from Aristotelian logic through medieval scholasticism to modern ontologies, with key milestones and philosophical contributions marked chronologically]*

Most fascinating was how Aristotle's categorization questions remain central to contemporary AI challenges. Reading Marquis, Papini and Prade (2020), I realized formal logic principles established millennia ago now underpin systems I work with daily.

### Intelligence Task Ontology (ITO) Case Study

Analyzing the ITO - a knowledge graph with 1,100 AI task classes and 26,000 benchmark results - proved eye-opening (Blagec et al., 2022). Critical evaluation revealed design tensions: the monolithic "Benchmarking" superclass violated modularity principles, while Papers-with-Code dependency created coverage bias toward vision/NLP. Most concerning was sustainability - two curators handling exponential AI literature growth seemed unsustainable.

This exercise taught me to look beyond impressive statistics to underlying design decisions. The ITO's real-world applications in research policy and regulatory compliance demonstrated ontologies' practical value, but also highlighted how design choices echo through entire systems.

### Job Matching Ontology Development

Building my own ontology transformed theoretical understanding into practical knowledge. Your seminar discussions on gold standard versus corpus-based approaches became crucial - no established employment ontology exists, forcing methodological innovation.

*[Image 2: Infographic showing the employment paradox - split visualization depicting employer talent shortages on one side and unemployed qualified candidates on the other, with semantic gap illustrated in the middle]*

The hybrid approach I developed combined lessons from ITO analysis with practical constraints:

| Implementation Aspect | Challenge Encountered | Resolution Approach |
|----------------------|----------------------|-------------------|
| Dataset Selection | No standardized job market ontology | Combined NYC Open Data with Kaggle resume dataset |
| Methodology Choice | Competing approaches (gold standard vs corpus-based) | Hybrid approach integrating multiple methodologies |
| Skill Categorization | 61 diverse skill types requiring classification | Systematic analysis and hierarchical organization |
| Performance Validation | Limited benchmarks for ontological job matching | Custom evaluation metrics and precision testing |

*[Image 3: Network diagram showing semantic relationships between job roles, with "Python Developer" and "Data Scientist" connected through shared skills like "Programming," "Statistical Analysis," and "Problem Solving," demonstrating how ontological reasoning bridges keyword gaps]*

The iterative development proved messier than textbook examples - initial automated extraction required extensive manual refinement, and balancing expressiveness with performance became an ongoing challenge.

### Collaborative Learning Experience

Unit 1's collaborative discussion proved most engaging, where my argument that knowledge representation predates computing technology generated substantive peer responses. While I participated less actively in later discussions, the initial exchanges with international peers provided valuable perspectives on different cultural approaches to knowledge organization.

## So What? Analysis and Significance

### Bridging Ancient Wisdom and Modern AI Challenges

This module revealed connections between historical knowledge representation and contemporary AI challenges. Working with SNOMED CT examples showed how centuries-old taxonomic principles guide clinical systems. Similarly, exploring ontologies like Gene Ontology demonstrated how formal structures enable scientific automation.

*[Image 5: Conceptual bridge illustration connecting ancient library/scroll imagery on one side to modern AI neural network visualization on the other, with ontological structures forming the bridge between them]*

The implications for AI safety became clear. As large language models deploy in critical systems, ontological frameworks provide structured approaches to understanding AI behavior. Rather than treating AI as black boxes, knowledge representation offers principled methods for encoding human values.

### Professional Application: Genomics Data Normalization

My recent genomics work exemplified practical KRR applications. Our team normalized large-scale genomic datasets where laboratories used inconsistent terminologies. Drawing from this module, we developed standardization protocols using PubMed ontologies, BRENDA database, and authoritative sources.

*[Image 6: Flowchart showing genomic data normalization process - raw laboratory data from multiple sources flowing through ontological standardization layers (PubMed, BRENDA, etc.) to produce normalized, standardized output]*

This demonstrated how ontological thinking transforms chaotic data into structured knowledge, enabling automated analysis and reducing manual overhead. The project's success validated knowledge engineering principles from this module.

### AI Interpretability and Mechanistic Understanding

Working with AI systems daily, I appreciate knowledge representation's role in interpretability. Large language models excel at pattern recognition but lack explicit reasoning structures. Ontological approaches offer complementary capabilities - providing structured, auditable reasoning paths.

The connection between traditional KRR and mechanistic interpretability fascinates me. While neural networks encode knowledge in distributed representations, ontologies maintain explicit relationships humans can inspect. This transparency proves crucial for high-stakes applications.

### Technical Performance and Scalability Insights

The implemented system demonstrated practical viability while revealing scalability considerations:

| Performance Metric | Value | Context |
|-------------------|-------|---------|
| Precision@5 | 82% | Top 5 job recommendations |
| Skill Coverage | 89% | Job requirements successfully mapped |
| Processing Time | 4.2s | For 7,543 instances |
| Reasoning Time | 1.8s | Full dataset inference |

*[Image 7: Performance dashboard visualization showing key metrics - precision rates, processing times, and scalability curves with annotated insights about ontological reasoning overhead]*

Scalability challenges emerged with larger datasets, highlighting trade-offs between expressiveness and computational efficiency that characterize real-world knowledge engineering.

## Now What? Future Applications and Development

### Professional Practice Enhancement

This module's insights directly influence my AI engineering practice. I now incorporate ontological thinking when designing systems, maintaining explicit separation inspired by BDI architectures. The job matching work demonstrates practical application potential in HR technology.

For AI component communication, I draw inspiration from formal reasoning approaches, creating more interpretable interactions. Experience with real datasets provides confidence in scaling knowledge-based solutions.

### AI Safety and Alignment Applications

The module's emphasis on formal knowledge representation aligns with my interest in AI safety research. As AI systems become more powerful, ontological frameworks offer structured approaches to encoding human values and ensuring alignment.

*[Image 8: Conceptual diagram showing AI safety architecture with ontological layers providing interpretability, value alignment, and behavioral constraints around a central AI system core]*

Moving forward, I plan exploring how traditional KRR techniques can enhance large language model safety through structured reasoning overlays.

### Continued Learning and Research Directions

I will pursue advanced semantic web technologies and enterprise-scale ontology management. The connection between traditional KRR and modern AI systems suggests innovation opportunities, particularly in explainable AI contexts.

Short-term goals include contributing to open-source knowledge representation projects. Medium-term objectives involve applying KRR techniques in genomics and healthcare contexts, leveraging domain ontologies like SNOMED CT.

## Emotional Response and Personal Development

### Initial Challenges and Growth

Initially, formal logic and ontology complexity seemed disconnected from practical machine learning. Unit 4's Prolog exercises proved particularly challenging, requiring shifts from imperative to declarative thinking. However, persistence revealed logical reasoning's power for structured problem-solving.

Protégé's complexity initially frustrated implementation efforts. The breakthrough came during reasoning exercises when automated inference revealed relationships I hadn't explicitly defined, demonstrating ontological systems' emergent properties.

### Transformation of Perspective

Unit 11's emerging applications generated appreciation for KRR's real-world impact. Seeing how ontologies support enterprise systems transformed my perception from academic exercise to essential professional capability.

The iterative refinement concepts changed my approach to complex projects. Previously thinking linearly about system design, KRR introduced iterative development through testing and reasoning - approaches now influencing my AI methodology.

### Professional Skills Development

| Skill Area | Evidence from Module | Professional Application |
|------------|---------------------|-------------------------|
| Critical Thinking | Analyzing peer arguments, evaluating methodologies | AI system evaluation and design decisions |
| Research Skills | Literature review, academic citation practices | Staying current in rapidly evolving AI fields |
| Technical Communication | Explaining ontological concepts to diverse audiences | Communicating AI capabilities/limitations to stakeholders |
| Ethical Awareness | Understanding Open/Closed World Assumptions | Responsible AI development and deployment |
| Problem-solving | Debugging Prolog programs, ontology validation | Systematic approach to complex AI issues |

These competencies transfer to professional contexts where understanding AI system behavior and ensuring responsible deployment become critical.

## Conclusion

This KRR module transformed my understanding of knowledge representation from historical curiosity to essential modern capability. The journey from Aristotelian logic to contemporary ontology engineering revealed both continuity of human knowledge organization and power of formal approaches for AI development.

The combination of historical perspective, practical implementation with real datasets, and philosophical reflection created comprehensive learning experiences. Most significantly, developing a job matching ontology with 7,543 instances while applying principles to genomics normalization demonstrated KRR's practical viability across diverse domains.

Moving forward, I'm equipped with technical skills and conceptual frameworks necessary for responsible AI engineering. As AI systems become increasingly powerful, the module's emphasis on formal knowledge representation provides essential tools for ensuring systems remain interpretable, controllable, and aligned with human values.

The ancient quest to organize human knowledge continues in our modern AI age, and this module provided both historical context and practical tools to contribute meaningfully to that endeavor.

## References

Blagec, K., Barbosa-Silva, A., Ott, S. & Samwald, M. (2022) 'A curated, ontology-based, large-scale knowledge graph of artificial intelligence tasks and benchmarks', *Scientific Data*, 9(1), pp. 322.

Brachman, R. and Levesque, H. (2004) *Knowledge Representation and Reasoning*. Germany: Elsevier Science.

Debellis, M. (2021) *A Practical Guide to Building OWL Ontologies Using Protégé 5.5 and Plugins*.

ManpowerGroup. (2023) *Talent Shortage Survey*. Available at: https://www.manpowergroup.com/talent-shortage

Marquis, P., Papini, O. and Prade, H. (2020) *A Guided Tour of Artificial Intelligence Research: Volume I: Knowledge Representation, Reasoning and Learning*. Switzerland: Springer.

Mochol, M., Wache, H. and Nixon, L. (2007) 'Improving the Accuracy of Job Search with Semantic Techniques', *International Conference on Business Information Systems*, pp. 301-313.

NYC Jobs. (2023) NYC Open Data Portal. Available at: https://data.cityofnewyork.us/

Open University Business Barometer. (2022) *Skills and Training in the Workplace*. Milton Keynes: Open University.

Rolfe, G., Freshwater, D. & Jasper, M. (2001) *Critical reflection in nursing and the helping professions: a user's guide*. Basingstoke: Palgrave Macmillan.

UpdatedResumeDataSet.csv. (2023) Resume Dataset. Kaggle.

Weststeijn, T. (2011) 'From hieroglyphs to universal characters: Pictography in the early modern Netherlands', *Netherlands Yearbook for History of Art*, 61(1), pp. 238–281.

---

[← Back to KRR Module Home](/krr/)