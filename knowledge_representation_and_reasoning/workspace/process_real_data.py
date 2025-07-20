#!/usr/bin/env python3
"""
Process Real Resume Dataset

This script adapts the ontology demo to work with your actual resume dataset structure:
- ID, Resume_str, Resume_html, Category, Cleaned_Resume

Usage: python process_real_data.py --resume your_resume_file.csv
"""

import pandas as pd
import os
import sys
import argparse
from ontology_demo_complete import (
    Config, DataAnalyzer, OntologyGenerator, 
    MermaidGenerator, OntologyTester
)

def analyze_resume_dataset(resume_file: str):
    """Analyze the structure of your resume dataset"""
    
    print("🔍 Analyzing Real Resume Dataset")
    print("=" * 40)
    
    # Load and inspect the dataset
    df = pd.read_csv(resume_file)
    
    print(f"📊 Dataset Info:")
    print(f"   Records: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Data types: {df.dtypes.to_dict()}")
    
    # Check for missing values
    print(f"\n🔍 Missing Values:")
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            print(f"   {col}: {count} missing ({count/len(df)*100:.1f}%)")
    
    # Analyze categories
    print(f"\n📋 Job Categories:")
    categories = df['Category'].value_counts()
    for cat, count in categories.head(10).items():
        print(f"   {cat}: {count} resumes")
    
    # Sample resume content
    print(f"\n📝 Sample Resume Content:")
    sample_resume = df['Cleaned_Resume'].dropna().iloc[0]
    print(f"   Length: {len(sample_resume)} characters")
    print(f"   Preview: {sample_resume[:200]}...")
    
    return df

def extract_skills_from_resumes(df: pd.DataFrame, max_samples: int = 1000):
    """Extract skills and concepts from resume text"""
    
    print(f"\n🔧 Extracting Skills from {min(len(df), max_samples)} resumes...")
    
    # Use cleaned resume text
    resume_texts = df['Cleaned_Resume'].dropna().head(max_samples)
    
    # Common technical skills to look for
    technical_skills = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes',
        'machine learning', 'deep learning', 'ai', 'nlp',
        'tensorflow', 'pytorch', 'scikit-learn',
        'html', 'css', 'nodejs', 'express', 'spring',
        'git', 'jenkins', 'ci/cd', 'devops',
        'tableau', 'powerbi', 'excel', 'r', 'matlab'
    ]
    
    # Extract skills
    skill_counts = {}
    category_skills = {}
    
    for idx, text in enumerate(resume_texts):
        text_lower = str(text).lower()
        category = df.iloc[idx]['Category']
        
        if category not in category_skills:
            category_skills[category] = {}
        
        for skill in technical_skills:
            if skill in text_lower:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
                category_skills[category][skill] = category_skills[category].get(skill, 0) + 1
    
    # Top skills overall
    print(f"\n🏆 Top Skills Found:")
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
    for skill, count in sorted_skills[:15]:
        print(f"   {skill}: {count} resumes ({count/len(resume_texts)*100:.1f}%)")
    
    # Skills by category
    print(f"\n📊 Skills by Category (top 3 categories):")
    for category in list(df['Category'].value_counts().head(3).index):
        if category in category_skills:
            print(f"\n   {category}:")
            cat_skills = sorted(category_skills[category].items(), key=lambda x: x[1], reverse=True)
            for skill, count in cat_skills[:5]:
                print(f"     {skill}: {count}")
    
    return skill_counts, category_skills

def generate_ontology_from_real_data(resume_file: str, max_samples: int = 1000):
    """Generate ontology from real resume dataset"""
    
    print(f"\n🔧 Generating Ontology from Real Data")
    print("=" * 40)
    
    # Load dataset
    df = pd.read_csv(resume_file)
    
    # Extract information
    skill_counts, category_skills = extract_skills_from_resumes(df, max_samples)
    
    # Create entities based on real data
    entities = {}
    
    # Person entity (from resume structure)
    entities['Person'] = {
        'properties': ['id', 'resume_text', 'category', 'cleaned_resume'],
        'instances': len(df),
        'source': 'resume_dataset'
    }
    
    # Skill entity (from extracted skills)
    top_skills = [skill for skill, count in sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20]]
    entities['Skill'] = {
        'properties': ['skill_name', 'frequency', 'category_relevance'],
        'instances': top_skills,
        'source': 'skill_extraction'
    }
    
    # Category entity (from job categories)
    categories = df['Category'].unique().tolist()
    entities['JobCategory'] = {
        'properties': ['category_name', 'resume_count'],
        'instances': categories,
        'source': 'resume_categories'
    }
    
    # Experience entity (inferred from resume content)
    entities['Experience'] = {
        'properties': ['experience_level', 'domain', 'years'],
        'instances': 'varied',
        'source': 'resume_content'
    }
    
    # Define relationships
    relationships = [
        ('Person', 'hasSkill', 'Skill'),
        ('Person', 'belongsToCategory', 'JobCategory'),
        ('Person', 'hasExperience', 'Experience'),
        ('JobCategory', 'requiresSkill', 'Skill'),
        ('Experience', 'involvesSkill', 'Skill')
    ]
    
    return entities, relationships, skill_counts, category_skills

