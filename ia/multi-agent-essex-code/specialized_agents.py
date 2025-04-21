#!/usr/bin/env python3

import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

from base_agent import Agent, Belief, Desire, Intention, SpeechAct, Message


class ReactiveAgent(Agent):
    """A reactive agent that responds directly to perceptions without planning"""
    
    def __init__(self, name: str):
        super().__init__(name, agent_type="reactive")
        self.reactive_rules = {}  # Stimulus-response rules
    
    def add_rule(self, stimulus: str, response_func):
        """Add a reactive rule (stimulus -> response)"""
        self.reactive_rules[stimulus] = response_func
        self.log_activity(f"Added reactive rule for stimulus: {stimulus}")
    
    # def deliberate(self) -> None:
    #     """Reactive agents don't deliberate extensively"""
    #     pass
    
    # def plan(self) -> None:
    #     """Reactive agents don't plan ahead"""
    #     pass
    
    def execute(self) -> None:
        """Execute reactive rules based on current beliefs"""
        for belief in self.beliefs:
            if belief.predicate in self.reactive_rules:
                self.log_activity(f"Triggering rule for {belief.predicate}")
                self.reactive_rules[belief.predicate](self, belief.value)
    
    def interpret_message(self, message: Message) -> None:
        """React to messages based on speech act"""
        # Convert message content to beliefs
        if message.speech_act == SpeechAct.INFORM:
            for key, value in message.content.items():
                self.add_belief(Belief(key, value))
                
        # Directly execute requests if we have a rule for it
        elif message.speech_act == SpeechAct.REQUEST:
            action = message.content.get("action")
            if action in self.reactive_rules:
                self.reactive_rules[action](self, message.content)


class DeliberativeAgent(Agent):
    """A deliberative agent with explicit reasoning about goals"""
    
    def __init__(self, name: str):
        super().__init__(name, agent_type="deliberative")
        self.knowledge_base = {}  # For more complex reasoning
    
    def deliberate(self) -> None:
        """Update desires based on current beliefs and knowledge"""
        # Example: If we believe the user's fitness is below target,
        # create a desire to generate recommendations
        fitness_belief = self.get_belief("fitness_level")
        if fitness_belief and fitness_belief.value == "Below target":
            if not any(d.name == "generate_recommendations" for d in self.desires):
                self.add_desire(Desire("generate_recommendations", priority=0.8))
    
    def plan(self) -> None:
        """Create intentions based on current desires"""
        # Clear completed intentions
        self.intentions = [i for i in self.intentions if not i.completed]
        
        # Only plan if we don't have active intentions
        if not self.intentions:
            # Get the highest priority unachieved desire
            active_desires = [d for d in self.desires if not d.achieved]
            if active_desires:
                desire = active_desires[0]
                if desire.name == "generate_recommendations":
                    self.add_intention(Intention(
                        "analyze_fitness_data",
                        {"detail_level": "high"},
                        desire
                    ))
    
    def execute(self) -> None:
        """Execute current intentions"""
        for intention in self.intentions[:]:  # Create a copy to iterate over
            if not intention.completed:
                self.log_activity(f"Executing intention: {intention.action}")
                
                if intention.action == "analyze_fitness_data":
                    # Find fitness data in beliefs
                    steps_belief = self.get_belief("steps")
                    hr_belief = self.get_belief("heart_rate")
                    
                    if steps_belief and hr_belief:
                        recommendations = self.analyze_fitness_data(
                            steps_belief.value, 
                            hr_belief.value
                        )
                        self.add_belief(Belief("recommendations", recommendations))
                        
                        # Communicate results
                        for agent in agent_registry:
                            if agent.name != self.name:
                                self.send_message(
                                    agent,
                                    SpeechAct.INFORM,
                                    {"recommendations": recommendations}
                                )
                        
                        # Mark intention as completed and move to history
                        self.complete_intention(intention)
                        self.intentions.remove(intention)
                        
                        # Mark desire as achieved if it exists
                        if intention.desire:
                            intention.desire.achieved = True
    
    def analyze_fitness_data(self, steps: int, heart_rate: List[int]) -> List[str]:
        """Analyze fitness data and generate recommendations"""
        recommendations = []
        
        avg_hr = sum(heart_rate) / len(heart_rate)
        
        if steps < 7500:
            recommendations.append("Increase daily steps to at least 10,000")
        
        if avg_hr > 100:
            recommendations.append("Consider more cardiovascular training")
        
        if not recommendations:
            recommendations.append("Maintain current routine - progress looks good")
            
        self.log_activity(f"Generated {len(recommendations)} fitness recommendations")
        return recommendations
    
    def interpret_message(self, message: Message) -> None:
        """Interpret messages using deliberative reasoning"""
        if message.speech_act == SpeechAct.INFORM:
            # Update beliefs from information
            for key, value in message.content.items():
                self.add_belief(Belief(key, value))
                
        elif message.speech_act == SpeechAct.REQUEST:
            # Create a desire based on the request
            action = message.content.get("action")
            if action:
                self.add_desire(Desire(action, priority=0.7))
                self.log_activity(f"Created desire from request: {action}")
                
        elif message.speech_act == SpeechAct.QUERY:
            # Respond to queries with our beliefs
            query_key = message.content.get("query")
            if query_key:
                belief = self.get_belief(query_key)
                if belief:
                    for agent in agent_registry:
                        if agent.name == message.sender:
                            self.send_message(
                                agent,
                                SpeechAct.INFORM,
                                {query_key: belief.value},
                                message.conversation_id
                            )
                            break


