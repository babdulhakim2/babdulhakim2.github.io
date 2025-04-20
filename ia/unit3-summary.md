---
layout: default
title: Unit 3 - Agent Architectures
permalink: /ia/unit3-summary/
---

# Unit 3: Agent Architectures

## Overview

Unit 3 explores various approaches to agent architectures, examining their historical development, comparative advantages, and practical applications. The unit investigates how different architectural models influence agent capabilities and performance across diverse problem domains.

## Key Concepts

- **Symbolic Reasoning Agents**: Knowledge-based systems that rely on explicit symbolic representations and logical reasoning
- **Reactive Architectures**: Systems that generate responses directly from environmental stimuli without complex internal representations
- **BDI (Belief-Desire-Intention)**: Architecture that models agents with mental states representing knowledge, goals, and commitments
- **Subsumption Architecture**: Layered approach where simple behaviors can be combined to create complex emergent behaviors

## Learning Outcomes

- Critically evaluate a range of agent architectures
- Select an appropriate architecture for a given task
- Explain the difference between intentions and desires

## Reflection Notes

Agent architectures provide the structural frameworks that determine how an agent perceives, reasons, and acts in its environment. Maes (1991, p.116) defines an architecture as a methodology that "specifies how the agent can be decomposed into a set of component modules and how these modules should interact" to transform sensor data and internal states into actions.

Symbolic agents represent a classical AI approach where reasoning occurs through manipulation of explicit symbolic representations. However, as Brooks (1991, p.140) argues, these systems face fundamental challenges in translating real-world complexity into accurate symbolic descriptions—the "transduction problem"—and in performing symbol manipulation efficiently.

Reactive architectures emerged as a response to these limitations. Brooks' (1991, p.142) subsumption architecture demonstrates how complex behaviors can emerge from simple reactive components without requiring complex internal models. This approach proved remarkably effective for robotic applications where real-time response was critical.

The BDI model bridges reactive and deliberative approaches by structuring agent reasoning around beliefs, desires, and intentions. Bratman et al. (1988, p.351) distinguish between desires (potential influencers of action) and intentions (committed plans), noting that "intentions are conduct-controlling pro-attitudes, ones that we are disposed to retain without reconsideration." This distinction allows agents to maintain goal-directed behavior while remaining responsive to environmental changes.

Collective agent behaviors, as described by Reynolds (1987), demonstrate how simple local rules can generate complex coordinated behaviors without central control—a principle increasingly important in multi-agent systems.

### References

Bratman, M.E., Israel, D.J. & Pollack, M.E. (1988) 'Plans and Resource‐bounded Practical Reasoning', _Computational Intelligence_, 4(3), pp. 349-355.

Brooks, R.A. (1991) 'Intelligence Without Representation', _Artificial Intelligence_, 47(1-3), pp. 139-159.

Maes, P. (1991) 'The Agent Network Architecture (ANA)', _SIGART Bulletin_, 2(4), pp. 115-120.

Reynolds, C.W. (1987) 'Flocks, Herds, and Schools: A Distributed Behavioral Model', _Computer Graphics_, 21(4), pp. 25-34.

---

[back to IA module](../../ia/)
