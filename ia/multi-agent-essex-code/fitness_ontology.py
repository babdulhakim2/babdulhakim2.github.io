#!/usr/bin/env python3

from typing import Dict, List, Any, Set, Optional
from datetime import datetime

class OntologyClass:
    """Base class for ontology definitions"""
    def __init__(self, name: str, properties: Dict[str, type] = None, parent: Optional['OntologyClass'] = None):
        self.name = name
        self.properties = properties or {}
        self.parent = parent
        self.subclasses = set()
        
        # Register as subclass of parent
        if parent:
            parent.subclasses.add(self)
    
    def __str__(self):
        return f"Class[{self.name}]"
    
    def get_all_properties(self) -> Dict[str, type]:
        """Get all properties including inherited ones"""
        all_properties = {}
        
        # Add parent properties first (can be overridden)
        if self.parent:
            all_properties.update(self.parent.get_all_properties())
        
        # Add own properties
        all_properties.update(self.properties)
        
        return all_properties
    
    def validate_instance(self, instance: Dict[str, Any]) -> List[str]:
        """Validate if an instance matches this class's schema"""
        errors = []
        all_properties = self.get_all_properties()
        
        # Check required properties
        for prop_name, prop_type in all_properties.items():
            if prop_name not in instance:
                errors.append(f"Missing required property: {prop_name}")
            else:
                # Check type
                value = instance[prop_name]
                if not isinstance(value, prop_type) and prop_type != Any:
                    errors.append(f"Property {prop_name} should be of type {prop_type.__name__}")
        
        return errors


class Relation:
    """Represents a relation between ontology classes"""
    def __init__(self, name: str, domain: OntologyClass, range_class: OntologyClass):
        self.name = name
        self.domain = domain  # From class
        self.range = range_class  # To class
    
    def __str__(self):
        return f"Relation[{self.name}: {self.domain.name} → {self.range.name}]"


class FitnessOntology:
    """Fitness domain ontology"""
    def __init__(self):
        self.classes = {}
        self.relations = {}
        self.instances = {}
        
        # Define the ontology
        self._build_ontology()
    
    def _build_ontology(self):
        # 1. Core classes
        self.add_class("Thing", {})
        self.add_class("Agent", {"name": str, "type": str}, parent="Thing")
        self.add_class("User", {"user_id": str, "age": int, "gender": str}, parent="Thing")
        self.add_class("FitnessMetric", {"timestamp": str, "user_id": str}, parent="Thing")
        
        # 2. FitnessMetric subclasses
        self.add_class("HeartRate", {"value": int, "resting": bool}, parent="FitnessMetric")
        self.add_class("Steps", {"count": int, "goal": int}, parent="FitnessMetric")
        self.add_class("Sleep", {"hours": float, "quality": str}, parent="FitnessMetric")
        self.add_class("Calories", {"burned": int, "goal": int}, parent="FitnessMetric")
        
        # 3. Activity and recommendation classes
        self.add_class("Activity", {"name": str, "duration": int, "intensity": str}, parent="Thing")
        self.add_class("Recommendation", {"text": str, "priority": float}, parent="Thing")
        self.add_class("FitnessGoal", {"name": str, "target": Any, "achieved": bool}, parent="Thing")
        
        # 4. Report class
        self.add_class("FitnessReport", {
            "report_id": str,
            "timestamp": str,
            "user_id": str,
            "fitness_level": str
        }, parent="Thing")
        
        # 5. Define relations
        self.add_relation("hasMetric", "User", "FitnessMetric")
        self.add_relation("generates", "Agent", "Recommendation")
        self.add_relation("performs", "User", "Activity")
        self.add_relation("contains", "FitnessReport", "FitnessMetric")
        self.add_relation("suggests", "FitnessReport", "Recommendation")
        self.add_relation("hasGoal", "User", "FitnessGoal")
    
    def add_class(self, name: str, properties: Dict[str, type], parent: Optional[str] = None):
        """Add a class to the ontology"""
        parent_class = self.classes.get(parent) if parent else None
        self.classes[name] = OntologyClass(name, properties, parent_class)
        return self.classes[name]
    
    def add_relation(self, name: str, domain: str, range_name: str):
        """Add a relation to the ontology"""
        domain_class = self.classes.get(domain)
        range_class = self.classes.get(range_name)
        
        if domain_class and range_class:
            self.relations[name] = Relation(name, domain_class, range_class)
            return self.relations[name]
        return None
    
    def add_instance(self, class_name: str, instance_id: str, data: Dict[str, Any]):
        """Add an instance of a class to the ontology"""
        if class_name in self.classes:
            # Validate against class schema
            errors = self.classes[class_name].validate_instance(data)
            if errors:
                raise ValueError(f"Instance validation errors: {', '.join(errors)}")
            
            # Store the instance
            self.instances[instance_id] = {
                "type": class_name,
                "data": data
            }
            return True
        return False
    
    def get_instance(self, instance_id: str) -> Dict[str, Any]:
        """Get an instance by ID"""
        return self.instances.get(instance_id, {}).get("data", {})
    
    def get_instances_of_type(self, class_name: str) -> List[Dict[str, Any]]:
        """Get all instances of a specific class"""
        result = []
        for instance_id, instance in self.instances.items():
            if instance["type"] == class_name:
                result.append(instance["data"])
        return result