class HybridAgent(Agent):
    """A hybrid agent with both reactive and deliberative capabilities"""
    
    def __init__(self, name: str):
        super().__init__(name, agent_type="hybrid")
        self.reactive_rules = {}  # For reactive layer
        self.plans = {}           # For deliberative layer
    
    def add_rule(self, stimulus: str, response_func):
        """Add a reactive rule"""
        self.reactive_rules[stimulus] = response_func
    
    def add_plan(self, goal: str, plan_func):
        """Add a plan for achieving a goal"""
        self.plans[goal] = plan_func
    
    def deliberate(self) -> None:
        """Update desires based on beliefs (deliberative layer)"""
        # Check if we need fitness data
        if not self.get_belief("fitness_data") and not any(d.name == "get_fitness_data" for d in self.desires):
            self.add_desire(Desire("get_fitness_data", priority=0.9))
        
        # Check if we need to generate a report
        recommendations = self.get_belief("recommendations")
        fitness_data = self.get_belief("fitness_data")
        if recommendations and fitness_data and not any(d.name == "generate_report" for d in self.desires):
            self.add_desire(Desire("generate_report", priority=0.6))
    
    def plan(self) -> None:
        """Create intentions from desires (deliberative layer)"""
        # Clear completed intentions
        self.intentions = [i for i in self.intentions if not i.completed]
        
        # Only plan if we don't have active intentions
        if not self.intentions:
            # Get highest priority unachieved desire
            active_desires = [d for d in self.desires if not d.achieved]
            if active_desires:
                desire = active_desires[0]
                
                if desire.name == "get_fitness_data":
                    self.add_intention(Intention(
                        "request_fitness_data",
                        {"user_id": "current_user"},
                        desire
                    ))
                
                elif desire.name == "generate_report":
                    self.add_intention(Intention(
                        "compile_fitness_report",
                        {},
                        desire
                    ))
    
    def execute(self) -> None:
        """Execute both reactive rules and deliberative plans"""
        # First, reactive layer (higher priority)
        for belief in self.beliefs:
            if belief.predicate in self.reactive_rules:
                self.log_activity(f"Reactive: Triggering rule for {belief.predicate}")
                self.reactive_rules[belief.predicate](self, belief.value)
        
        # Then, deliberative layer
        for intention in self.intentions[:]:  # Create a copy to iterate over
            if not intention.completed:
                self.log_activity(f"Deliberative: Executing {intention.action}")
                
                if intention.action == "request_fitness_data":
                    # Find an agent that can provide fitness data
                    for agent in agent_registry:
                        if agent.name != self.name:
                            self.send_message(
                                agent,
                                SpeechAct.REQUEST,
                                {
                                    "action": "retrieve_fitness_data",
                                    "user_id": intention.params["user_id"]
                                }
                            )
                    # Mark as completed and move to history
                    self.complete_intention(intention)
                    self.intentions.remove(intention)
                
                elif intention.action == "compile_fitness_report":
                    # Get the necessary data from beliefs
                    fitness_data = self.get_belief("fitness_data")
                    recommendations = self.get_belief("recommendations")
                    
                    if fitness_data and recommendations:
                        report = self.generate_report(fitness_data.value, recommendations.value)
                        self.add_belief(Belief("fitness_report", report))
                        
                        # Mark as completed and move to history
                        self.complete_intention(intention)
                        self.intentions.remove(intention)
                        
                        # Mark desire as achieved if it exists
                        if intention.desire:
                            intention.desire.achieved = True
                            
                        # Notify other agents
                        for agent in agent_registry:
                            if agent.name != self.name:
                                self.send_message(
                                    agent,
                                    SpeechAct.INFORM,
                                    {"report_available": True, "report_id": report["report_id"]}
                                )
                        
                        self.log_activity(f"Generated report {report['report_id']}")
    
    def generate_report(self, fitness_data, recommendations) -> Dict:
        """Generate a fitness report"""
        report = {
            "report_id": f"FR-{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "user_id": fitness_data.get("user_id", "default_user"),
            "metrics": {
                "steps": fitness_data.get("steps", 0),
                "heart_rate_avg": sum(fitness_data.get("heart_rate", [70])) / len(fitness_data.get("heart_rate", [70])),
                "calories": fitness_data.get("calories", 0),
                "sleep_hours": fitness_data.get("sleep_hours", 0)
            },
            "fitness_level": self.determine_fitness_level(fitness_data),
            "recommendations": recommendations
        }
        
        self.log_activity(f"Generated report {report['report_id']}")
        return report
    
    def determine_fitness_level(self, fitness_data) -> str:
        """Determine fitness level based on data"""
        steps = fitness_data.get("steps", 0)
        heart_rate = fitness_data.get("heart_rate", [70])
        avg_hr = sum(heart_rate) / len(heart_rate)
        
        if steps > 10000 and avg_hr < 85:
            return "Excellent"
        elif steps > 7500:
            return "Good"
        elif steps > 5000:
            return "Average"
        else:
            return "Below target"
    
    def interpret_message(self, message: Message) -> None:
        """Process messages using both reactive and deliberative approaches"""
        # Reactive response to certain speech acts
        if message.speech_act == SpeechAct.INFORM:
            # Update beliefs from information
            for key, value in message.content.items():
                self.add_belief(Belief(key, value))
        
        # Deliberative processing for more complex messages
        if message.speech_act == SpeechAct.REQUEST:
            action = message.content.get("action")
            if action == "get_report":
                report_belief = self.get_belief("fitness_report")
                if report_belief:
                    # Find the requesting agent
                    for agent in agent_registry:
                        if agent.name == message.sender:
                            self.send_message(
                                agent,
                                SpeechAct.INFORM,
                                {"fitness_report": report_belief.value},
                                message.conversation_id
                            )
                            break


