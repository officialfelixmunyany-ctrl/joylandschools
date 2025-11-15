"""OpenAI integration for GPT models."""

from typing import Optional, Any, Dict
from django.conf import settings
import openai
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# Initialize the OpenAI client with settings
openai.api_key = settings.OPENAI_API_KEY


@lru_cache(maxsize=1)
def get_default_model() -> str:
    """Get the default model to use based on settings.
    
    Returns:
        Model identifier string to use with OpenAI API
    """
    if getattr(settings, 'ENABLE_GPT5_MINI', False):
        return 'gpt-5-mini'
    return getattr(settings, 'OPENAI_DEFAULT_MODEL', 'gpt-4')


class OpenAIClient:
    """Client for interacting with OpenAI APIs."""
    
    def __init__(self, model: Optional[str] = None):
        """Initialize the client.
        
        Args:
            model: Optional model override. If not provided, uses settings.
        """
        self.model = model or get_default_model()
    
    def complete(
        self, 
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Generate a completion for the given prompt.
        
        Args:
            prompt: The text prompt to complete
            max_tokens: Maximum tokens in the response
            temperature: Sampling temperature (0-1)
            **kwargs: Additional parameters for openai.Completion.create
            
        Returns:
            OpenAI API response
            
        Raises:
            Exception: If the API call fails
        """
        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            logger.debug('Generated completion for prompt: %s...', prompt[:100])
            return response
        except Exception as e:
            logger.error('OpenAI API error', exc_info=e)
            raise
    
    def embed(self, text: str) -> Dict[str, Any]:
        """Generate embeddings for the given text.
        
        Args:
            text: Text to generate embeddings for
            
        Returns:
            OpenAI API response with embeddings
            
        Raises:
            Exception: If the API call fails
        """
        try:
            response = openai.Embedding.create(
                model='text-embedding-ada-002',
                input=text
            )
            logger.debug('Generated embeddings for text: %s...', text[:100])
            return response
        except Exception as e:
            logger.error('OpenAI API error', exc_info=e)
            raise

    def analyze_student_application(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a student registration request for insights.
        
        Args:
            request_data: Registration request data including academic history,
                        interests, and background
        
        Returns:
            Dict containing:
            - recommended_class_level: Suggested class placement
            - learning_style: Identified learning style preferences
            - academic_interests: Key areas of interest
            - support_needs: Potential areas needing additional support
        """
        prompt = f"""Analyze this student registration data and provide educational insights:
Background: {request_data.get('heard_about', '')}
Age: {request_data.get('birth_year', 'Unknown')}
Interests/Notes: {request_data.get('notes', '')}

Provide specific recommendations for:
1. Recommended class level and placement
2. Learning style indicators
3. Key academic interest areas
4. Potential support needs or areas for attention"""

        try:
            response = self.complete(prompt, temperature=0.7)
            return self._parse_student_analysis(response['choices'][0]['text'])
        except Exception as e:
            logger.error('Failed to analyze student application', exc_info=e)
            return {
                'recommended_class_level': 'Needs manual review',
                'learning_style': 'Unable to determine',
                'academic_interests': [],
                'support_needs': []
            }

    def generate_admission_questions(self, age_group: str, focus_areas: list) -> list:
        """Generate personalized admission assessment questions.
        
        Args:
            age_group: Target age group (e.g., '5-7', '8-10', '11-13')
            focus_areas: List of subjects or skills to assess
            
        Returns:
            List of generated questions with difficulty levels
        """
        prompt = f"""Create age-appropriate educational assessment questions for:
Age Group: {age_group}
Focus Areas: {', '.join(focus_areas)}

For each area, generate 2-3 questions that:
1. Match cognitive development level
2. Assess both knowledge and thinking skills
3. Include clear scoring criteria
4. Are engaging and relevant

Format each question with:
- Subject
- Question text
- Expected learning outcome
- Scoring guide (1-5 points)"""

        try:
            response = self.complete(prompt, temperature=0.8, max_tokens=1500)
            return self._parse_assessment_questions(response['choices'][0]['text'])
        except Exception as e:
            logger.error('Failed to generate admission questions', exc_info=e)
            return []

    def analyze_teacher_workload(self, assignments: list) -> Dict[str, Any]:
        """Analyze teacher assignments and workload distribution.
        
        Args:
            assignments: List of teaching assignments with class sizes,
                       subjects, and time allocations
            
        Returns:
            Dict containing workload analysis and optimization suggestions
        """
        prompt = f"""Analyze this teaching workload data:
{assignments}

Provide:
1. Total contact hours and preparation time
2. Subject distribution analysis
3. Student load analysis
4. Specific workload optimization recommendations
5. Potential scheduling conflicts or concerns"""

        try:
            response = self.complete(prompt, temperature=0.7)
            return self._parse_workload_analysis(response['choices'][0]['text'])
        except Exception as e:
            logger.error('Failed to analyze teacher workload', exc_info=e)
            return {
                'total_hours': 0,
                'warnings': ['Analysis failed - please review manually'],
                'recommendations': []
            }

    def draft_announcement(self, 
                         topic: str, 
                         audience: str,
                         key_points: list,
                         tone: str = 'professional') -> str:
        """Draft a school announcement with appropriate tone and content.
        
        Args:
            topic: Main announcement subject
            audience: Target audience (students/parents/teachers)
            key_points: List of points to cover
            tone: Desired communication tone
            
        Returns:
            Drafted announcement text
        """
        prompt = f"""Create a school announcement:
Topic: {topic}
Audience: {audience}
Tone: {tone}
Key Points to Cover:
{chr(10).join(f'- {point}' for point in key_points)}

Requirements:
1. Clear and concise language
2. Appropriate for {audience}
3. Include all key points
4. Maintain {tone} tone
5. Include any relevant next steps or actions"""

        try:
            response = self.complete(prompt, temperature=0.7)
            return response['choices'][0]['text'].strip()
        except Exception as e:
            logger.error('Failed to draft announcement', exc_info=e)
            return ""

    def _parse_student_analysis(self, text: str) -> Dict[str, Any]:
        """Parse the AI response into structured student analysis data."""
        lines = text.strip().split('\n')
        result = {
            'recommended_class_level': '',
            'learning_style': '',
            'academic_interests': [],
            'support_needs': []
        }
        
        current_section = ''
        for line in lines:
            line = line.strip()
            if line.lower().startswith('recommend'):
                current_section = 'recommended_class_level'
                result[current_section] = line.split(':', 1)[1].strip() if ':' in line else line
            elif line.lower().startswith('learning style'):
                current_section = 'learning_style'
                result[current_section] = line.split(':', 1)[1].strip() if ':' in line else line
            elif line.lower().startswith('academic'):
                current_section = 'academic_interests'
                result[current_section] = []
            elif line.lower().startswith('support'):
                current_section = 'support_needs'
                result[current_section] = []
            elif line.startswith('-') and current_section in ['academic_interests', 'support_needs']:
                result[current_section].append(line.lstrip('- '))
                
        return result

    def _parse_assessment_questions(self, text: str) -> list:
        """Parse the AI response into structured assessment questions."""
        questions = []
        current_question = {}
        
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                if current_question:
                    questions.append(current_question)
                    current_question = {}
            elif line.startswith('Subject:'):
                current_question['subject'] = line.split(':', 1)[1].strip()
            elif line.startswith('Question:'):
                current_question['question'] = line.split(':', 1)[1].strip()
            elif line.startswith('Learning Outcome:'):
                current_question['outcome'] = line.split(':', 1)[1].strip()
            elif line.startswith('Scoring:'):
                current_question['scoring'] = line.split(':', 1)[1].strip()
                
        if current_question:
            questions.append(current_question)
            
        return questions

    def _parse_workload_analysis(self, text: str) -> Dict[str, Any]:
        """Parse the AI response into structured workload analysis."""
        lines = text.strip().split('\n')
        analysis = {
            'total_hours': 0,
            'warnings': [],
            'recommendations': []
        }
        
        current_section = ''
        for line in lines:
            line = line.strip()
            if line.lower().startswith('total hours:'):
                try:
                    analysis['total_hours'] = float(line.split(':')[1].strip().split()[0])
                except (ValueError, IndexError):
                    pass
            elif line.startswith('Warning:') or line.startswith('⚠'):
                analysis['warnings'].append(line.split(':', 1)[1].strip() if ':' in line else line)
            elif line.startswith('Recommendation:') or line.startswith('→'):
                analysis['recommendations'].append(line.split(':', 1)[1].strip() if ':' in line else line)
                
        return analysis