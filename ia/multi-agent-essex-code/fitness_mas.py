#!/usr/bin/env python3

import time
import random
from typing import Dict, List, Any

from base_agent import agent_registry, SpeechAct
from specialized_agents import FitnessDataAgent, AnalysisAgent, UserInterfaceAgent
from fitness_ontology import fitness_ontology, convert_fitness_data_to_ontology, create_fitness_report_in_ontology


class FitnessMAS:
    """Multi-Agent System for fitness analysis and reporting"""
    
    def __init__(self):
        # Clear any existing agents
        global agent_registry
        agent_registry.clear()
        
        # Create specialized agents
        self.data_agent = FitnessDataAgent("FitnessDataAgent")
        self.analysis_agent = AnalysisAgent("AnalysisAgent")
        self.ui_agent = UserInterfaceAgent("UserInterfaceAgent")
        
        print("Fitness Multi-Agent System initialized with 3 specialized agents:")
        print(f"- {self.data_agent.name} (Reactive Agent)")
        print(f"- {self.analysis_agent.name} (Deliberative Agent)")
        print(f"- {self.ui_agent.name} (Hybrid Agent)")
    
    def start_analysis(self, user_id="default_user"):
        """Start the fitness analysis process"""
        print(f"\nStarting fitness analysis for user {user_id}...")
        
        # UI agent initiates the process
        self.ui_agent.send_message(
            self.data_agent,
            SpeechAct.REQUEST,
            {"action": "retrieve_fitness_data", "user_id": user_id}
        )
        
        # Clear existing ontology instances for clean demo
        self._clear_ontology_instances()
    
    def _clear_ontology_instances(self):
        """Clear existing ontology instances for a fresh start"""
        fitness_ontology.instances = {}
    
    def process_user_command(self, command: str) -> str:
        """Process a user command via the UI agent"""
        return self.ui_agent.process_user_input(command)
    
    def run_cycle(self, wait_time=0.2, max_cycles=15):
        """Run the BDI reasoning cycle for all agents"""
        for cycle in range(max_cycles):
            any_activity = False
            
            print(f"\nRunning agent cycle {cycle+1}...")
            
            # Run each agent's reasoning cycle
            for agent in agent_registry:
                active = agent.step()
                any_activity = any_activity or active
                
                # Store data in ontology when available
                self._update_ontology(agent)
                
            # If no agent did anything, we can stop
            if not any_activity and cycle > 0:
                print(f"All agents idle, stopping after {cycle+1} cycles")
                break
                
            # Wait between cycles
            time.sleep(wait_time)
    
    def _update_ontology(self, agent):
        """Update ontology with agent's belief data"""
        fitness_data = agent.get_belief("fitness_data")
        if fitness_data and hasattr(fitness_data, "value"):
            # Store fitness data in ontology
            convert_fitness_data_to_ontology(fitness_data.value)
        
        # Store report in ontology if available
        report = agent.get_belief("fitness_report")
        if report and hasattr(report, "value"):
            create_fitness_report_in_ontology(report.value)
    
    def display_agent_beliefs(self):
        """Display the current beliefs of all agents"""
        print("\n=== AGENT BELIEFS ===")
        for agent in agent_registry:
            print(f"\n{agent.name} ({agent.agent_type} agent) Beliefs:")
            if not agent.beliefs:
                print("  No beliefs")
            for belief in agent.beliefs:
                # Truncate large belief values for display
                value_str = str(belief.value)
                if len(value_str) > 100:
                    value_str = value_str[:100] + "..."
                print(f"  • {belief.predicate}: {value_str}")
    
    def display_agent_desires(self):
        """Display the current desires of all agents"""
        print("\n=== AGENT DESIRES ===")
        for agent in agent_registry:
            print(f"\n{agent.name} ({agent.agent_type} agent) Desires:")
            if not agent.desires:
                print("  No active desires")
            for desire in agent.desires:
                status = "✓" if desire.achieved else "○"
                print(f"  {status} {desire.name} (priority: {desire.priority:.2f})")
    
    def display_agent_intentions(self):
        """Display the current intentions of all agents"""
        print("\n=== AGENT INTENTIONS ===")
        for agent in agent_registry:
            print(f"\n{agent.name} ({agent.agent_type} agent) Intentions:")
            
            # Display active intentions
            if not agent.intentions:
                print("  No active intentions")
            else:
                print("  Active intentions:")
                for intention in agent.intentions:
                    status = "✓" if intention.completed else "○"
                    print(f"    {status} {intention.action}")
                    print(f"        params: {intention.params}")
                    if intention.desire:
                        print(f"        for desire: {intention.desire.name}")
            
            # Display recently completed intentions
            if agent.completed_intentions:
                print("\n  Recently completed intentions:")
                for intention in agent.completed_intentions:
                    print(f"    ✓ {intention.action}")
                    print(f"        params: {intention.params}")
                    if intention.desire:
                        print(f"        for desire: {intention.desire.name}")
    
    def display_communication_log(self, max_messages=10):
        """Display the recent communications between agents"""
        print("\n=== AGENT COMMUNICATION LOG ===")
        
        # Collect all messages from agents
        all_messages = []
        for agent in agent_registry:
            all_messages.extend(agent.message_history)
        
        # Sort by timestamp and take most recent
        all_messages.sort(key=lambda m: m.timestamp, reverse=True)
        recent_messages = all_messages[:max_messages]
        
        if not recent_messages:
            print("  No messages exchanged yet")
        
        # Display in reverse order to show most recent last
        for msg in reversed(recent_messages):
            print(f"  {msg.timestamp.strftime('%H:%M:%S')} | {msg.sender} → {msg.receiver}: " 
                  f"{msg.speech_act.value.upper()} {str(msg.content)[:50]}")
    
    def display_ontology_instances(self, class_name=None):
        """Display instances in the fitness ontology"""
        print("\n=== FITNESS ONTOLOGY INSTANCES ===")
        
        if class_name:
            instances = fitness_ontology.get_instances_of_type(class_name)
            print(f"\nInstances of {class_name}:")
            for i, instance in enumerate(instances):
                print(f"  {i+1}. {instance}")
        else:
            # Show counts by class
            class_counts = {}
            for instance_id, instance in fitness_ontology.instances.items():
                class_type = instance["type"]
                if class_type not in class_counts:
                    class_counts[class_type] = 0
                class_counts[class_type] += 1
            
            for cls, count in class_counts.items():
                print(f"  {cls}: {count} instances")


