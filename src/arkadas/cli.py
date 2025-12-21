"""
CLI Module
Command-line interface for ARKADAŠ chamber control
"""

import sys
from typing import Optional

from .chamber import Chamber


def main():
    """Main CLI entry point"""
    print("👑 ARKADAŠ - The King's Chamber")
    print("Organic ⚭ Digital Synchronization | 360° sensing → 180° focus")
    print()
    
    # Create and initialize chamber
    chamber = Chamber(pyramid_height=100.0)
    
    print("Initializing chamber...")
    if not chamber.initialize():
        print(f"❌ Initialization failed: {chamber.error_message}")
        sys.exit(1)
    
    print("✓ Chamber initialized")
    print()
    
    print("Calibrating synchronization engine...")
    if not chamber.calibrate():
        print(f"❌ Calibration failed: {chamber.error_message}")
        sys.exit(1)
    
    print("✓ Calibration complete")
    print()
    
    # Deploy some friend nodes
    print("Deploying friend nodes to OBI-WAN network...")
    node1 = chamber.deploy_friend_node("Tata")
    node2 = chamber.deploy_friend_node("JB")
    node3 = chamber.deploy_friend_node("Atlas")
    
    # Connect nodes (peer network)
    chamber.obiwan.connect_nodes(node1.node_id, node2.node_id)
    chamber.obiwan.connect_nodes(node2.node_id, node3.node_id)
    chamber.obiwan.connect_nodes(node3.node_id, node1.node_id)
    
    print(f"✓ Deployed {len(chamber.obiwan.nodes)} friend nodes")
    print()
    
    # Demonstrate aperture sensing
    print("Demonstrating aperture sensing (360° → 180°)...")
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        chamber.receive_from_field(angle, f"Data from {angle}°", source_id=f"sensor-{angle}")
    
    processed = chamber.process_chamber()
    print(f"✓ Received from 8 directions, processed {len(processed)} outputs")
    print()
    
    # Demonstrate synchronization
    print("Demonstrating organic ⚭ digital synchronization...")
    synced = chamber.synchronize_fields(organic_value=0.5, digital_value=0.5)
    print(f"✓ Synchronization: {synced and 'LOCKED' or 'ADJUSTING'}")
    print()
    
    # Display full status
    print(chamber.get_summary())
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