class FitnessDataAgent(ReactiveAgent):
    """Agent responsible for retrieving fitness data"""
    
    def __init__(self, name: str):
        super().__init__(name)
        
        # Add reactive rules
        self.add_rule("retrieve_fitness_data", self.retrieve_data)
    
    def retrieve_data(self, agent, params):
        """Reactive rule to retrieve fitness data"""
        user_id = params.get("user_id", "default_user")
        self.log_activity(f"Retrieving fitness data for user {user_id}")
        
        # Simulate API call delay
        time.sleep(0.5)
        
        # Randomly generate fitness data
        # In a real-world scenario, this would be replaced with an API call to a fitness data provider
        # or a database query
        # For demonstration purposes, we generate random data
        fitness_data = {
            "user_id": user_id,
            "heart_rate": [random.randint(60, 150) for _ in range(10)],
            "steps": random.randint(5000, 15000),
            "calories": random.randint(1500, 3000),
            "sleep_hours": round(random.uniform(5.0, 9.0), 1),
            "active_minutes": random.randint(30, 120),
            "timestamp": datetime.now().isoformat()
        }
        
        # Store as belief
        self.add_belief(Belief("fitness_data", fitness_data))
        
        # Inform the requesting agent
        for agent in agent_registry:
            if isinstance(agent, DeliberativeAgent) or isinstance(agent, HybridAgent):
                self.send_message(
                    agent,
                    SpeechAct.INFORM,
                    {"fitness_data": fitness_data}
                )
        
        return fitness_data