def run_interactive_demo():
    """Run an interactive demonstration of the Fitness MAS"""
    print("\n" + "="*60)
    print("FITNESS MULTI-AGENT SYSTEM DEMONSTRATION".center(60))
    print("="*60)
    print("This demo showcases intelligent agent concepts:")
    print("- BDI architecture (Beliefs, Desires, Intentions)")
    print("- Different agent types (Reactive, Deliberative, Hybrid)")
    print("- Advanced reasoning mechanisms (Means-End, Subsumption)")
    print("- Speech act based communication")
    print("- Domain ontology for fitness knowledge representation")
    
    # Create the multi-agent system
    fitness_mas = FitnessMAS()
    
    while True:
        print("\n" + "-"*60)
        print("MAIN MENU".center(60))
        print("-"*60)
        print("1. Run Fitness Analysis")
        print("2. View Agent Mental States (BDI)")
        print("3. View Agent Communication Log")
        print("4. View Fitness Ontology")
        print("5. Enter Custom Command")
        print("6. Exit Demo")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            user_id = input("\nEnter user ID (or press Enter for default): ")
            if not user_id.strip():
                user_id = f"user_{random.randint(1000, 9999)}"
            
            fitness_mas.start_analysis(user_id)
            print("\nRunning agent cycles...")
            print("(Watch for means-end reasoning in AnalysisAgent and subsumption architecture in UserInterfaceAgent)")
            fitness_mas.run_cycle()
            
            # Display the report
            print(fitness_mas.process_user_command("show report"))
            
            # Show a prompt to inform the user about viewing intentions
            print("\nTip: To see agent intentions that executed during analysis,")
            print("     select option 2 'View Agent Mental States (BDI)' from the menu.")
            
        elif choice == '2':
            print("\n=== AGENT MENTAL STATES (BDI MODEL) ===")
            print("Observing how different agent architectures process information:")
            print("- FitnessDataAgent: Reactive (stimulus-response)")
            print("- AnalysisAgent: Deliberative with means-end reasoning")
            print("- UserInterfaceAgent: Hybrid with subsumption architecture\n")
            
            fitness_mas.display_agent_beliefs()
            fitness_mas.display_agent_desires()
            fitness_mas.display_agent_intentions()
            
        elif choice == '3':
            print("\n=== AGENT COMMUNICATION (SPEECH ACTS) ===")
            print("Showing message exchange using KQML-inspired speech acts:")
            print("- INFORM: Sharing information (e.g., fitness data)")
            print("- REQUEST: Asking for actions (e.g., data retrieval)")
            print("- QUERY: Asking for knowledge\n")
            
            fitness_mas.display_communication_log()
            
        elif choice == '4':
            print("\n=== FITNESS DOMAIN ONTOLOGY ===")
            print("The ontology represents the domain knowledge in a structured format:")
            print("- Classes: represent concepts like User, HeartRate, Steps")
            print("- Relations: define connections like 'User hasMetric HeartRate'")
            print("- Instances: specific data points from the analysis\n")
            
            print("Available classes in the fitness ontology:")
            for i, class_name in enumerate(fitness_ontology.classes.keys()):
                print(f"  {i+1}. {class_name}")
            
            class_choice = input("\nEnter class number to view instances (or Enter for summary): ")
            if class_choice.strip() and class_choice.isdigit():
                class_idx = int(class_choice) - 1
                if 0 <= class_idx < len(fitness_ontology.classes):
                    class_name = list(fitness_ontology.classes.keys())[class_idx]
                    fitness_mas.display_ontology_instances(class_name)
                else:
                    print("Invalid class number")
            else:
                fitness_mas.display_ontology_instances()
            
        elif choice == '5':
            command = input("\nEnter command for UI agent: ")
            result = fitness_mas.process_user_command(command)
            print(result)
            
        elif choice == '6':
            print("\nThank you for exploring the Fitness Multi-Agent System!")
            print("Key demonstrated concepts:")
            print("- Different agent architectures (reactive, deliberative, hybrid)")
            print("- BDI reasoning cycle (beliefs → desires → intentions → actions)")
            print("- Means-end reasoning (goals to subgoals to actions)")
            print("- Subsumption architecture (layered behaviors with priority)")
            print("- Ontology-based knowledge representation")
            print("- Speech act communication between agents")
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    run_interactive_demo() 