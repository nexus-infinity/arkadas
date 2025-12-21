"""
OBI-WAN Collective Intelligence Module
=======================================

Aggregates wisdom from multiple sensor nodes to form a unified
understanding, transcending individual sensor limitations.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import statistics

from .sensor_node import SensorReading, SensorType
from .network import ObiWanNetwork


@dataclass
class FusionWeights:
    """Weights for different sensor types in data fusion."""
    electromagnetic: float = 0.4
    acoustic: float = 0.4
    thermal: float = 0.2
    proximity: float = 0.3
    chemical: float = 0.3


@dataclass
class CollectiveInsight:
    """An insight derived from collective intelligence."""
    angle: float  # Primary direction of interest
    intensity: float  # Strength of the insight
    confidence: float  # Confidence level
    contributing_sensors: List[str]
    sensor_agreement: float  # How well sensors agree
    timestamp: float


class CollectiveIntelligence:
    """
    Aggregates wisdom from the OBI-WAN sensor network.
    
    Like the Force, collective intelligence emerges from the 
    interconnection of all nodes, providing awareness beyond
    individual sensing capabilities.
    """
    
    def __init__(
        self,
        network: ObiWanNetwork,
        fusion_weights: Optional[FusionWeights] = None
    ):
        """
        Initialize collective intelligence system.
        
        Args:
            network: OBI-WAN network to aggregate from
            fusion_weights: Weights for sensor fusion
        """
        self.network = network
        self.fusion_weights = fusion_weights or FusionWeights()
        self.insights_history: List[CollectiveInsight] = []
    
    def aggregate_readings(
        self,
        readings: List[SensorReading],
        angle_resolution: float = 10.0
    ) -> Dict[float, float]:
        """
        Aggregate sensor readings by angle.
        
        Args:
            readings: List of sensor readings to aggregate
            angle_resolution: Angular resolution for binning
            
        Returns:
            Dictionary mapping angles to aggregated values
        """
        # Create angle bins
        num_bins = int(360.0 / angle_resolution)
        bins: Dict[float, List[float]] = {
            i * angle_resolution: [] for i in range(num_bins)
        }
        
        # Distribute readings into bins
        for reading in readings:
            bin_angle = (reading.angle // angle_resolution) * angle_resolution
            
            # Apply sensor type weight
            weight = self._get_sensor_weight(reading.sensor_type)
            weighted_value = reading.value * weight * reading.confidence
            
            bins[bin_angle].append(weighted_value)
        
        # Aggregate each bin
        aggregated = {}
        for angle, values in bins.items():
            if values:
                # Use weighted average
                aggregated[angle] = sum(values) / len(values)
        
        return aggregated
    
    def _get_sensor_weight(self, sensor_type: SensorType) -> float:
        """Get fusion weight for a sensor type."""
        weight_map = {
            SensorType.ELECTROMAGNETIC: self.fusion_weights.electromagnetic,
            SensorType.ACOUSTIC: self.fusion_weights.acoustic,
            SensorType.THERMAL: self.fusion_weights.thermal,
            SensorType.PROXIMITY: self.fusion_weights.proximity,
            SensorType.CHEMICAL: self.fusion_weights.chemical
        }
        return weight_map.get(sensor_type, 0.3)
    
    def generate_insight(
        self,
        angle_range: Optional[tuple] = None
    ) -> Optional[CollectiveInsight]:
        """
        Generate a collective insight from current network state.
        
        Args:
            angle_range: Optional (min, max) angle range to focus on
            
        Returns:
            CollectiveInsight if sufficient data available
        """
        # Collect readings from network
        readings = self.network.collect_readings(angle_range=angle_range)
        
        if not readings:
            return None
        
        # Aggregate by angle
        aggregated = self.aggregate_readings(readings, angle_resolution=10.0)
        
        if not aggregated:
            return None
        
        # Find angle with maximum intensity
        max_angle = max(aggregated.keys(), key=lambda a: aggregated[a])
        max_intensity = aggregated[max_angle]
        
        # Calculate confidence based on sensor agreement
        angle_readings = [r for r in readings if abs(r.angle - max_angle) < 15.0]
        
        if len(angle_readings) < 2:
            confidence = 0.5
            agreement = 0.5
        else:
            # Calculate standard deviation as measure of agreement
            values = [r.value for r in angle_readings]
            mean_val = statistics.mean(values)
            if len(values) > 1:
                std_val = statistics.stdev(values)
                # Lower std = higher agreement
                agreement = max(0.0, 1.0 - (std_val / (mean_val + 0.001)))
            else:
                agreement = 1.0
            
            # Confidence from average of individual confidences
            avg_confidence = statistics.mean([r.confidence for r in angle_readings])
            confidence = (agreement + avg_confidence) / 2.0
        
        # Get contributing sensors
        contributing_sensors = list(set(r.sensor_id for r in angle_readings))
        
        # Get timestamp from most recent reading
        timestamp = max(r.timestamp for r in readings)
        
        insight = CollectiveInsight(
            angle=max_angle,
            intensity=max_intensity,
            confidence=confidence,
            contributing_sensors=contributing_sensors,
            sensor_agreement=agreement,
            timestamp=timestamp
        )
        
        self.insights_history.append(insight)
        
        # Keep history manageable
        if len(self.insights_history) > 100:
            self.insights_history.pop(0)
        
        return insight
    
    def analyze_coverage(self) -> Dict[str, Any]:
        """
        Analyze network coverage quality.
        
        Returns:
            Dictionary with coverage metrics
        """
        coverage_map = self.network.get_coverage_map(resolution=10.0)
        
        if not coverage_map:
            return {
                "min_coverage": 0,
                "max_coverage": 0,
                "avg_coverage": 0.0,
                "uniformity": 0.0
            }
        
        coverages = list(coverage_map.values())
        min_coverage = min(coverages)
        max_coverage = max(coverages)
        avg_coverage = statistics.mean(coverages)
        
        # Uniformity: how evenly distributed is coverage
        if len(coverages) > 1:
            std_coverage = statistics.stdev(coverages)
            uniformity = 1.0 - (std_coverage / (avg_coverage + 0.001))
        else:
            uniformity = 1.0
        
        return {
            "min_coverage": min_coverage,
            "max_coverage": max_coverage,
            "avg_coverage": avg_coverage,
            "uniformity": max(0.0, min(1.0, uniformity)),
            "coverage_map": coverage_map
        }
    
    def get_wisdom_summary(self) -> Dict[str, Any]:
        """
        Get a summary of collective wisdom.
        
        Returns:
            Dictionary with wisdom metrics
        """
        if not self.insights_history:
            return {
                "total_insights": 0,
                "avg_confidence": 0.0,
                "avg_agreement": 0.0
            }
        
        recent_insights = self.insights_history[-20:]
        
        avg_confidence = statistics.mean([i.confidence for i in recent_insights])
        avg_agreement = statistics.mean([i.sensor_agreement for i in recent_insights])
        
        return {
            "total_insights": len(self.insights_history),
            "recent_insights": len(recent_insights),
            "avg_confidence": avg_confidence,
            "avg_agreement": avg_agreement,
            "network_stats": self.network.get_network_stats(),
            "coverage_analysis": self.analyze_coverage()
        }
