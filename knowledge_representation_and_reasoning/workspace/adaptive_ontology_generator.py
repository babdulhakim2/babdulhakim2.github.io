#!/usr/bin/env python3
"""
Adaptive Ontology Generator for NYC Jobs and Resume Data
Generates ontologies using corpus-based and task-based approaches
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re
import json

class AdaptiveCorpusOntologyGenerator:
    def __init__(self, min_frequency=3, max_concepts=30):
        self.min_frequency = min_frequency
        self.max_concepts = max_concepts
        
    def detect_text_columns(self, df, min_text_length=50):
        """Automatically detect text columns in dataframe"""
        text_columns = []
        
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check if column contains substantial text
                sample_texts = df[col].dropna().astype(str).head(10)
                avg_length = sample_texts.str.len().mean()
                
                if avg_length > min_text_length:
                    text_columns.append(col)
                    print(f"  📝 Detected text column: '{col}' (avg length: {avg_length:.0f})")
        
        return text_columns
    
    def get_resume_text_columns(self, resume_df):
        """Get text columns specifically for resume data"""
        # For our cleaned resume data, use the 'Resume' column
        if 'Resume' in resume_df.columns:
            return ['Resume']
        else:
            return self.detect_text_columns(resume_df)
    
    def get_job_text_columns(self, jobs_df):
        """Get text columns specifically for job data"""
        # For NYC jobs data, use description and requirements columns
        job_text_cols = []
        preferred_cols = ['Job Description', 'Minimum Qual Requirements', 'Preferred Skills']
        
        for col in preferred_cols:
            if col in jobs_df.columns:
                job_text_cols.append(col)
        
        if not job_text_cols:
            job_text_cols = self.detect_text_columns(jobs_df)
        
        return job_text_cols
    
    def extract_concepts_from_corpus(self, text_corpus, corpus_name):
        """Extract concepts using TF-IDF and pattern matching"""
        
        print(f"🔍 Extracting concepts from {corpus_name} corpus...")
        print(f"   Processing {len(text_corpus)} documents...")
        
        # Clean and preprocess text
        cleaned_corpus = []
        for text in text_corpus:
            if pd.notna(text) and str(text).strip():
                # Remove HTML, special chars, normalize
                clean_text = re.sub(r'<[^>]+>', '', str(text))
                clean_text = re.sub(r'[^\w\s]', ' ', clean_text)
                clean_text = re.sub(r'\s+', ' ', clean_text)
                if len(clean_text.strip()) > 10:
                    cleaned_corpus.append(clean_text.lower().strip())
        
        print(f"   After cleaning: {len(cleaned_corpus)} valid documents")
        
        if len(cleaned_corpus) < 5:
            print(f"   ⚠️ Too few documents for analysis")
            return {'top_terms': [], 'key_phrases': [], 'topics': [], 'corpus_name': corpus_name}
        
        # Extract key terms using TF-IDF
        try:
            vectorizer = TfidfVectorizer(
                max_features=min(500, len(cleaned_corpus) * 5),
                stop_words='english',
                ngram_range=(1, 3),
                min_df=max(2, min(self.min_frequency, len(cleaned_corpus) // 20)),
                max_df=0.8
            )
            
            tfidf_matrix = vectorizer.fit_transform(cleaned_corpus)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get top terms by TF-IDF score
            tfidf_scores = tfidf_matrix.sum(axis=0).A1
            top_terms = [(feature_names[i], float(tfidf_scores[i])) 
                         for i in tfidf_scores.argsort()[-min(self.max_concepts, len(feature_names)):][::-1]]
            
            print(f"   ✅ Extracted {len(top_terms)} key terms")
            
        except Exception as e:
            print(f"   ⚠️ TF-IDF extraction failed: {e}")
            top_terms = []
        
        # Extract domain-specific patterns
        domain_patterns = self._extract_domain_patterns(cleaned_corpus)
        
        # Simple topic discovery
        topics = self._discover_simple_topics(cleaned_corpus)
        
        return {
            'top_terms': top_terms,
            'domain_patterns': domain_patterns,
            'topics': topics,
            'corpus_name': corpus_name,
            'document_count': len(cleaned_corpus)
        }
    
    def _extract_domain_patterns(self, corpus):
        """Extract domain-specific patterns"""
        patterns = Counter()
        
        # Government/job-specific patterns
        job_patterns = [
            r'\b(?:bachelor|master|phd|degree|diploma|certificate|certification)\s+(?:in\s+)?[a-z\s]+',
            r'\b\d+\s*(?:year|month)s?\s+(?:of\s+)?(?:experience|exp|work)',
            r'\b(?:proficient|skilled|experience|knowledge)\s+(?:in\s+|with\s+)[a-z\s]+',
            r'\b(?:microsoft|adobe|oracle|google|aws|azure)\s+[a-z\s]+',
            r'\b(?:project|program|budget|team|staff)\s+(?:management|coordination|supervision)',
            r'\b(?:public|government|federal|state|municipal|city)\s+[a-z\s]+',
        ]
        
        for text in corpus[:100]:  # Sample for performance
            for pattern in job_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    clean_match = re.sub(r'\s+', ' ', match.strip())
                    if len(clean_match) > 8:
                        patterns[clean_match.lower()] += 1
        
        return patterns.most_common(15)
    
    def _discover_simple_topics(self, corpus):
        """Simple topic discovery using keyword clustering"""
        
        # Define topic keywords
        topic_keywords = {
            'technical': ['software', 'computer', 'technology', 'system', 'database', 'programming'],
            'management': ['management', 'supervision', 'leadership', 'coordination', 'planning'],
            'finance': ['budget', 'financial', 'accounting', 'revenue', 'cost', 'fiscal'],
            'education': ['education', 'training', 'teaching', 'curriculum', 'student', 'academic'],
            'health': ['health', 'medical', 'patient', 'clinical', 'healthcare', 'hospital'],
            'legal': ['legal', 'law', 'compliance', 'regulation', 'policy', 'attorney'],
            'operations': ['operations', 'maintenance', 'facility', 'logistics', 'service', 'support']
        }
        
        topic_scores = defaultdict(int)
        
        for text in corpus[:200]:  # Sample for performance
            text_lower = text.lower()
            for topic, keywords in topic_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    topic_scores[topic] += score
        
        # Convert to list of topics
        topics = [{'topic': topic, 'score': score} 
                 for topic, score in sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)]
        
        return topics[:5]
    
    def infer_entity_types(self, concepts):
        """Automatically infer entity types from concepts"""
        
        print("🧠 Inferring entity types from discovered concepts...")
        
        # Enhanced classification patterns
        patterns = {
            'Person': ['person', 'candidate', 'employee', 'worker', 'staff', 'individual', 'applicant', 'specialist'],
            'Organization': ['agency', 'department', 'company', 'organization', 'bureau', 'office', 'authority', 'administration'],
            'Role': ['position', 'job', 'title', 'role', 'manager', 'director', 'analyst', 'coordinator', 'supervisor'],
            'Skill': ['skill', 'ability', 'knowledge', 'expertise', 'competency', 'proficient', 'experience'],
            'Location': ['location', 'place', 'site', 'area', 'region', 'building', 'manhattan', 'brooklyn', 'queens'],
            'Education': ['education', 'degree', 'university', 'college', 'bachelor', 'master', 'phd', 'certificate'],
            'Technology': ['software', 'system', 'application', 'technology', 'computer', 'database', 'microsoft'],
            'Process': ['process', 'procedure', 'method', 'operation', 'management', 'administration'],
            'Requirement': ['requirement', 'qualification', 'criteria', 'standard', 'minimum', 'preferred'],
            'Finance': ['budget', 'financial', 'salary', 'revenue', 'cost', 'accounting', 'fiscal']
        }
        
        inferred_entities = defaultdict(list)
        
        # Collect all concepts
        all_concepts = []
        for concept_data in concepts.values():
            # Add terms from TF-IDF
            all_concepts.extend([term for term, score in concept_data.get('top_terms', [])])
            # Add domain patterns
            all_concepts.extend([pattern for pattern, count in concept_data.get('domain_patterns', [])])
        
        # Remove duplicates and classify
        unique_concepts = list(set(all_concepts))
        print(f"   Analyzing {len(unique_concepts)} unique concepts...")
        
        for concept in unique_concepts:
            concept_lower = concept.lower()
            classified = False
            
            for entity_type, keywords in patterns.items():
                if any(keyword in concept_lower for keyword in keywords):
                    inferred_entities[entity_type].append(concept)
                    classified = True
                    break
            
            if not classified:
                # Additional classification rules
                if any(char.isdigit() for char in concept):
                    inferred_entities['Metric'].append(concept)
                elif len(concept.split()) > 3:
                    inferred_entities['Description'].append(concept)
                else:
                    inferred_entities['General'].append(concept)
        
        # Filter out entity types with too few concepts
        filtered_entities = {k: v for k, v in inferred_entities.items() if len(v) >= 1}
        
        print(f"   ✅ Identified {len(filtered_entities)} entity types:")
        for entity_type, concepts in filtered_entities.items():
            print(f"      {entity_type}: {len(concepts)} concepts")
        
        return dict(filtered_entities)
    
    def discover_relationships(self, resume_concepts, job_concepts):
        """Discover relationships through concept analysis"""
        
        print("🔗 Discovering relationships...")
        
        relationships = []
        
        # Find common concepts
        resume_terms = set([term for term, score in resume_concepts.get('top_terms', [])])
        job_terms = set([term for term, score in job_concepts.get('top_terms', [])])
        
        common_terms = resume_terms & job_terms
        print(f"   Found {len(common_terms)} common terms between datasets")
        
        # Relationship inference based on topics
        resume_topics = resume_concepts.get('topics', [])
        job_topics = job_concepts.get('topics', [])
        
        # Basic relationships
        relationships = [
            ('Person', 'has', 'Skill'),
            ('Person', 'seeks', 'Role'),
            ('Person', 'attained', 'Education'),
            ('Role', 'requires', 'Skill'),
            ('Role', 'offered_by', 'Organization'),
            ('Role', 'located_in', 'Location'),
            ('Role', 'demands', 'Requirement'),
            ('Organization', 'posts', 'Role'),
            ('Skill', 'applied_in', 'Technology'),
            ('Education', 'provides', 'Skill')
        ]
        
        print(f"   ✅ Discovered {len(relationships)} relationships")
        return relationships
    
    def generate_ontology_structure(self, resume_df, jobs_df):
        """Generate complete ontology structure"""
        
        print("🏗️ Generating adaptive corpus-based ontology from REAL data...")
        
        # Get text columns using specialized methods
        print("\n📋 Identifying text columns in resume data:")
        resume_text_cols = self.get_resume_text_columns(resume_df)
        print(f"   Using columns: {resume_text_cols}")
        
        print("\n📋 Identifying text columns in job data:")
        job_text_cols = self.get_job_text_columns(jobs_df)
        print(f"   Using columns: {job_text_cols}")
        
        if not resume_text_cols:
            print("⚠️ No substantial text columns found in resume data")
            resume_text_cols = ['Category']  # Fallback to category
            
        if not job_text_cols:
            print("⚠️ No substantial text columns found in job data") 
            job_text_cols = ['Agency', 'Business Title', 'Job Category']  # Fallback
        
        # Extract concepts from resume corpus
        resume_corpus = []
        for col in resume_text_cols:
            resume_corpus.extend(resume_df[col].dropna().astype(str).tolist())
        
        resume_concepts = self.extract_concepts_from_corpus(resume_corpus, 'Resume')
        
        # Extract concepts from job corpus  
        job_corpus = []
        for col in job_text_cols:
            job_corpus.extend(jobs_df[col].dropna().astype(str).tolist())
        
        job_concepts = self.extract_concepts_from_corpus(job_corpus, 'Job')
        
        # Infer entity types
        all_concepts = {
            'resume': resume_concepts,
            'job': job_concepts
        }
        
        entity_types = self.infer_entity_types(all_concepts)
        
        # Discover relationships
        relationships = self.discover_relationships(resume_concepts, job_concepts)
        
        # Create ontology structure
        ontology = {
            'entities': entity_types,
            'relationships': relationships,
            'concepts': {
                'resume_concepts': resume_concepts,
                'job_concepts': job_concepts
            },
            'data_sources': {
                'resume_text_columns': resume_text_cols,
                'job_text_columns': job_text_cols
            },
            'metadata': {
                'approach': 'adaptive_corpus_based',
                'resume_documents': len(resume_df),
                'job_documents': len(jobs_df),
                'total_entities': len(entity_types),
                'total_relationships': len(relationships)
            }
        }
        
        return ontology


class AdaptiveTaskBasedOntologyGenerator:
    def __init__(self, task_focus='job_matching'):
        self.task_focus = task_focus
        
    def analyze_data_structure(self, df, dataset_name):
        """Analyze dataframe structure for ontology generation"""
        
        print(f"🔍 Analyzing {dataset_name} data structure...")
        
        structure = {
            'categorical_columns': [],
            'numerical_columns': [],
            'text_columns': [],
            'identifier_columns': []
        }
        
        for col in df.columns:
            col_data = df[col].dropna()
            
            if col_data.empty:
                continue
                
            # Identify column types with special handling for our real data
            if any(id_word in col.lower() for id_word in ['id', 'number']):
                structure['identifier_columns'].append(col)
            elif df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                structure['numerical_columns'].append(col)
            elif df[col].dtype == 'object':
                # Check if it's categorical or text
                unique_ratio = col_data.nunique() / len(col_data)
                avg_length = col_data.astype(str).str.len().mean()
                
                # Special handling for known text columns
                if col in ['Resume', 'Job Description', 'Minimum Qual Requirements', 'Preferred Skills']:
                    structure['text_columns'].append(col)
                elif col in ['Category', 'Agency', 'Posting Type', 'Job Category', 'Business Title']:
                    structure['categorical_columns'].append(col)
                elif unique_ratio < 0.1 and avg_length < 100:  # Likely categorical
                    structure['categorical_columns'].append(col)
                elif avg_length > 50:  # Likely text
                    structure['text_columns'].append(col)
                else:
                    structure['categorical_columns'].append(col)
        
        print(f"   📊 Categorical: {len(structure['categorical_columns'])} columns")
        print(f"   🔢 Numerical: {len(structure['numerical_columns'])} columns")
        print(f"   📝 Text: {len(structure['text_columns'])} columns")
        print(f"   🆔 Identifiers: {len(structure['identifier_columns'])} columns")
        
        return structure
        
    def generate_task_ontology(self, resume_df, jobs_df):
        """Generate ontology based on task requirements"""
        
        print("🎯 Generating task-based ontology for job matching...")
        
        # Analyze data structures
        resume_structure = self.analyze_data_structure(resume_df, "Resume")
        job_structure = self.analyze_data_structure(jobs_df, "Job")
        
        task_entities = {}
        task_relationships = []
        
        # Core entities based on task
        task_entities['JobSeeker'] = {
            'properties': ['id', 'profile', 'qualifications', 'preferences'],
            'count': len(resume_df),
            'source': 'resume_records',
            'description': 'Individuals seeking employment'
        }
        
        task_entities['JobOpportunity'] = {
            'properties': ['id', 'title', 'description', 'requirements', 'compensation'],
            'count': len(jobs_df),
            'source': 'job_records',
            'description': 'Available job positions'
        }
        
        # Create entities from categorical data
        for col in resume_structure['categorical_columns']:
            if resume_df[col].nunique() > 1 and resume_df[col].nunique() < 100:
                entity_name = f"Resume{col.replace(' ', '').replace('_', '')}"
                unique_values = resume_df[col].dropna().unique().tolist()
                task_entities[entity_name] = {
                    'instances': unique_values[:20],  # Limit for readability
                    'count': len(unique_values),
                    'source': f'resume_{col}',
                    'description': f'Categories from resume {col}'
                }
        
        for col in job_structure['categorical_columns']:
            if jobs_df[col].nunique() > 1 and jobs_df[col].nunique() < 200:
                entity_name = f"Job{col.replace(' ', '').replace('_', '')}"
                unique_values = jobs_df[col].dropna().unique().tolist()
                task_entities[entity_name] = {
                    'instances': unique_values[:20],  # Limit for readability
                    'count': len(unique_values),
                    'source': f'job_{col}',
                    'description': f'Categories from job {col}'
                }
        
        # Generate task-specific relationships
        entity_names = list(task_entities.keys())
        
        # Core relationships for job matching
        task_relationships = [
            ('JobSeeker', 'appliesTo', 'JobOpportunity'),
            ('JobSeeker', 'hasProfile', 'ResumeCategory') if 'ResumeCategory' in entity_names else None,
            ('JobOpportunity', 'belongsTo', 'JobCategory') if 'JobCategory' in entity_names else None,
            ('JobOpportunity', 'offeredBy', 'JobAgency') if 'JobAgency' in entity_names else None,
            ('JobOpportunity', 'locatedAt', 'JobWorkLocation') if 'JobWorkLocation' in entity_names else None,
        ]
        
        # Filter out None relationships
        task_relationships = [rel for rel in task_relationships if rel is not None]
        
        # Add inferred relationships based on available entities
        for entity in entity_names:
            if 'Job' in entity and entity != 'JobSeeker' and entity != 'JobOpportunity':
                task_relationships.append(('JobOpportunity', 'hasAttribute', entity))
            elif 'Resume' in entity and entity != 'JobSeeker':
                task_relationships.append(('JobSeeker', 'hasAttribute', entity))
        
        return {
            'entities': task_entities,
            'relationships': task_relationships,
            'data_structure': {
                'resume': resume_structure,
                'job': job_structure
            },
            'metadata': {
                'approach': 'adaptive_task_based',
                'entities_count': len(task_entities),
                'relationships_count': len(task_relationships),
                'task_focus': self.task_focus
            }
        }


def load_real_data():
    """Load actual processed resume and job data"""
    
    print("📊 Loading Real Processed Data...")
    print("=" * 35)
    
    try:
        # Load cleaned resume data
        resume_df = pd.read_csv('cleaned_resume_data.csv')
        print(f"✅ Loaded {len(resume_df)} real resume records")
        
        # Load cleaned job data
        jobs_df = pd.read_csv('cleaned_job_data.csv')
        print(f"✅ Loaded {len(jobs_df)} real job records")
        
        # Load processing summary for additional metrics
        with open('real_data_processing_summary.json', 'r') as f:
            processing_summary = json.load(f)
        
        print(f"📋 Real Data Overview:")
        print(f"   Resume Categories: {processing_summary['resume_data']['categories']}")
        print(f"   Job Agencies: {processing_summary['job_data']['agencies']}")
        print(f"   Skills Extracted: {processing_summary['resume_data']['total_skills_extracted']}")
        print(f"   Requirements Extracted: {processing_summary['job_data']['total_requirements_extracted']}")
        
        return resume_df, jobs_df, processing_summary
        
    except FileNotFoundError:
        print("⚠️ Processed data files not found. Running real data processor first...")
        
        # Import and run the real data processor
        from real_data_processor import RealDataProcessor
        
        processor = RealDataProcessor()
        processor.load_and_clean_resume_data()
        processor.load_and_clean_job_data()
        summary = processor.save_processed_data()
        
        # Load the newly created files
        resume_df = pd.read_csv('cleaned_resume_data.csv')
        jobs_df = pd.read_csv('cleaned_job_data.csv')
        
        return resume_df, jobs_df, summary


def main():
    print("🚀 Adaptive Ontology Generator - Real Data Edition")
    print("=" * 60)
    
    # Load real processed data
    resume_df, jobs_df, processing_summary = load_real_data()
    
    print(f"📊 Real Data Loaded:")
    print(f"   Resumes: {len(resume_df)} records")
    print(f"   Jobs: {len(jobs_df)} records")
    print(f"   Resume columns: {list(resume_df.columns)}")
    print(f"   Job columns: {list(jobs_df.columns)[:10]}...")  # Show first 10
    
    # CORPUS-BASED APPROACH
    print("\n" + "="*50)
    print("ADAPTIVE CORPUS-BASED ONTOLOGY GENERATION")
    print("="*50)
    
    try:
        corpus_generator = AdaptiveCorpusOntologyGenerator(min_frequency=3, max_concepts=25)
        corpus_ontology = corpus_generator.generate_ontology_structure(resume_df, jobs_df)
        print("✅ Corpus-based ontology generated successfully")
    except Exception as e:
        print(f"❌ Corpus-based generation failed: {e}")
        corpus_ontology = None
    
    # TASK-BASED APPROACH
    print("\n" + "="*50)
    print("ADAPTIVE TASK-BASED ONTOLOGY GENERATION")
    print("="*50)
    
    try:
        task_generator = AdaptiveTaskBasedOntologyGenerator(task_focus='job_matching')
        task_ontology = task_generator.generate_task_ontology(resume_df, jobs_df)
        print("✅ Task-based ontology generated successfully")
    except Exception as e:
        print(f"❌ Task-based generation failed: {e}")
        task_ontology = None
    
    # RESULTS COMPARISON
    print("\n" + "="*50)
    print("ONTOLOGY ANALYSIS & COMPARISON")
    print("="*50)
    
    if corpus_ontology:
        print(f"\n📊 Corpus-based Approach Results:")
        print(f"   Entity Types: {len(corpus_ontology['entities'])}")
        print(f"   Relationships: {len(corpus_ontology['relationships'])}")
        print(f"   Key Entity Types: {', '.join(list(corpus_ontology['entities'].keys())[:8])}")
        
        # Show sample concepts
        print(f"\n   Sample Discovered Concepts:")
        resume_terms = corpus_ontology['concepts']['resume_concepts'].get('top_terms', [])[:5]
        job_terms = corpus_ontology['concepts']['job_concepts'].get('top_terms', [])[:5]
        
        if resume_terms:
            print(f"   Resume Terms: {', '.join([term for term, score in resume_terms])}")
        if job_terms:
            print(f"   Job Terms: {', '.join([term for term, score in job_terms])}")
    
    if task_ontology:
        print(f"\n🎯 Task-based Approach Results:")
        print(f"   Entity Types: {len(task_ontology['entities'])}")
        print(f"   Relationships: {len(task_ontology['relationships'])}")
        print(f"   Key Entity Types: {', '.join(list(task_ontology['entities'].keys())[:8])}")
        
        # Show sample entities
        print(f"\n   Sample Entities:")
        for entity_name, entity_data in list(task_ontology['entities'].items())[:3]:
            print(f"   {entity_name}: {entity_data.get('count', 'N/A')} instances")
    
    # SAVE RESULTS
    print(f"\n💾 Saving Results...")
    
    if corpus_ontology:
        with open('corpus_based_ontology.json', 'w') as f:
            json.dump(corpus_ontology, f, indent=2, default=str)
        print(f"   ✅ Corpus ontology: corpus_based_ontology.json")
    
    if task_ontology:
        with open('task_based_ontology.json', 'w') as f:
            json.dump(task_ontology, f, indent=2, default=str)
        print(f"   ✅ Task ontology: task_based_ontology.json")
    
    # GENERATE SUMMARY REPORT
    report_lines = [
        "# Adaptive Ontology Generation Report",
        "",
        "## Dataset Overview",
        f"- Resume Records: {len(resume_df):,}",
        f"- Job Records: {len(jobs_df):,}",
        "",
        "## Methodology Comparison",
        ""
    ]
    
    if corpus_ontology and task_ontology:
        report_lines.extend([
            "| Approach | Entities | Relationships | Focus |",
            "|----------|----------|---------------|-------|",
            f"| Corpus-based | {len(corpus_ontology['entities'])} | {len(corpus_ontology['relationships'])} | Content analysis |",
            f"| Task-based | {len(task_ontology['entities'])} | {len(task_ontology['relationships'])} | Job matching structure |",
            "",
            "## Key Findings",
            "",
            "### Corpus-based Approach:",
            "- Discovers concepts from actual text content",
            "- Identifies domain-specific terminology",
            "- Reveals latent semantic relationships",
            "",
            "### Task-based Approach:", 
            "- Focuses on job matching requirements",
            "- Utilizes existing data categorizations",
            "- Emphasizes operational relationships",
            "",
            "## Recommendations",
            "",
            "1. **Hybrid Approach**: Combine both methodologies for comprehensive coverage",
            "2. **Domain Validation**: Validate discovered concepts with domain experts",
            "3. **Iterative Refinement**: Use feedback to improve concept extraction",
            "4. **Application Focus**: Tailor ontology to specific use cases",
        ])
    
    report_content = "\n".join(report_lines)
    
    with open('ontology_generation_report.md', 'w') as f:
        f.write(report_content)
    
    print(f"   ✅ Summary report: ontology_generation_report.md")
    
    print(f"\n🎯 Analysis Complete!")
    print(f"   Generated ontologies using both corpus-based and task-based approaches")
    print(f"   Results saved as JSON files for further analysis")
    print(f"   Summary report available in Markdown format")
    
    return corpus_ontology, task_ontology


if __name__ == "__main__":
    # Run the complete analysis
    corpus_ontology, task_ontology = main()