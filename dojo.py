"""
ARKADAŠ Dojo Module
===================

The Dojo is where the system trains, learns, and calibrates itself.
Like a martial arts training hall, it provides a space for refinement
and mastery of the King's Chamber capabilities.

Handles:
- System calibration
- Performance optimization  
- Learning from patterns
- Adaptive tuning
"""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
import time
import statistics


@dataclass
class TrainingSession:
    """A training session in the dojo."""
    session_id: str
    start_time: float
    end_time: Optional[float] = None
    iterations: int = 0
    metrics: Dict[str, List[float]] = field(default_factory=dict)
    improvements: Dict[str, float] = field(default_factory=dict)


@dataclass
class CalibrationRecord:
    """Record of a calibration adjustment."""
    timestamp: float
    component: str
    parameter: str
    old_value: float
    new_value: float
    reason: str


@dataclass
class DojoConfig:
    """Configuration for the Dojo."""
    training_mode: bool = True
    calibration_interval: float = 3600.0  # seconds
    learning_rate: float = 0.01
    max_iterations: int = 1000
    convergence_threshold: float = 0.001


class Dojo:
    """
    Training and calibration center for the King's Chamber.
    
    The Dojo continuously learns from system performance and
    adjusts parameters to optimize operation according to
    sacred geometry principles.
    """
    
    def __init__(self, config: Optional[DojoConfig] = None):
        """
        Initialize the Dojo.
        
        Args:
            config: Dojo configuration
        """
        self.config = config or DojoConfig()
        self.sessions: List[TrainingSession] = []
        self.calibrations: List[CalibrationRecord] = []
        self.parameters: Dict[str, float] = {}
        self.active = False
        self._last_calibration = time.time()
        
        # Initialize default parameters
        self._init_default_parameters()
    
    def _init_default_parameters(self) -> None:
        """Initialize default system parameters."""
        self.parameters = {
            "chamber_ratio": 0.333,  # King's Chamber ratio
            "base_frequency": 528.0,  # Solfeggio frequency
            "aperture_focal_angle": 90.0,  # degrees
            "sync_ratio": 0.333,
            "organic_rate": 60.0,  # Hz
            "digital_rate": 1000.0,  # Hz
        }
    
    def start_training_session(self, session_id: str) -> TrainingSession:
        """
        Start a new training session.
        
        Args:
            session_id: Unique identifier for session
            
        Returns:
            TrainingSession object
        """
        session = TrainingSession(
            session_id=session_id,
            start_time=time.time()
        )
        
        self.sessions.append(session)
        return session
    
    def record_metric(
        self,
        session_id: str,
        metric_name: str,
        value: float
    ) -> None:
        """
        Record a training metric.
        
        Args:
            session_id: Session to record to
            metric_name: Name of metric
            value: Metric value
        """
        session = self._get_session(session_id)
        if not session:
            return
        
        if metric_name not in session.metrics:
            session.metrics[metric_name] = []
        
        session.metrics[metric_name].append(value)
    
    def _get_session(self, session_id: str) -> Optional[TrainingSession]:
        """Get a session by ID."""
        for session in self.sessions:
            if session.session_id == session_id:
                return session
        return None
    
    def end_training_session(self, session_id: str) -> Optional[TrainingSession]:
        """
        End a training session and analyze results.
        
        Args:
            session_id: Session to end
            
        Returns:
            Completed TrainingSession
        """
        session = self._get_session(session_id)
        if not session:
            return None
        
        session.end_time = time.time()
        
        # Calculate improvements
        for metric_name, values in session.metrics.items():
            if len(values) >= 2:
                initial = values[0]
                final = values[-1]
                
                if initial != 0:
                    improvement = (final - initial) / initial
                    session.improvements[metric_name] = improvement
        
        return session
    
    def calibrate_parameter(
        self,
        component: str,
        parameter: str,
        new_value: float,
        reason: str = "Manual calibration"
    ) -> None:
        """
        Calibrate a system parameter.
        
        Args:
            component: Component being calibrated
            parameter: Parameter name
            new_value: New value
            reason: Reason for calibration
        """
        param_key = f"{component}.{parameter}"
        old_value = self.parameters.get(param_key, 0.0)
        
        # Record calibration
        record = CalibrationRecord(
            timestamp=time.time(),
            component=component,
            parameter=parameter,
            old_value=old_value,
            new_value=new_value,
            reason=reason
        )
        
        self.calibrations.append(record)
        self.parameters[param_key] = new_value
        self._last_calibration = time.time()
    
    def auto_calibrate(self, metrics: Dict[str, float]) -> List[CalibrationRecord]:
        """
        Automatically calibrate based on performance metrics.
        
        Uses gradient descent with the configured learning rate.
        
        Args:
            metrics: Current performance metrics
            
        Returns:
            List of calibration records
        """
        records = []
        
        # Check if calibration interval has passed
        if time.time() - self._last_calibration < self.config.calibration_interval:
            return records
        
        # Calibrate chamber ratio if efficiency is low
        if "aperture_efficiency" in metrics:
            efficiency = metrics["aperture_efficiency"]
            target_efficiency = 0.8
            
            if efficiency < target_efficiency:
                # Adjust chamber ratio
                current = self.parameters.get("chamber_ratio", 0.333)
                adjustment = self.config.learning_rate * (target_efficiency - efficiency)
                new_value = max(0.1, min(0.5, current + adjustment))
                
                self.calibrate_parameter(
                    "aperture",
                    "chamber_ratio",
                    new_value,
                    f"Auto-calibrate efficiency: {efficiency:.3f} -> target {target_efficiency}"
                )
                records.append(self.calibrations[-1])
        
        # Calibrate sync ratio if resonance is low
        if "harmonic_resonance" in metrics:
            resonance = metrics["harmonic_resonance"]
            target_resonance = 0.9
            
            if resonance < target_resonance:
                current = self.parameters.get("sync_ratio", 0.333)
                adjustment = self.config.learning_rate * (target_resonance - resonance)
                new_value = max(0.1, min(0.5, current + adjustment))
                
                self.calibrate_parameter(
                    "synchronizer",
                    "sync_ratio",
                    new_value,
                    f"Auto-calibrate resonance: {resonance:.3f} -> target {target_resonance}"
                )
                records.append(self.calibrations[-1])
        
        return records
    
    async def training_loop(
        self,
        metrics_provider: Callable[[], Dict[str, float]],
        iterations: int = 100
    ) -> TrainingSession:
        """
        Run a training loop to optimize system parameters.
        
        Args:
            metrics_provider: Async function that provides current metrics
            iterations: Number of iterations to train
            
        Returns:
            Completed TrainingSession
        """
        session_id = f"training_{int(time.time())}"
        session = self.start_training_session(session_id)
        
        for i in range(iterations):
            # Get current metrics
            metrics = metrics_provider()
            
            # Record metrics
            for name, value in metrics.items():
                self.record_metric(session_id, name, value)
            
            # Auto-calibrate
            if self.config.training_mode:
                self.auto_calibrate(metrics)
            
            session.iterations += 1
            
            # Check for convergence
            if self._check_convergence(session):
                break
            
            # Small delay between iterations
            await asyncio.sleep(0.01)
        
        return self.end_training_session(session_id)
    
    def _check_convergence(self, session: TrainingSession) -> bool:
        """
        Check if training has converged.
        
        Args:
            session: Current training session
            
        Returns:
            True if converged
        """
        if session.iterations < 10:
            return False
        
        # Check if recent metrics are stable
        for metric_name, values in session.metrics.items():
            if len(values) < 10:
                continue
            
            recent = values[-10:]
            if len(recent) > 1:
                std = statistics.stdev(recent)
                mean = statistics.mean(recent)
                
                # Coefficient of variation
                if mean != 0:
                    cv = std / abs(mean)
                    if cv > self.config.convergence_threshold:
                        return False
        
        return True
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get training statistics."""
        total_sessions = len(self.sessions)
        completed_sessions = sum(
            1 for s in self.sessions if s.end_time is not None
        )
        
        total_iterations = sum(s.iterations for s in self.sessions)
        
        avg_improvements = {}
        if completed_sessions > 0:
            for session in self.sessions:
                if session.end_time:
                    for metric, improvement in session.improvements.items():
                        if metric not in avg_improvements:
                            avg_improvements[metric] = []
                        avg_improvements[metric].append(improvement)
            
            # Calculate averages
            avg_improvements = {
                metric: statistics.mean(values)
                for metric, values in avg_improvements.items()
            }
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "total_iterations": total_iterations,
            "total_calibrations": len(self.calibrations),
            "avg_improvements": avg_improvements,
            "training_mode": self.config.training_mode,
            "current_parameters": self.parameters.copy()
        }
    
    def get_calibration_history(
        self,
        component: Optional[str] = None,
        limit: int = 10
    ) -> List[CalibrationRecord]:
        """
        Get calibration history.
        
        Args:
            component: Optional component filter
            limit: Maximum records to return
            
        Returns:
            List of CalibrationRecord objects
        """
        calibrations = self.calibrations
        
        if component:
            calibrations = [
                c for c in calibrations if c.component == component
            ]
        
        return calibrations[-limit:]
    
    def reset_to_defaults(self) -> None:
        """Reset all parameters to defaults."""
        self._init_default_parameters()
        self.calibrations.clear()
        
        # Record reset
        record = CalibrationRecord(
            timestamp=time.time(),
            component="system",
            parameter="all",
            old_value=0.0,
            new_value=0.0,
            reason="Reset to defaults"
        )
        self.calibrations.append(record)
