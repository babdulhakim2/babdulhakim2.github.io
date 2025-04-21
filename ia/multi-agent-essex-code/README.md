# FitnessMAS: Intelligent Fitness Multi-Agent System

This project demonstrates core concepts of intelligent agent systems in a fitness domain. It showcases multiple agent architectures, BDI (Belief-Desire-Intention) reasoning, speech act communication, and ontology-based knowledge representation.

## Requirements
**Only python 3.11 or newer**


## Quick Start

### Running Tests

```bash
python -m pytest tests/
```

Tests verify agent communication, BDI reasoning, data processing, and report generation.

### Running the Demo

```bash
python fitness_mas.py
```

The demo provides an interactive menu to:

- Run fitness analysis
- View agent mental states
- See communication logs
- Explore the ontology
- Enter custom commands

## Key Concepts Demonstrated

1. **Agent Architectures**

   - Reactive agents: Direct stimulus-response behavior
   - Deliberative agents: Goal-directed reasoning
   - Hybrid agents: Combining reactive and deliberative capabilities
   - Subsumption architecture: Layered behaviors with priority-based inhibition

2. **BDI Architecture**

   - Beliefs: Agent's knowledge about the world
   - Desires: Agent's goals
   - Intentions: Agent's plans to achieve goals

   The BDI cycle works as follows:

   - Beliefs are updated based on perceptions
   - Desires are formed/updated based on beliefs
   - Intentions (action plans) are created to achieve desires
   - Intentions are executed and cleared once completed
   - The cycle repeats

   When viewing the agent mental states, you'll see:

   - Current active intentions (if any)
   - Recently completed intentions (showing what actions were just taken)

3. **Advanced Reasoning Mechanisms**

   - Means-end reasoning: Backward reasoning from goals to the means to achieve them
   - Precondition-action-postcondition chains
   - Hierarchical subsumption of behaviors in layers

4. **Speech Acts (KQML-inspired)**

   - INFORM: Providing information
   - REQUEST: Requesting information or action
   - QUERY: Asking a question
   - And more...

5. **Ontology-Based Knowledge Representation**

   - Domain knowledge structured as classes and relations
   - Instance validation against class definitions
   - Fitness data stored using a formal knowledge representation
   - Demonstration of how structured data enables rich domain modeling

6. **Multi-Agent Communication**
   - Message passing with speech acts
   - Conversation tracking

## System Architecture

The system includes three specialized agents:

1. **FitnessDataAgent** (Reactive Architecture)

   - Retrieves fitness data from wearable devices (simulated)
   - Responds directly to data retrieval requests

2. **AnalysisAgent** (Deliberative Architecture with Means-End Reasoning)

   - Analyzes fitness data to extract insights
   - Generates personalized recommendations
   - Uses means-end reasoning to connect goals to actions
   - Plans with preconditions and postconditions

3. **UserInterfaceAgent** (Hybrid Architecture with Subsumption)
   - Handles user interaction
   - Displays fitness reports
   - Uses layered behaviors with subsumption architecture
   - Prioritizes actions based on behavior layers

## Workflow

The system follows this typical workflow:

1. **Data Collection Phase**:

   - UserInterfaceAgent initiates data collection (subsumption layer: data_collection)
   - Request sent to FitnessDataAgent via REQUEST speech act
   - FitnessDataAgent reactively retrieves fitness data
   - Data sent to AnalysisAgent via INFORM speech act

2. **Analysis Phase**:

   - AnalysisAgent uses means-end reasoning to create analysis plan
   - Preconditions checked (has_fitness_data)
   - Intention created to analyze data
   - Recommendations generated
   - Results sent to UserInterfaceAgent via INFORM speech act

3. **Reporting Phase**:
   - UserInterfaceAgent receives data (subsumption layer: report_generation)
   - Report generated
   - Report displayed to user

Throughout this process, each agent follows the BDI cycle:

- Beliefs updated from perceptions and messages
- Desires formed based on beliefs
- Intentions created to satisfy desires
- Actions executed and intentions completed
- New cycle begins

## File Structure

- `base_agent.py`: Core BDI agent classes and message passing
- `specialized_agents.py`: Reactive, deliberative and hybrid agents
- `fitness_ontology.py`: Domain knowledge representation
- `fitness_mas.py`: MAS coordinator and demo runner
- `tests/`: Test suite for system components

## Requirements

- Python 3.6+
- No external dependencies required
