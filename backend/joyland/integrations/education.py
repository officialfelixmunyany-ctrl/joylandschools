"""Educational AI services for curriculum and assessment."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Union

logger = logging.getLogger(__name__)

@dataclass
class LearningObjective:
    """A specific learning objective with assessment criteria."""
    description: str
    subject_area: str
    grade_level: str
    assessment_criteria: List[str]
    skills: List[str]
    term: Optional[int] = None

@dataclass
class AssessmentItem:
    """An individual assessment item with rubric."""
    question: str
    subject: str
    grade_level: str
    learning_objective: str
    rubric: Dict[str, str]  # score -> criteria
    sample_answer: Optional[str] = None
    max_score: int = 5

@dataclass
class StudentProgress:
    """Student's progress tracking data."""
    student_id: str
    subject: str
    objectives_mastered: List[str]
    areas_for_growth: List[str]
    recent_assessments: List[Dict[str, Any]]
    recommendations: List[str]

class EducationalAIService:
    """AI-powered educational planning and assessment service."""
    
    def __init__(self, openai_client):
        """Initialize with OpenAI client."""
        self.ai = openai_client
    
    def generate_term_plan(
        self,
        subject: str,
        grade_level: str,
        term: int,
        existing_objectives: Optional[List[str]] = None
    ) -> List[LearningObjective]:
        """Generate a term's learning objectives and progression.
        
        Args:
            subject: Subject area (e.g., 'Mathematics', 'Science')
            grade_level: Grade level (e.g., '9th', '10th')
            term: Term number (1-3)
            existing_objectives: Optional list of already-covered objectives
            
        Returns:
            List of learning objectives for the term
        """
        # Build a detailed prompt for curriculum planning
        context = {
            'subject': subject,
            'grade': grade_level,
            'term': term,
            'prior_learning': existing_objectives or []
        }
        
        prompt = f"""Create a detailed term plan for {subject} ({grade_level} Grade, Term {term}).

Previous Coverage:
{chr(10).join('- ' + obj for obj in context['prior_learning']) if context['prior_learning'] else 'No prior objectives provided'}

For each learning objective, provide:
1. Clear description
2. Key skills developed
3. Specific assessment criteria
4. Cross-curricular connections
5. Progressive difficulty alignment

Format each objective as:
Description: (clear learning outcome)
Skills: (comma-separated list)
Assessment: (bullet points)
"""
        
        try:
            response = self.ai.complete(prompt, temperature=0.7)
            return self._parse_term_plan(response['choices'][0]['text'])
        except Exception as e:
            logger.error('Failed to generate term plan', exc_info=e)
            return []
    
    def generate_assessment(
        self,
        objective: Union[LearningObjective, dict, str],
        assessment_type: str,
        student_level: str = 'standard'
    ) -> List[AssessmentItem]:
        """Generate assessment items for a learning objective.
        
        Args:
            objective: The learning objective to assess
            assessment_type: Type of assessment ('formative', 'summative', 'diagnostic')
            student_level: Differentiation level ('support', 'standard', 'extension')
            
        Returns:
            List of assessment items
        """
        obj = self._ensure_objective(objective)

        prompt = f"""Create {assessment_type} assessment items for:
        Subject: {obj.subject_area}
        Grade: {obj.grade_level}
        Objective: {obj.description}
        Level: {student_level}

        For each question:
        1. Clear, age-appropriate language
        2. Specific skill assessment
        3. Detailed scoring rubric
        4. Sample answer/solution
        5. Common misconception notes

        Create 3-5 questions that:
        - Progress in difficulty
        - Include different question types
        - Allow demonstration of understanding
        - Support meaningful feedback
        """

        try:
            response = self.ai.complete(prompt, temperature=0.7)
            return self._parse_assessment_items(response['choices'][0]['text'])
        except Exception as e:
            logger.error('Failed to generate assessment', exc_info=e)
            return []
    
    def analyze_student_progress(
        self,
        student_data: Dict[str, Any],
        subject_area: str,
        timeframe: str = 'term'
    ) -> StudentProgress:
        """Analyze student progress and generate recommendations.
        
        Args:
            student_data: Dictionary of student performance data
            subject_area: Subject to analyze
            timeframe: Analysis period ('term', 'year')
            
        Returns:
            StudentProgress with analysis and recommendations
        """
        # Format student data for analysis
        data_points = [
            f"Assessment {idx}: {result['score']}/{result['max']} - {result['notes']}"
            for idx, result in enumerate(student_data.get('assessments', []), 1)
        ]
        
        prompt = f"""Analyze student progress in {subject_area} over {timeframe}:

Assessment History:
{chr(10).join(data_points)}

Prior Teacher Notes:
{student_data.get('teacher_notes', 'No notes provided')}

Provide:
1. Mastered learning objectives
2. Areas needing development
3. Specific support recommendations
4. Next steps for extension
5. Learning strategy suggestions
"""
        
        try:
            response = self.ai.complete(prompt, temperature=0.7)
            return self._parse_progress_analysis(
                response['choices'][0]['text'],
                student_data['student_id'],
                subject_area
            )
        except Exception as e:
            logger.error('Failed to analyze student progress', exc_info=e)
            return StudentProgress(
                student_id=student_data['student_id'],
                subject=subject_area,
                objectives_mastered=[],
                areas_for_growth=[],
                recent_assessments=[],
                recommendations=['Analysis failed - please review manually']
            )
    
    def generate_differentiated_activities(
        self,
        objective: Union[LearningObjective, dict, str],
        class_profile: Dict[str, int]  # level -> number of students
    ) -> Dict[str, List[str]]:
        """Generate differentiated learning activities.
        
        Args:
            objective: Learning objective to address
            class_profile: Distribution of student levels
            
        Returns:
            Dictionary of activities by level
        """
        obj = self._ensure_objective(objective)

        prompt = f"""Create differentiated activities for:
        Objective: {obj.description}
        Subject: {obj.subject_area}
        Grade: {obj.grade_level}

        Class Profile:
        {chr(10).join(f'- {level}: {count} students' for level, count in class_profile.items())}

        For each level (support, standard, extension):
        1. 2-3 specific activities
        2. Success criteria
        3. Required resources
        4. Time estimation
        5. Key teaching points

        Ensure activities:
        - Target same objective
        - Vary in complexity
        - Allow progression
        - Support different learning styles
        """

        try:
            response = self.ai.complete(prompt, temperature=0.7)
            return self._parse_activities(response['choices'][0]['text'])
        except Exception as e:
            logger.error('Failed to generate activities', exc_info=e)
            return {
                'support': ['Activity generation failed - please plan manually'],
                'standard': ['Activity generation failed - please plan manually'],
                'extension': ['Activity generation failed - please plan manually']
            }
    
    def _parse_term_plan(self, text: str) -> List[LearningObjective]:
        """Parse AI response into learning objectives."""
        objectives = []
        current_obj = {}
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                if current_obj.get('description'):
                    objectives.append(LearningObjective(**current_obj))
                    current_obj = {}
                continue
                
            if line.startswith('Description:'):
                current_obj['description'] = line.split(':', 1)[1].strip()
            elif line.startswith('Skills:'):
                current_obj['skills'] = [
                    s.strip() 
                    for s in line.split(':', 1)[1].split(',')
                ]
            elif line.startswith('Assessment:'):
                current_obj['assessment_criteria'] = []
            elif line.startswith('-') and 'assessment_criteria' in current_obj:
                current_obj['assessment_criteria'].append(line.lstrip('- '))
        
        # Don't forget the last one
        if current_obj.get('description'):
            objectives.append(LearningObjective(**current_obj))
        
        return objectives
    
    def _parse_assessment_items(self, text: str) -> List[AssessmentItem]:
        """Parse AI response into assessment items."""
        items = []
        current_item = {}
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                if current_item.get('question'):
                    items.append(AssessmentItem(**current_item))
                    current_item = {}
                continue
                
            if line.startswith('Question:'):
                current_item['question'] = line.split(':', 1)[1].strip()
            elif line.startswith('Rubric:'):
                current_item['rubric'] = {}
            elif line.startswith('Sample:'):
                current_item['sample_answer'] = line.split(':', 1)[1].strip()
            elif line.startswith('-') and 'rubric' in current_item:
                score, criteria = line.lstrip('- ').split(':', 1)
                current_item['rubric'][score.strip()] = criteria.strip()
        
        # Don't forget the last one
        if current_item.get('question'):
            items.append(AssessmentItem(**current_item))
        
        return items
    
    def _parse_progress_analysis(
        self,
        text: str,
        student_id: str,
        subject: str
    ) -> StudentProgress:
        """Parse AI response into student progress analysis."""
        mastered = []
        growth = []
        recommendations = []
        current_section = None
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.lower().startswith('mastered'):
                current_section = mastered
            elif line.lower().startswith('growth'):
                current_section = growth
            elif line.lower().startswith('recommend'):
                current_section = recommendations
            elif line.startswith('-') and current_section is not None:
                current_section.append(line.lstrip('- '))
        
        return StudentProgress(
            student_id=student_id,
            subject=subject,
            objectives_mastered=mastered,
            areas_for_growth=growth,
            recent_assessments=[],  # Would come from actual assessment data
            recommendations=recommendations
        )
    
    def _parse_activities(self, text: str) -> Dict[str, List[str]]:
        """Parse AI response into differentiated activities."""
        activities = {
            'support': [],
            'standard': [],
            'extension': []
        }
        current_level = None
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.lower().startswith('support'):
                current_level = 'support'
            elif line.lower().startswith('standard'):
                current_level = 'standard'
            elif line.lower().startswith('extension'):
                current_level = 'extension'
            elif line.startswith('-') and current_level:
                activities[current_level].append(line.lstrip('- '))
        
        return activities

    def _ensure_objective(self, objective: Union[LearningObjective, dict, str]) -> LearningObjective:
        """Normalize an objective argument into a LearningObjective instance.

        Accepts a LearningObjective, a dict with compatible keys, or a string (description).
        """
        if isinstance(objective, LearningObjective):
            return objective

        if isinstance(objective, dict):
            # Map common dict keys to LearningObjective fields with safe defaults
            return LearningObjective(
                description=objective.get('description') or objective.get('objective') or str(objective),
                subject_area=objective.get('subject_area') or objective.get('subject') or 'Unknown',
                grade_level=objective.get('grade_level') or objective.get('grade') or 'Unknown',
                assessment_criteria=objective.get('assessment_criteria') or objective.get('assessment') or [],
                skills=objective.get('skills') or [],
                term=objective.get('term')
            )

        # Otherwise treat it as a free-text description
        return LearningObjective(
            description=str(objective),
            subject_area='Unknown',
            grade_level='Unknown',
            assessment_criteria=[],
            skills=[],
            term=None
        )