class AnalysisAgent(DeliberativeAgent):
    """Agent responsible for analyzing fitness data and generating recommendations
    
    This agent demonstrates means-end reasoning, a goal-directed problem-solving
    approach that works backward from goals to determine the means to achieve them.
    
    Key components of means-end reasoning:
    1. Action library: Maps goals to actions with preconditions and postconditions
    2. Condition checking: Evaluates if necessary conditions are met
    3. Plan selection: Chooses actions that can achieve goals based on current state
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        # Means-end reasoning component: Maps goals to actions and their preconditions
        self.action_library = {
            "analyze_fitness": {
                "actions": ["analyze_fitness_data"],
                "preconditions": ["has_fitness_data"],
                "postconditions": ["has_recommendations"]
            },
            "generate_recommendations": {
                "actions": ["analyze_fitness_data"],
                "preconditions": ["has_fitness_data"],
                "postconditions": ["has_recommendations"]
            }
        }
    
    def check_condition(self, condition: str) -> bool:
        """Check if a condition is met based on current beliefs"""
        if condition == "has_fitness_data":
            return self.get_belief("fitness_data") is not None
        elif condition == "has_recommendations":
            return self.get_belief("recommendations") is not None
        return False
    
    def interpret_message(self, message: Message) -> None:
        """Process messages with special handling for fitness data"""
        super().interpret_message(message)
        
        # If we receive fitness data, create desire to analyze it
        if message.speech_act == SpeechAct.INFORM and "fitness_data" in message.content:
            fitness_data = message.content["fitness_data"]
            
            # Store the complete fitness data
            self.add_belief(Belief("fitness_data", fitness_data))
            
            # Extract and store key metrics as separate beliefs
            self.add_belief(Belief("steps", fitness_data["steps"]))
            self.add_belief(Belief("heart_rate", fitness_data["heart_rate"]))
            self.add_belief(Belief("sleep_hours", fitness_data["sleep_hours"]))
            self.add_belief(Belief("calories", fitness_data["calories"]))
            
            # Determine fitness level
            avg_hr = sum(fitness_data["heart_rate"]) / len(fitness_data["heart_rate"])
            
            if fitness_data["steps"] > 10000 and avg_hr < 85:
                fitness_level = "Excellent"
            elif fitness_data["steps"] > 7500:
                fitness_level = "Good"
            elif fitness_data["steps"] > 5000:
                fitness_level = "Average"
            else:
                fitness_level = "Below target"
                
            self.add_belief(Belief("fitness_level", fitness_level))
            
            # Create desire to analyze this data
            if not any(d.name == "analyze_fitness" for d in self.desires):
                self.add_desire(Desire("analyze_fitness", priority=0.9))
    
    def deliberate(self) -> None:
        """Update desires based on current beliefs and knowledge using means-end reasoning"""
        super().deliberate()
        
        # Use means-end reasoning to determine what desires to create
        if self.check_condition("has_fitness_data") and not self.check_condition("has_recommendations"):
            # We have fitness data but no recommendations - create a desire to generate them
            if not any(d.name == "analyze_fitness" for d in self.desires):
                self.log_activity("Means-end reasoning: Creating 'analyze_fitness' desire based on available data")
                self.add_desire(Desire("analyze_fitness", priority=0.9))
                
        # If fitness level is below target, add a higher priority desire to generate detailed recommendations
        fitness_belief = self.get_belief("fitness_level")
        if fitness_belief and fitness_belief.value == "Below target":
            if not any(d.name == "generate_recommendations" for d in self.desires):
                self.log_activity("Means-end reasoning: Creating 'generate_recommendations' desire for below-target fitness")
                self.add_desire(Desire("generate_recommendations", priority=1.0))  # Higher priority
    
    def plan(self) -> None:
        """Create intentions based on current desires using means-end reasoning"""
        # Clear completed intentions
        self.intentions = [i for i in self.intentions if not i.completed]
        
        # Only plan if we don't have active intentions
        if not self.intentions:
            # Get the highest priority unachieved desire
            active_desires = [d for d in self.desires if not d.achieved]
            if active_desires:
                desire = active_desires[0]
                
                # Use means-end reasoning to select an action for the desire
                if desire.name in self.action_library:
                    action_plan = self.action_library[desire.name]
                    
                    # Check if preconditions are met
                    preconditions_met = all(self.check_condition(cond) for cond in action_plan["preconditions"])
                    
                    if preconditions_met:
                        # Create intention for the first action in the plan
                        self.log_activity(f"Means-end reasoning: Selected action '{action_plan['actions'][0]}' for desire '{desire.name}'")
                        self.add_intention(Intention(
                            action_plan["actions"][0],
                            {"detail_level": "high" if desire.name == "generate_recommendations" else "standard"},
                            desire
                        ))
                    else:
                        self.log_activity(f"Means-end reasoning: Cannot satisfy preconditions for desire '{desire.name}'")
                
    def execute(self) -> None:
        """Execute current intentions"""
        for intention in self.intentions[:]:  # Create a copy to iterate over
            if not intention.completed:
                self.log_activity(f"Executing intention: {intention.action}")
                
                if intention.action == "analyze_fitness_data":
                    # Get the fitness data from beliefs
                    fitness_data = self.get_belief("fitness_data")
                    
                    if fitness_data:
                        # Generate recommendations
                        recommendations = self.analyze_fitness_data(
                            fitness_data.value.get("steps", 0), 
                            fitness_data.value.get("heart_rate", [70]),
                            fitness_data.value.get("sleep_hours", 0)
                        )
                        
                        # Store recommendations as belief
                        self.add_belief(Belief("recommendations", recommendations))
                        
                        # Communicate results to UI agent
                        for agent in agent_registry:
                            if isinstance(agent, UserInterfaceAgent):
                                self.send_message(
                                    agent,
                                    SpeechAct.INFORM,
                                    {
                                        "recommendations": recommendations,
                                        "fitness_level": self.get_belief("fitness_level").value,
                                        "fitness_data": fitness_data.value
                                    }
                                )
                        
                        # Mark intention as completed and move to history
                        self.complete_intention(intention)
                        self.intentions.remove(intention)
                        
                        # Mark desire as achieved if it exists
                        if intention.desire:
                            intention.desire.achieved = True
    
    def analyze_fitness_data(self, steps: int, heart_rate: List[int], sleep_hours: float) -> List[str]:
        """Analyze fitness data and generate recommendations"""
        self.log_activity(f"Analyzing fitness data: steps={steps}, heart_rate={heart_rate[:3]}..., sleep={sleep_hours}")
        recommendations = []
        
        # Calculate average heart rate
        avg_hr = sum(heart_rate) / len(heart_rate)
        
        # Generate personalized recommendations
        if steps < 7500:
            recommendations.append("Increase daily steps to at least 10,000 for better cardiovascular health")
        
        if avg_hr > 100:
            recommendations.append("Consider more cardiovascular training to improve heart efficiency")
        
        if sleep_hours < 7:
            recommendations.append("Aim for 7-8 hours of sleep for optimal recovery and performance")
        
        if len([hr for hr in heart_rate if hr > 140]) > 2:
            recommendations.append("Your heart rate spikes suggest high intensity. Consider adding recovery sessions")
        
        # Always provide positive feedback
        if steps > 8000:
            recommendations.append("Good job on staying active with your step count!")
        
        if sleep_hours >= 7:
            recommendations.append("You're getting adequate sleep which is excellent for recovery")
        
        # If no specific recommendations, add a general one
        if not recommendations:
            recommendations.append("Keep up your current routine - your fitness metrics look good")
        
        self.log_activity(f"Generated {len(recommendations)} fitness recommendations")
        return recommendations


class UserInterfaceAgent(HybridAgent):
    """Agent responsible for user interaction and report presentation with subsumption architecture
    
    This agent demonstrates subsumption architecture, a layered approach to behavior
    control where higher priority behaviors can inhibit or override lower priority ones.
    
    Key components of subsumption architecture:
    1. Behavior layers: Organized by priority (higher layers can inhibit lower ones)
    2. Activation conditions: Each layer activates based on specific environmental conditions
    3. Inhibition: Higher priority behaviors can suppress lower priority ones
    4. Emergent behavior: Complex behavior emerges from the interaction of simple layers
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self.user_queries = []
        self.last_report = None
        self.processing_report = False  # Flag to prevent duplicate report generation
        
        # Set up behavior layers for subsumption architecture
        # Lower layers are overridden by higher layers
        self.behavior_layers = [
            {"name": "report_display", "priority": 1},  # Lowest priority - display existing reports
            {"name": "data_collection", "priority": 2},  # Request and process data
            {"name": "report_generation", "priority": 3},  # Generate reports from data
            {"name": "user_interaction", "priority": 4}   # Highest priority - respond to user input
        ]
        
        # Add reactive rule for handling new reports
        self.add_rule("report_available", self.handle_new_report)
    
    def handle_new_report(self, agent, report_id):
        """React to new report availability"""
        self.log_activity(f"New report {report_id} is available")
        
        # Request the report
        for agent in agent_registry:
            if agent.name != self.name:
                self.send_message(
                    agent,
                    SpeechAct.REQUEST,
                    {"action": "get_report", "report_id": report_id}
                )
    
    def interpret_message(self, message: Message) -> None:
        """Process messages with special handling for reports using subsumption architecture"""
        super().interpret_message(message)
        
        # Generate a report when we receive recommendations and fitness data (report_generation layer)
        if message.speech_act == SpeechAct.INFORM and "recommendations" in message.content and not self.processing_report:
            self.log_activity("Subsumption: Activating report_generation layer")
            
            # Set flag to prevent duplicate report generation
            self.processing_report = True
            
            # Store the recommendations
            self.add_belief(Belief("recommendations", message.content["recommendations"]))
            
            if "fitness_data" in message.content:
                # New analysis started - clear previous report
                self.last_report = None
                
                # Store new fitness data
                self.add_belief(Belief("fitness_data", message.content["fitness_data"]))
            
            if "fitness_level" in message.content:
                self.add_belief(Belief("fitness_level", message.content["fitness_level"]))
            
            # Create desire to generate a report
            if not any(d.name == "generate_report" for d in self.desires):
                self.add_desire(Desire("generate_report", priority=0.9))
                
        # Store report when received from another agent (report_display layer)
        elif message.speech_act == SpeechAct.INFORM and "fitness_report" in message.content:
            self.log_activity("Subsumption: Activating report_display layer")
            self.last_report = message.content["fitness_report"]
            self.log_activity(f"Received report {self.last_report['report_id']}")
    
    def deliberate(self) -> None:
        """Update desires based on beliefs using subsumption architecture"""
        # Check if we need to generate a report based on received data (report_generation layer)
        recommendations = self.get_belief("recommendations")
        fitness_data = self.get_belief("fitness_data")
        
        if recommendations and fitness_data and not self.last_report and not any(d.name == "generate_report" for d in self.desires):
            self.log_activity("Subsumption: report_generation layer creating desire")
            self.add_desire(Desire("generate_report", priority=0.9))
    
    def plan(self) -> None:
        """Create intentions from desires using subsumption architecture layers"""
        # Apply subsumption architecture - higher layers can inhibit lower ones
        active_layer = None
        
        # Determine which layer should be active based on current state
        if any(d.name == "generate_report" for d in self.desires):
            active_layer = "report_generation"
        elif not self.get_belief("fitness_data"):
            active_layer = "data_collection"
        else:
            active_layer = "report_display"
            
        self.log_activity(f"Subsumption: Active layer is '{active_layer}'")
        
        # Call parent implementation for basic planning
        super().plan()
        
        # Clear completed intentions
        self.intentions = [i for i in self.intentions if not i.completed]
        
        # Only plan if we don't have active intentions
        if not self.intentions:
            # Get highest priority unachieved desire
            active_desires = [d for d in self.desires if not d.achieved]
            if active_desires:
                desire = active_desires[0]
                
                # Handle different layers with appropriate intentions
                if active_layer == "report_generation" and desire.name == "generate_report":
                    self.log_activity("Subsumption: Creating intention in report_generation layer")
                    self.add_intention(Intention(
                        "compile_fitness_report",
                        {},
                        desire
                    ))
                elif active_layer == "data_collection" and desire.name == "get_fitness_data":
                    self.log_activity("Subsumption: Creating intention in data_collection layer")
                    self.add_intention(Intention(
                        "request_fitness_data",
                        {"user_id": "current_user"},
                        desire
                    ))
    
    def execute(self) -> None:
        """Execute both reactive rules and deliberative plans using subsumption architecture"""
        # First, reactive layer (higher priority)
        for belief in self.beliefs:
            if belief.predicate in self.reactive_rules:
                self.log_activity(f"Reactive: Triggering rule for {belief.predicate}")
                self.reactive_rules[belief.predicate](self, belief.value)
        
        # Then, deliberative layer
        for intention in self.intentions[:]:  # Create a copy to iterate over
            if not intention.completed:
                self.log_activity(f"Deliberative: Executing {intention.action}")
                
                if intention.action == "compile_fitness_report":
                    # Get the necessary data from beliefs
                    fitness_data = self.get_belief("fitness_data")
                    recommendations = self.get_belief("recommendations")
                    fitness_level = self.get_belief("fitness_level")
                    
                    if fitness_data and recommendations:
                        # Generate the report
                        report = self.generate_report(
                            fitness_data.value, 
                            recommendations.value,
                            fitness_level.value if fitness_level else "Unknown"
                        )
                        
                        # Store the report
                        self.last_report = report
                        self.add_belief(Belief("fitness_report", report))
                        
                        # Mark as completed and move to history
                        self.complete_intention(intention)
                        self.intentions.remove(intention)
                        
                        self.log_activity(f"Generated fitness report {report['report_id']}")
                        
                        # Reset processing flag
                        self.processing_report = False
                            
                # Handle other intentions with parent implementation
                else:
                    super().execute()
    
    def process_user_input(self, query: str) -> str:
        """Process user queries and commands"""
        self.log_activity(f"Processing user input: {query}")
        self.user_queries.append(query)
        
        # Simple command processing
        if "start analysis" in query.lower():
            # Request fitness data collection
            for agent in agent_registry:
                if isinstance(agent, FitnessDataAgent):
                    self.send_message(
                        agent,
                        SpeechAct.REQUEST,
                        {"action": "retrieve_fitness_data", "user_id": "current_user"}
                    )
            return "Starting fitness analysis..."
        
        elif "show report" in query.lower():
            if self.last_report:
                return self.format_report_for_display(self.last_report)
            else:
                return "No fitness report available yet. Try starting an analysis first."
        
        elif "help" in query.lower():
            return """
Available commands:
- start analysis: Begin fitness data collection and analysis
- show report: Display the latest fitness report
- help: Show this help message
"""
        else:
            return f"I'm not sure how to handle '{query}'. Try 'help' for available commands."
    
    def format_report_for_display(self, report) -> str:
        """Format a report for user display"""
        timestamp = datetime.fromisoformat(report["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
======= FITNESS REPORT ({report['report_id']}) =======
User: {report['user_id']}
Date: {timestamp}

METRICS:
- Steps: {report['metrics']['steps']}
- Average Heart Rate: {report['metrics']['heart_rate_avg']:.1f} BPM
- Calories: {report['metrics']['calories']}
- Sleep: {report['metrics']['sleep_hours']} hours

FITNESS LEVEL: {report['fitness_level']}

RECOMMENDATIONS:
{chr(10).join(['- ' + rec for rec in report['recommendations']])}
==========================================
"""

    def generate_report(self, fitness_data, recommendations, fitness_level="Unknown") -> Dict:
        """Generate a fitness report"""
        report = {
            "report_id": f"FR-{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "user_id": fitness_data.get("user_id", "default_user"),
            "metrics": {
                "steps": fitness_data.get("steps", 0),
                "heart_rate_avg": sum(fitness_data.get("heart_rate", [70])) / len(fitness_data.get("heart_rate", [70])),
                "calories": fitness_data.get("calories", 0),
                "sleep_hours": fitness_data.get("sleep_hours", 0)
            },
            "fitness_level": fitness_level or self.determine_fitness_level(fitness_data),
            "recommendations": recommendations
        }
        
        self.log_activity(f"Generated report {report['report_id']}")
        return report
    
    def determine_fitness_level(self, fitness_data) -> str:
        """Determine fitness level based on data"""
        steps = fitness_data.get("steps", 0)
        heart_rate = fitness_data.get("heart_rate", [70])
        avg_hr = sum(heart_rate) / len(heart_rate)
        
        if steps > 10000 and avg_hr < 85:
            return "Excellent"
        elif steps > 7500:
            return "Good"
        elif steps > 5000:
            return "Average"
        else:
            return "Below target"

# Import at the end to avoid circular imports
from base_agent import agent_registry 