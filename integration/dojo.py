"""
DOJO Module - Upward to DOJO.

Provides interface for upward integration to the DOJO layer,
handling training, learning, and skill development coordination.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class Skill:
    """Represents a learnable skill."""
    
    def __init__(self, skill_name: str, difficulty: int = 1):
        """
        Initialize a skill.
        
        Args:
            skill_name: Name of the skill
            difficulty: Difficulty level (1-10)
        """
        self.skill_name = skill_name
        self.difficulty = difficulty
        self.proficiency = 0.0
        self.practice_sessions = 0
        self.last_practiced = None
        
    def practice(self, quality: float = 0.5):
        """
        Practice the skill.
        
        Args:
            quality: Quality of practice session (0-1)
        """
        # Proficiency increases with practice
        gain = quality * (1.0 / self.difficulty) * 0.1
        self.proficiency = min(1.0, self.proficiency + gain)
        self.practice_sessions += 1
        self.last_practiced = datetime.now()
        
    def is_mastered(self) -> bool:
        """Check if skill is mastered."""
        return self.proficiency >= 0.9


class TrainingSession:
    """Represents a DOJO training session."""
    
    def __init__(self, session_id: str, focus: str):
        """
        Initialize training session.
        
        Args:
            session_id: Session identifier
            focus: Focus area for training
        """
        self.session_id = session_id
        self.focus = focus
        self.start_time = datetime.now()
        self.end_time = None
        self.skills_practiced: List[str] = []
        self.insights_gained: List[str] = []
        self.effectiveness = 0.0
        
    def add_skill(self, skill_name: str):
        """Add practiced skill."""
        self.skills_practiced.append(skill_name)
        
    def add_insight(self, insight: str):
        """Record an insight."""
        self.insights_gained.append(insight)
        
    def complete(self, effectiveness: float):
        """
        Complete the session.
        
        Args:
            effectiveness: Overall effectiveness (0-1)
        """
        self.end_time = datetime.now()
        self.effectiveness = effectiveness
        
    def get_duration(self) -> Optional[float]:
        """Get session duration in minutes."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60
        return None


class DOJOInterface:
    """Interface for upward communication to DOJO layer."""
    
    def __init__(self, dojo_name: str = "ARKADAS_DOJO"):
        """
        Initialize DOJO interface.
        
        Args:
            dojo_name: Name of the DOJO
        """
        self.dojo_name = dojo_name
        self.skills: Dict[str, Skill] = {}
        self.active_session: Optional[TrainingSession] = None
        self.completed_sessions: List[TrainingSession] = []
        self.mastery_level = 0.0
        
    def register_skill(self, skill_name: str, difficulty: int = 1) -> Skill:
        """
        Register a new skill.
        
        Args:
            skill_name: Name of skill
            difficulty: Difficulty level
            
        Returns:
            Created Skill object
        """
        skill = Skill(skill_name, difficulty)
        self.skills[skill_name] = skill
        return skill
    
    def start_training_session(self, focus: str) -> TrainingSession:
        """
        Start a new training session.
        
        Args:
            focus: Training focus area
            
        Returns:
            Created TrainingSession
        """
        if self.active_session:
            # Complete previous session
            self.active_session.complete(0.5)
            self.completed_sessions.append(self.active_session)
            
        session_id = f"session_{len(self.completed_sessions) + 1:04d}"
        self.active_session = TrainingSession(session_id, focus)
        return self.active_session
    
    def practice_skill(self, skill_name: str, quality: float = 0.5):
        """
        Practice a skill.
        
        Args:
            skill_name: Skill to practice
            quality: Practice quality
        """
        if skill_name not in self.skills:
            self.register_skill(skill_name)
            
        self.skills[skill_name].practice(quality)
        
        if self.active_session:
            self.active_session.add_skill(skill_name)
            
        self._update_mastery()
        
    def record_insight(self, insight: str):
        """
        Record a learning insight.
        
        Args:
            insight: Insight description
        """
        if self.active_session:
            self.active_session.add_insight(insight)
            
    def complete_session(self, effectiveness: float = 0.7):
        """
        Complete current training session.
        
        Args:
            effectiveness: Session effectiveness
        """
        if self.active_session:
            self.active_session.complete(effectiveness)
            self.completed_sessions.append(self.active_session)
            self.active_session = None
            
    def get_skill_proficiency(self, skill_name: str) -> float:
        """
        Get proficiency level for a skill.
        
        Args:
            skill_name: Skill name
            
        Returns:
            Proficiency level (0-1)
        """
        skill = self.skills.get(skill_name)
        return skill.proficiency if skill else 0.0
    
    def get_mastered_skills(self) -> List[str]:
        """
        Get list of mastered skills.
        
        Returns:
            List of skill names
        """
        return [name for name, skill in self.skills.items() if skill.is_mastered()]
    
    def _update_mastery(self):
        """Update overall mastery level."""
        if not self.skills:
            self.mastery_level = 0.0
            return
            
        total_proficiency = sum(skill.proficiency for skill in self.skills.values())
        self.mastery_level = total_proficiency / len(self.skills)
        
    def get_dojo_status(self) -> Dict[str, Any]:
        """
        Get DOJO status summary.
        
        Returns:
            Status information
        """
        return {
            'dojo_name': self.dojo_name,
            'total_skills': len(self.skills),
            'mastered_skills': len(self.get_mastered_skills()),
            'mastery_level': self.mastery_level,
            'total_sessions': len(self.completed_sessions),
            'active_session': self.active_session is not None,
            'average_effectiveness': self._calculate_average_effectiveness()
        }
    
    def _calculate_average_effectiveness(self) -> float:
        """Calculate average session effectiveness."""
        if not self.completed_sessions:
            return 0.0
        total = sum(s.effectiveness for s in self.completed_sessions)
        return total / len(self.completed_sessions)
    
    def request_guidance(self, area: str) -> str:
        """
        Request guidance from DOJO on specific area.
        
        Args:
            area: Area needing guidance
            
        Returns:
            Guidance message
        """
        # Simple guidance logic
        if area in self.skills:
            skill = self.skills[area]
            if skill.proficiency < 0.3:
                return f"Focus on fundamental practice of {area}"
            elif skill.proficiency < 0.7:
                return f"Continue steady practice of {area}, you're progressing well"
            else:
                return f"You're close to mastering {area}, refine advanced techniques"
        else:
            return f"Begin learning {area} with foundational exercises"
