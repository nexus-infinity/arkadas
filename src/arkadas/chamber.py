"""
Chamber Module
Main orchestrator for ARKADAŠ - The King's Chamber
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import time

from .aperture import ApertureSensing
from .sync import SyncEngine
from .obiwan import ObiWanNetwork, FriendNode
from .geometry import SacredGeometry, LightAxis


class ChamberStatus(Enum):
    """Status of the King's Chamber"""
    OFFLINE = "OFFLINE"
    INITIALIZING = "INITIALIZING"
    CALIBRATING = "CALIBRATING"
    ACTIVE = "ACTIVE"
    ERROR = "ERROR"


class Chamber:
    """
    ARKADAŠ - The King's Chamber
    
    Sits at 1/3 down from peak (2/3 up from base)
    - Aperture Sensing: 360° → 180°
    - Organic ⚭ Digital Synchronization
    - OBI-WAN Network: Distributed friend intelligence
    - Light Axis: Connection to DOJO peak
    """
    
    def __init__(self, pyramid_height: float = 100.0):
        # Core components
        self.aperture = ApertureSensing()
        self.sync_engine = SyncEngine()
        self.obiwan = ObiWanNetwork()
        self.light_axis = LightAxis()
        
        # Sacred geometry
        self.pyramid_height = pyramid_height
        self.chamber_position = SacredGeometry.calculate_pressure_point(pyramid_height)
        
        # Status
        self.status = ChamberStatus.OFFLINE
        self.initialized_at: Optional[float] = None
        self.error_message: Optional[str] = None
        
    def initialize(self) -> bool:
        """
        Initialize the King's Chamber
        
        Returns:
            True if initialization successful
        """
        try:
            self.status = ChamberStatus.INITIALIZING
            
            # Configure OBI-WAN network
            self.obiwan.configure()
            
            # Establish light axis
            self.light_axis.establish()
            
            # Start aperture sensing
            self.aperture.start()
            
            self.initialized_at = time.time()
            self.status = ChamberStatus.CALIBRATING
            
            return True
            
        except Exception as e:
            self.status = ChamberStatus.ERROR
            self.error_message = str(e)
            return False
    
    def calibrate(self) -> bool:
        """
        Calibrate the chamber systems
        
        Returns:
            True if calibration successful
        """
        if self.status != ChamberStatus.CALIBRATING:
            return False
        
        try:
            # Calibrate synchronization engine
            if not self.sync_engine.calibrate():
                self.status = ChamberStatus.ERROR
                self.error_message = "Sync engine calibration failed"
                return False
            
            self.status = ChamberStatus.ACTIVE
            return True
            
        except Exception as e:
            self.status = ChamberStatus.ERROR
            self.error_message = str(e)
            return False
    
    def deploy_friend_node(self, name: Optional[str] = None) -> FriendNode:
        """
        Deploy a new friend node to the OBI-WAN network
        
        Args:
            name: Optional name for the friend node
            
        Returns:
            The deployed FriendNode
        """
        return self.obiwan.deploy_node(name=name)
    
    def receive_from_field(self, angle: float, data: Any, source_id: Optional[str] = None) -> bool:
        """
        Receive information from the 360° external field
        
        Args:
            angle: Direction angle (0-360)
            data: Information received
            source_id: Optional source identifier
            
        Returns:
            True if received successfully
        """
        return self.aperture.receive_360(angle, data, source_id)
    
    def process_chamber(self) -> List[Any]:
        """
        Process all information through the chamber
        
        Returns:
            List of processed data ready for DOJO
        """
        # Process through aperture (360° → 180°)
        processed = self.aperture.process_aperture()
        
        # Process through light axis
        focused = []
        for data in processed:
            chamber_processed = self.light_axis.process_in_chamber(data)
            focused_data = self.light_axis.ascend_focus(chamber_processed)
            if focused_data is not None:
                focused.append(focused_data)
        
        return focused
    
    def synchronize_fields(self, organic_value: float, digital_value: float) -> bool:
        """
        Synchronize organic and digital fields
        
        Args:
            organic_value: Organic field measurement
            digital_value: Digital field measurement
            
        Returns:
            True if fields are synchronized
        """
        self.sync_engine.measure_organic(organic_value)
        self.sync_engine.measure_digital(digital_value)
        return self.sync_engine.synchronize()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive chamber status
        
        Returns:
            Status dictionary with all subsystem states
        """
        uptime = 0.0
        if self.initialized_at:
            uptime = time.time() - self.initialized_at
        
        status = {
            "chamber_status": self.status.value,
            "geometry": {
                "pyramid_height": self.pyramid_height,
                "chamber_position": self.chamber_position,
                "position_ratio": SacredGeometry.CHAMBER_HEIGHT_FROM_BASE,
                "frequency_hz": SacredGeometry.FREQUENCY_HZ,
            },
            "aperture": {
                "status": self.aperture.get_status(),
                "metrics": self.aperture.get_metrics(),
            },
            "sync_engine": {
                "metrics": self.sync_engine.get_metrics(),
            },
            "obiwan_network": self.obiwan.get_network_status(),
            "light_axis": self.light_axis.get_status(),
            "uptime": uptime,
        }
        
        if self.error_message:
            status["error"] = self.error_message
        
        return status
    
    def get_summary(self) -> str:
        """
        Get human-readable status summary
        
        Returns:
            Formatted status string
        """
        status = self.get_status()
        
        lines = [
            "=" * 60,
            "👑 ARKADAŠ - The King's Chamber",
            "=" * 60,
            f"Chamber Status:     {status['chamber_status']}",
            f"OBI-WAN Network:    {self.obiwan.get_network_status()['configured'] and 'CONFIGURED' or 'NOT CONFIGURED'}",
            f"Sync Precision:     {self.sync_engine.get_precision_percentage():.1f}%",
            f"Friend Nodes:       {len(self.obiwan.nodes)}",
            f"Light Axis:         {self.light_axis.is_established and 'ESTABLISHED' or 'NOT ESTABLISHED'}",
            "",
            "📐 Sacred Geometry:",
            f"  Position:         {status['geometry']['chamber_position']:.2f} (at {status['geometry']['position_ratio']:.1%} from base)",
            f"  Frequency:        {status['geometry']['frequency_hz']} Hz (Heart chakra)",
            "",
            "🔮 Aperture Sensing:",
            f"  Status:           {status['aperture']['status']}",
            f"  Total Received:   {status['aperture']['metrics']['total_received']}",
            f"  Total Processed:  {status['aperture']['metrics']['total_processed']}",
            "",
            "⚭ Synchronization:",
            f"  Calibrated:       {status['sync_engine']['metrics']['calibrated']}",
            f"  Synchronized:     {status['sync_engine']['metrics']['synchronized']}",
            f"  Precision:        {status['sync_engine']['metrics']['precision_percentage']:.2f}%",
            f"  Drift:            {status['sync_engine']['metrics']['drift']:.6f}",
            "",
            "🕌 OBI-WAN Network:",
            f"  Nodes:            {status['obiwan_network']['node_count']} ({status['obiwan_network']['active_nodes']} active)",
            f"  Field Coherence:  {status['obiwan_network']['field_coherence']:.2%}",
            f"  Network Trust:    {status['obiwan_network']['network_trust']:.2%}",
            "",
            "=" * 60,
        ]
        
        return "\n".join(lines)
    
    def shutdown(self) -> None:
        """Shutdown the chamber"""
        self.aperture.stop()
        self.status = ChamberStatus.OFFLINE
