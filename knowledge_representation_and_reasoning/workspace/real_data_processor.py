#!/usr/bin/env python3
"""
Real Data Processor for NYC Jobs and Resume Datasets
Handles CSV parsing issues and extracts clean data for ontology generation
"""

import pandas as pd
import numpy as np
import re
import json
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')

class RealDataProcessor:
    def __init__(self):
        self.resume_data = None
        self.job_data = None
        self.cleaned_resumes = []
        self.cleaned_jobs = []
        
    def load_and_clean_resume_data(self, file_path='UpdatedResumeDataSet.csv'):
        """Load and clean the resume dataset, handling multi-line CSV issues"""
        
        print("📄 Loading Resume Dataset...")
        print("=" * 40)
        
        # Read the file with proper handling for embedded newlines
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Split into lines and process
            lines = content.split('\n')
            
            resume_records = []
            current_category = None
            current_resume = []
            
            for line in lines[1:]:  # Skip header
                if not line.strip():
                    continue
                    
                # Check if this line starts with a job category (not a continuation)
                if self._is_category_line(line):
                    # Save previous record if exists
                    if current_category and current_resume:
                        resume_text = ' '.join(current_resume).strip()
                        if len(resume_text) > 50:  # Filter out very short entries
                            resume_records.append({
                                'Category': current_category,
                                'Resume': resume_text
                            })
                    
                    # Start new record
                    parts = line.split(',', 1)
                    if len(parts) >= 2:
                        current_category = parts[0].strip()
                        current_resume = [parts[1]]
                    else:
                        current_category = line.strip()
                        current_resume = []
                else:
                    # This is a continuation line
                    if current_resume is not None:
                        current_resume.append(line)
            
            # Save last record
            if current_category and current_resume:
                resume_text = ' '.join(current_resume).strip()
                if len(resume_text) > 50:
                    resume_records.append({
                        'Category': current_category,
                        'Resume': resume_text
                    })
            
            self.resume_data = pd.DataFrame(resume_records)
            
            # Clean categories
            self.resume_data = self._clean_resume_categories()
            
            print(f"✅ Loaded {len(self.resume_data)} resume records")
            print(f"📊 Categories found: {self.resume_data['Category'].nunique()}")
            
            # Show category distribution
            category_counts = self.resume_data['Category'].value_counts().head(10)
            print(f"\n🔝 Top categories:")
            for cat, count in category_counts.items():
                print(f"   {cat}: {count} resumes")
            
            return self.resume_data
            
        except Exception as e:
            print(f"❌ Error loading resume data: {e}")
            return None
    
    def _is_category_line(self, line):
        """Determine if a line represents a new category or continuation"""
        
        # Known job categories
        job_categories = [
            'Data Science', 'Java Developer', 'Python Developer', 'HR', 'Sales',
            'Mechanical Engineer', 'Testing', 'Web Designer', 'DevOps Engineer',
            'ETL Developer', 'Business Analyst', 'Network Security Engineer',
            'Blockchain', 'DotNet Developer', 'Automation Testing', 'SAP Developer',
            'Civil Engineer', 'Electrical Engineer', 'Advocate', 'Operations Manager'
        ]
        
        # Check if line starts with known category
        line_start = line.split(',')[0].strip()
        
        # Direct match
        if line_start in job_categories:
            return True
            
        # Partial match for variations
        for cat in job_categories:
            if line_start.startswith(cat) or cat in line_start:
                return True
        
        # Check for common patterns
        category_patterns = [
            r'^[A-Za-z\s]+Developer$',
            r'^[A-Za-z\s]+Engineer$',
            r'^[A-Za-z\s]+Manager$',
            r'^[A-Za-z\s]+Analyst$',
            r'^Data Science',
            r'^Web Design',
            r'^Software',
            r'^System',
        ]
        
        for pattern in category_patterns:
            if re.match(pattern, line_start):
                return True
        
        # If line doesn't start with lowercase/continuation patterns
        if not line_start[0].islower() and not line_start.startswith(('â', 'o ', '•', '*')):
            return True
            
        return False
    
    def _clean_resume_categories(self):
        """Clean and standardize resume categories"""
        
        print("\n🧹 Cleaning resume categories...")
        
        # Category mapping for standardization
        category_mapping = {
            'Data Science': 'Data Science',
            'Data Science Assurance Associate': 'Data Science',
            'Data Science Consultant': 'Data Science',
            'Data Science internship': 'Data Science',
            'Java Developer': 'Java Developer',
            'Java developer': 'Java Developer',
            'Python Developer': 'Python Developer',
            'Python Developer ': 'Python Developer',
            'Web Designer': 'Web Designer',
            'Web Designer ': 'Web Designer',
            'DevOps Engineer': 'DevOps Engineer',
            'Devops Engineer': 'DevOps Engineer',
            'ETL Developer': 'ETL Developer',
            'ETL Developer ': 'ETL Developer',
            'Business Analyst': 'Business Analyst',
            'Business Analyst ': 'Business Analyst',
            'Testing Engineer': 'Testing',
            'Testing': 'Testing',
            'Mechanical Engineer': 'Mechanical Engineer',
            'Electrical Engineer': 'Electrical Engineer',
            'Civil Engineer': 'Civil Engineer',
            'Network Security Engineer': 'Network Security Engineer',
            'HR': 'HR',
            'HR ': 'HR',
            'Sales': 'Sales',
            'Sales Manager': 'Sales',
            'Sales manager': 'Sales',
            'Operations Manager': 'Operations Manager',
            'Operations Manager ': 'Operations Manager',
            'DotNet Developer': 'DotNet Developer',
            'SAP Developer': 'SAP Developer',
            'Blockchain': 'Blockchain',
            'Blockchain Engineer': 'Blockchain',
            'Blockchain Developer': 'Blockchain',
            'Advocate': 'Advocate',
            'Hadoop': 'Big Data',
            'Hadoop Developer': 'Big Data',
            'Team Lead': 'Team Lead',
            'PMO': 'Project Management'
        }
        
        # Apply mapping
        self.resume_data['Category'] = self.resume_data['Category'].map(
            lambda x: category_mapping.get(x, x)
        )
        
        # Filter to keep only substantial categories
        category_counts = self.resume_data['Category'].value_counts()
        substantial_categories = category_counts[category_counts >= 5].index
        
        filtered_data = self.resume_data[
            self.resume_data['Category'].isin(substantial_categories)
        ].copy()
        
        print(f"   Filtered to {len(substantial_categories)} substantial categories")
        print(f"   Kept {len(filtered_data)} resume records")
        
        return filtered_data
    
    def load_and_clean_job_data(self, file_path='nyc-jobs.csv'):
        """Load and clean NYC jobs dataset"""
        
        print("\n💼 Loading NYC Jobs Dataset...")
        print("=" * 35)
        
        try:
            # Load the CSV
            self.job_data = pd.read_csv(file_path, low_memory=False)
            
            print(f"✅ Loaded {len(self.job_data)} job records")
            print(f"📊 Columns: {len(self.job_data.columns)}")
            
            # Show basic info
            print(f"\n📋 Dataset Info:")
            print(f"   Agencies: {self.job_data['Agency'].nunique()}")
            print(f"   Job Categories: {self.job_data['Job Category'].nunique()}")
            print(f"   Posting Types: {self.job_data['Posting Type'].value_counts().to_dict()}")
            
            # Show top agencies
            print(f"\n🏢 Top Agencies:")
            for agency, count in self.job_data['Agency'].value_counts().head(5).items():
                print(f"   {agency}: {count} jobs")
            
            # Show top job categories
            print(f"\n💼 Top Job Categories:")
            job_cats = self.job_data['Job Category'].value_counts().head(8)
            for cat, count in job_cats.items():
                if pd.notna(cat):
                    print(f"   {cat}: {count} jobs")
            
            return self.job_data
            
        except Exception as e:
            print(f"❌ Error loading job data: {e}")
            return None
    
    def extract_skills_from_resumes(self):
        """Extract skills from resume text using pattern matching"""
        
        print("\n🧠 Extracting Skills from Resumes...")
        print("=" * 40)
        
        # Comprehensive skill patterns
        skill_patterns = {
            'Programming Languages': [
                r'\b(?:Python|Java|JavaScript|C\+\+|C#|Ruby|PHP|Go|Rust|Swift|Kotlin)\b',
                r'\b(?:HTML|CSS|SQL|R|MATLAB|Scala|Perl|Shell)\b'
            ],
            'Frameworks & Libraries': [
                r'\b(?:React|Angular|Vue|Django|Flask|Spring|Node\.js|Express)\b',
                r'\b(?:TensorFlow|PyTorch|scikit-learn|pandas|numpy|matplotlib)\b',
                r'\b(?:Bootstrap|jQuery|Laravel|Rails|ASP\.NET)\b'
            ],
            'Databases': [
                r'\b(?:MySQL|PostgreSQL|MongoDB|Oracle|SQL Server|SQLServer)\b',
                r'\b(?:Redis|Cassandra|HBase|ElasticSearch|DynamoDB)\b'
            ],
            'Tools & Technologies': [
                r'\b(?:Docker|Kubernetes|Git|Jenkins|AWS|Azure|GCP)\b',
                r'\b(?:Tableau|Power BI|Excel|Spark|Hadoop|Kafka)\b',
                r'\b(?:Linux|Unix|Windows|MacOS|Ubuntu)\b'
            ],
            'Methodologies': [
                r'\b(?:Agile|Scrum|DevOps|CI/CD|Machine Learning|Data Science)\b',
                r'\b(?:Project Management|Quality Assurance|Testing|ETL)\b'
            ]
        }
        
        extracted_skills = defaultdict(Counter)
        all_skills = Counter()
        
        for _, resume in self.resume_data.iterrows():
            resume_text = resume['Resume'].lower()
            category = resume['Category']
            
            for skill_type, patterns in skill_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, resume_text, re.IGNORECASE)
                    for match in matches:
                        clean_skill = match.strip().title()
                        extracted_skills[skill_type][clean_skill] += 1
                        all_skills[clean_skill] += 1
        
        print(f"📊 Skills Extraction Results:")
        for skill_type, skills in extracted_skills.items():
            print(f"\n   {skill_type} ({len(skills)} unique):")
            for skill, count in skills.most_common(5):
                print(f"     {skill}: {count} occurrences")
        
        return dict(extracted_skills), all_skills
    
    def analyze_job_requirements(self):
        """Analyze job requirements and descriptions"""
        
        print("\n🔍 Analyzing Job Requirements...")
        print("=" * 35)
        
        # Combine job description and requirements text
        job_texts = []
        for _, job in self.job_data.iterrows():
            text_parts = []
            
            for col in ['Job Description', 'Minimum Qual Requirements', 'Preferred Skills']:
                if pd.notna(job[col]):
                    text_parts.append(str(job[col]))
            
            if text_parts:
                job_texts.append(' '.join(text_parts))
        
        print(f"📝 Processed {len(job_texts)} job descriptions")
        
        # Extract requirements patterns
        requirement_patterns = [
            r'(?:bachelor|master|phd|degree|diploma)\s+(?:in\s+)?\w+',
            r'\d+\s*(?:year|month)s?\s+(?:of\s+)?(?:experience|exp)',
            r'(?:proficient|skilled|experience|knowledge)\s+(?:in\s+|with\s+)\w+',
            r'(?:microsoft|oracle|google|aws|azure)\s+\w+',
            r'(?:project|program|budget|team)\s+(?:management|coordination)',
        ]
        
        extracted_requirements = Counter()
        for text in job_texts:
            text_lower = text.lower()
            for pattern in requirement_patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    clean_req = re.sub(r'\s+', ' ', match.strip())
                    if len(clean_req) > 5:
                        extracted_requirements[clean_req] += 1
        
        print(f"🎯 Top Job Requirements:")
        for req, count in extracted_requirements.most_common(10):
            print(f"   {req}: {count} occurrences")
        
        return extracted_requirements, job_texts
    
    def generate_processing_summary(self):
        """Generate comprehensive summary of data processing"""
        
        print("\n📋 Data Processing Summary")
        print("=" * 50)
        
        # Extract skills and requirements
        skills_data, all_skills = self.extract_skills_from_resumes()
        requirements_data, job_texts = self.analyze_job_requirements()
        
        summary = {
            'resume_data': {
                'total_records': len(self.resume_data),
                'categories': self.resume_data['Category'].nunique(),
                'category_distribution': self.resume_data['Category'].value_counts().to_dict(),
                'avg_resume_length': self.resume_data['Resume'].str.len().mean(),
                'total_skills_extracted': len(all_skills),
                'top_skills': dict(all_skills.most_common(20))
            },
            'job_data': {
                'total_records': len(self.job_data),
                'agencies': self.job_data['Agency'].nunique(),
                'job_categories': self.job_data['Job Category'].nunique(),
                'posting_types': self.job_data['Posting Type'].value_counts().to_dict(),
                'salary_ranges': {
                    'min_salary': self.job_data['Salary Range From'].min(),
                    'max_salary': self.job_data['Salary Range To'].max(),
                    'avg_min_salary': self.job_data['Salary Range From'].mean()
                },
                'total_requirements_extracted': len(requirements_data),
                'top_requirements': dict(requirements_data.most_common(15))
            },
            'text_analysis': {
                'resume_text_columns': ['Resume'],
                'job_text_columns': ['Job Description', 'Minimum Qual Requirements', 'Preferred Skills'],
                'total_resume_text_length': self.resume_data['Resume'].str.len().sum(),
                'total_job_text_entries': len(job_texts),
                'avg_job_description_length': np.mean([len(text) for text in job_texts])
            },
            'skills_by_category': {
                category: dict(skills_data[category].most_common(5))
                for category in skills_data.keys()
            }
        }
        
        print(f"✅ Resume Records: {summary['resume_data']['total_records']:,}")
        print(f"✅ Job Records: {summary['job_data']['total_records']:,}")
        print(f"✅ Skills Extracted: {summary['resume_data']['total_skills_extracted']:,}")
        print(f"✅ Requirements Extracted: {summary['job_data']['total_requirements_extracted']:,}")
        print(f"✅ Resume Categories: {summary['resume_data']['categories']}")
        print(f"✅ Job Agencies: {summary['job_data']['agencies']}")
        
        return summary
    
    def save_processed_data(self):
        """Save cleaned data for use in ontology generation"""
        
        print("\n💾 Saving Processed Data...")
        print("=" * 30)
        
        try:
            # Save cleaned resume data
            self.resume_data.to_csv('cleaned_resume_data.csv', index=False)
            print("✅ Saved: cleaned_resume_data.csv")
            
            # Save cleaned job data
            self.job_data.to_csv('cleaned_job_data.csv', index=False)
            print("✅ Saved: cleaned_job_data.csv")
            
            # Generate and save summary
            summary = self.generate_processing_summary()
            
            with open('real_data_processing_summary.json', 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            print("✅ Saved: real_data_processing_summary.json")
            
            return summary
            
        except Exception as e:
            print(f"❌ Error saving processed data: {e}")
            return None

def main():
    """Main function to process both datasets"""
    
    print("🚀 Real Data Processing Pipeline")
    print("=" * 60)
    
    processor = RealDataProcessor()
    
    # Process resume data
    resume_data = processor.load_and_clean_resume_data()
    
    if resume_data is not None:
        # Process job data
        job_data = processor.load_and_clean_job_data()
        
        if job_data is not None:
            # Save processed data and generate summary
            summary = processor.save_processed_data()
            
            if summary:
                print(f"\n🎯 Processing Complete!")
                print(f"   Ready for ontology generation with real data")
                return True
    
    print(f"\n❌ Processing Failed!")
    return False

if __name__ == "__main__":
    main()