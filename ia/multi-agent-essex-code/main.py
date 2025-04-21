#!/usr/bin/env python3

"""
This file run the whole code featuring:
- BDI architecture (Beliefs, Desires, Intentions)
- Means-End reasoning and Subsumption architecture 
- Speech act communication
- Ontology-based knowledge representation
"""

import os
import sys

print("Redirecting to advanced fitness multi-agent system with means-end reasoning and subsumption architecture...")

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Run the implementation
exec(open(os.path.join(script_dir, "fitness_mas.py")).read())