# Create the fitness ontology
fitness_ontology = FitnessOntology()

def convert_fitness_data_to_ontology(data: Dict[str, Any]) -> Dict[str, str]:
    """Convert raw fitness data to ontology instances"""
    instance_ids = {}
    user_id = data.get("user_id", "default_user")
    timestamp = data.get("timestamp", datetime.now().isoformat())
    
    # Add User instance if not exists
    user_instance_id = f"user_{user_id}"
    if user_instance_id not in fitness_ontology.instances:
        fitness_ontology.add_instance("User", user_instance_id, {
            "user_id": user_id,
            "age": 30,  # Default values
            "gender": "unknown"
        })
        instance_ids["user"] = user_instance_id
    
    # Add heart rate metrics
    heart_rates = data.get("heart_rate", [])
    for i, hr in enumerate(heart_rates):
        hr_id = f"hr_{user_id}_{int(datetime.now().timestamp())}_{i}"
        fitness_ontology.add_instance("HeartRate", hr_id, {
            "timestamp": timestamp,
            "user_id": user_id,
            "value": hr,
            "resting": False  # Assume not resting heart rate
        })
        if "heart_rate" not in instance_ids:
            instance_ids["heart_rate"] = []
        instance_ids["heart_rate"].append(hr_id)
    
    # Add steps metrics
    steps = data.get("steps", 0)
    steps_id = f"steps_{user_id}_{int(datetime.now().timestamp())}"
    fitness_ontology.add_instance("Steps", steps_id, {
        "timestamp": timestamp,
        "user_id": user_id,
        "count": steps,
        "goal": 10000  # Default goal
    })
    instance_ids["steps"] = steps_id
    
    # Add sleep metrics
    sleep = data.get("sleep_hours", 0)
    sleep_id = f"sleep_{user_id}_{int(datetime.now().timestamp())}"
    fitness_ontology.add_instance("Sleep", sleep_id, {
        "timestamp": timestamp,
        "user_id": user_id,
        "hours": sleep,
        "quality": "unknown"  # Default quality
    })
    instance_ids["sleep"] = sleep_id
    
    # Add calories metrics
    calories = data.get("calories", 0)
    calories_id = f"calories_{user_id}_{int(datetime.now().timestamp())}"
    fitness_ontology.add_instance("Calories", calories_id, {
        "timestamp": timestamp,
        "user_id": user_id,
        "burned": calories,
        "goal": 2000  # Default goal
    })
    instance_ids["calories"] = calories_id
    
    return instance_ids


def create_fitness_report_in_ontology(report: Dict[str, Any]) -> str:
    """Create a fitness report instance in the ontology"""
    report_id = report.get("report_id", f"FR-{int(datetime.now().timestamp())}")
    
    # Add the report instance
    fitness_ontology.add_instance("FitnessReport", report_id, {
        "report_id": report_id,
        "timestamp": report.get("timestamp", datetime.now().isoformat()),
        "user_id": report.get("user_id", "default_user"),
        "fitness_level": report.get("fitness_level", "Unknown")
    })
    
    # Add recommendations
    for i, rec_text in enumerate(report.get("recommendations", [])):
        rec_id = f"rec_{report_id}_{i}"
        fitness_ontology.add_instance("Recommendation", rec_id, {
            "text": rec_text,
            "priority": 0.5  # Default priority
        })
    
    return report_id 