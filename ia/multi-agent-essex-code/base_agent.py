#!/usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional, Set


class SpeechAct(Enum):
    """KQML-inspired speech acts for agent communication"""
    INFORM = "inform"      # Providing information
    REQUEST = "request"    # Requesting information or action
    QUERY = "query"        # Asking a question
    CONFIRM = "confirm"    # Confirming information
    DENY = "deny"          # Denying information
    COMMIT = "commit"      # Committing to action
    RECOMMEND = "recommend"  # Making a recommendation


class Belief:
    """Represents an agent's belief about the world"""
    def __init__(self, predicate: str, value: Any, confidence: float = 1.0):
        self.predicate = predicate
        self.value = value
        self.confidence = confidence  # 0.0 to 1.0
        self.timestamp = datetime.now()
    
    def __str__(self):
        return f"{self.predicate}({self.value}) [conf={self.confidence:.2f}]"
    
    def __eq__(self, other):
        if not isinstance(other, Belief):
            return False
        return self.predicate == other.predicate and self.value == other.value
    
    def __hash__(self):
        """Make Belief objects hashable for use in sets"""
        # Hash based on predicate only, since value might not be hashable
        return hash(self.predicate)


class Desire:
    """Represents an agent's goal or desire"""
    def __init__(self, name: str, priority: float = 0.5):
        self.name = name
        self.priority = priority  # 0.0 to 1.0
        self.achieved = False
    
    def __str__(self):
        status = "✓" if self.achieved else "○"
        return f"{status} {self.name} (priority={self.priority:.2f})"


class Intention:
    """Represents an agent's intention to act"""
    def __init__(self, action: str, params: Dict[str, Any], desire: Optional[Desire] = None):
        self.action = action
        self.params = params
        self.desire = desire
        self.completed = False
        self.timestamp = datetime.now()
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.action}({', '.join([f'{k}={v}' for k,v in self.params.items()])})"


class Message:
    """Message format for agent communication"""
    def __init__(self, sender: str, receiver: str, speech_act: SpeechAct, content: Dict[str, Any], conversation_id: Optional[str] = None):
        self.sender = sender
        self.receiver = receiver
        self.speech_act = speech_act
        self.content = content
        self.timestamp = datetime.now()
        self.conversation_id = conversation_id or f"conv-{int(datetime.now().timestamp())}"
    
    def __str__(self):
        return f"Message({self.speech_act.value}: {self.sender} → {self.receiver})"


class Agent(ABC):
    """Base agent class with BDI architecture"""
    
    def __init__(self, name: str, agent_type: str = "generic"):
        self.name = name
        self.agent_type = agent_type
        self.beliefs = set()  # Set of Belief objects
        self.desires = []     # List of Desire objects
        self.intentions = []  # List of Intention objects
        self.completed_intentions = []  # History of completed intentions
        self.message_queue = []  # Incoming messages
        self.message_history = []  # All messages sent and received
        self.log = []  # Activity log
        
        # Add the agent to global registry
        agent_registry.append(self)
    
    def add_belief(self, belief: Belief) -> None:
        """Add a new belief or update existing one"""
        # Remove any existing belief with the same predicate
        self.beliefs = {b for b in self.beliefs if b.predicate != belief.predicate}
        self.beliefs.add(belief)
        self.log_activity(f"Updated belief: {belief}")
    
    def get_belief(self, predicate: str) -> Optional[Belief]:
        """Get a belief by predicate"""
        for belief in self.beliefs:
            if belief.predicate == predicate:
                return belief
        return None
    
    def add_desire(self, desire: Desire) -> None:
        """Add a new desire"""
        self.desires.append(desire)
        # Sort by priority (highest first)
        self.desires.sort(key=lambda d: d.priority, reverse=True)
        self.log_activity(f"Added desire: {desire}")
    
    def add_intention(self, intention: Intention) -> None:
        """Add a new intention"""
        self.intentions.append(intention)
        self.log_activity(f"Added intention: {intention}")
    
    def complete_intention(self, intention: Intention) -> None:
        """Mark an intention as completed and move it to history"""
        intention.completed = True
        # Add to completed intentions history (max 5 recent ones)
        self.completed_intentions.append(intention)
        if len(self.completed_intentions) > 5:
            self.completed_intentions.pop(0)  # Remove oldest
        self.log_activity(f"Completed intention: {intention.action}")
    
    def send_message(self, receiver, speech_act: SpeechAct, content: Dict[str, Any], conversation_id: Optional[str] = None) -> Message:
        """Send a message to another agent"""
        message = Message(self.name, receiver.name, speech_act, content, conversation_id)
        self.message_history.append(message)
        self.log_activity(f"Sent {speech_act.value} message to {receiver.name}")
        receiver.receive_message(message)
        return message
    
    def receive_message(self, message: Message) -> None:
        """Receive a message from another agent"""
        self.message_queue.append(message)
        self.message_history.append(message)
        self.log_activity(f"Received {message.speech_act.value} message from {message.sender}")
    
    def log_activity(self, activity: str) -> None:
        """Log an agent activity"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {self.name}: {activity}"
        self.log.append(log_entry)
        

    @abstractmethod
    def execute(self) -> None:
        """Execute current intentions"""
        pass
    
    def process_messages(self) -> bool:
        """Process messages in queue"""
        if not self.message_queue:
            return False
        
        # Process all messages
        processed = len(self.message_queue) > 0
        for message in self.message_queue:
            self.interpret_message(message)
        
        self.message_queue = []
        return processed
    
    @abstractmethod
    def interpret_message(self, message: Message) -> None:
        """Interpret and act on a message"""
        pass
    
    def step(self) -> bool:
        """Perform one agent reasoning cycle (BDI loop)"""
        # Process incoming messages
        messages_processed = self.process_messages()
        
        # BDI cycle - only for non-reactive agents
        if self.agent_type != "reactive":
            self.deliberate()  # Update desires based on beliefs
            self.plan()        # Create intentions based on desires
        
        # Execute is always called as it's required for all agent types
        self.execute()     # Execute intentions
        
        # Return whether the agent did anything
        return messages_processed or len(self.intentions) > 0


# Global agent registry
agent_registry = [] 