def create_mermaid_from_real_data(entities, relationships):
    """Create Mermaid diagram from real data analysis"""
    
    lines = ["classDiagram"]
    
    # Add classes
    for entity_name, entity_data in entities.items():
        lines.append(f"    class {entity_name} {{")
        
        properties = entity_data.get('properties', [])
        for prop in properties:
            lines.append(f"        +string {prop}")
        
        # Add instance info as comment
        instances = entity_data.get('instances', 'unknown')
        if isinstance(instances, list):
            lines.append(f"        +note {len(instances)} instances")
        elif isinstance(instances, int):
            lines.append(f"        +note {instances} records")
        
        lines.append("    }")
        lines.append("")
    
    # Add relationships
    for source, relation, target in relationships:
        if source in entities and target in entities:
            lines.append(f"    {source} ||--o{{ {target} : {relation}")
    
    return "\n".join(lines)

def generate_real_data_report(resume_file: str, entities, relationships, skill_counts, category_skills):
    """Generate comprehensive report for real dataset"""
    
    df = pd.read_csv(resume_file)
    
    report_lines = [
        "# Real Resume Dataset Ontology Analysis",
        "",
        f"## Dataset Overview",
        f"- **Total Records**: {len(df)}",
        f"- **Columns**: {', '.join(df.columns)}",
        f"- **Job Categories**: {len(df['Category'].unique())}",
        "",
        "## Generated Ontology",
        "",
        "### Entities:",
        ""
    ]
    
    for entity_name, entity_data in entities.items():
        instances = entity_data.get('instances', 'unknown')
        if isinstance(instances, list):
            instance_count = len(instances)
        elif isinstance(instances, int):
            instance_count = instances
        else:
            instance_count = 'varied'
        
        report_lines.append(f"- **{entity_name}**: {instance_count} instances")
        report_lines.append(f"  - Properties: {', '.join(entity_data.get('properties', []))}")
        report_lines.append(f"  - Source: {entity_data.get('source', 'unknown')}")
        report_lines.append("")
    
    report_lines.extend([
        "### Relationships:",
        ""
    ])
    
    for source, relation, target in relationships:
        report_lines.append(f"- {source} --{relation}--> {target}")
    
    report_lines.extend([
        "",
        "## Top Skills Analysis",
        ""
    ])
    
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)
    for skill, count in sorted_skills[:20]:
        percentage = (count / len(df)) * 100
        report_lines.append(f"- **{skill}**: {count} resumes ({percentage:.1f}%)")
    
    report_lines.extend([
        "",
        "## Category Distribution",
        ""
    ])
    
    for category, count in df['Category'].value_counts().items():
        percentage = (count / len(df)) * 100
        report_lines.append(f"- **{category}**: {count} resumes ({percentage:.1f}%)")
    
    report_content = "\n".join(report_lines)
    
    # Save report
    with open("real_data_analysis.md", "w") as f:
        f.write(report_content)
    
    return report_content

def main():
    parser = argparse.ArgumentParser(description="Process Real Resume Dataset")
    parser.add_argument("--resume", required=True, help="Path to resume CSV file")
    parser.add_argument("--max-samples", type=int, default=1000, help="Maximum samples to process")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.resume):
        print(f"❌ Resume file not found: {args.resume}")
        sys.exit(1)
    
    print("🚀 Processing Real Resume Dataset")
    print("=" * 50)
    
    # Step 1: Analyze dataset
    df = analyze_resume_dataset(args.resume)
    
    # Step 2: Generate ontology
    entities, relationships, skill_counts, category_skills = generate_ontology_from_real_data(
        args.resume, args.max_samples
    )
    
    # Step 3: Create Mermaid diagram
    mermaid_code = create_mermaid_from_real_data(entities, relationships)
    
    # Step 4: Save outputs
    with open("real_data_ontology.mmd", "w") as f:
        f.write(mermaid_code)
    
    # Step 5: Generate report
    report = generate_real_data_report(args.resume, entities, relationships, skill_counts, category_skills)
    
    # Summary
    print(f"\n🎯 Analysis Complete!")
    print("=" * 30)
    print(f"📁 Files generated:")
    print(f"   📊 real_data_analysis.md - Comprehensive analysis report")
    print(f"   🎨 real_data_ontology.mmd - Mermaid diagram")
    print(f"")
    print(f"🔧 Generated Ontology:")
    print(f"   Entities: {len(entities)}")
    print(f"   Relationships: {len(relationships)}")
    print(f"   Skills identified: {len(skill_counts)}")
    print(f"   Categories: {len(df['Category'].unique())}")
    print(f"")
    print(f"🎨 Mermaid Diagram Preview:")
    print("-" * 30)
    print(mermaid_code)
    print("-" * 30)
    print(f"")
    print(f"🚀 Next Steps:")
    print(f"1. Copy the Mermaid code to https://mermaid.live/")
    print(f"2. Export as PNG/SVG for your assignment")
    print(f"3. Review 'real_data_analysis.md' for detailed insights")

if __name__ == "__main__":
    main()