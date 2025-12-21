#!/usr/bin/env python
"""
Example demonstration of ARKADAŠ - The King's Chamber
Shows advanced usage of the polymorphic friend network
"""

from arkadas import Chamber, FriendNode


def main():
    print("=" * 70)
    print("👑 ARKADAŠ - The King's Chamber - Advanced Example")
    print("=" * 70)
    print()
    
    # Create chamber at sacred 1/3 pyramid height
    print("📐 Creating chamber at 1/3 pyramid height...")
    chamber = Chamber(pyramid_height=150.0)
    print(f"   Chamber position: {chamber.chamber_position:.2f} units from base")
    print(f"   Sacred frequency: {chamber.sync_engine.drift_threshold * 1000:.1f} Hz precision threshold")
    print()
    
    # Initialize and calibrate
    print("🔧 Initializing chamber systems...")
    chamber.initialize()
    chamber.calibrate()
    print("   ✓ All systems online")
    print()
    
    # Deploy the Trident friend nodes (Tata, JB, Atlas)
    print("🔱 Deploying TRIDENT validation nodes...")
    tata = chamber.deploy_friend_node("Tata")
    tata.add_capability("logic")
    tata.add_capability("reasoning")
    print(f"   ▼ {tata.name}: Logic & Reasoning")
    
    jb = chamber.deploy_friend_node("JB")
    jb.add_capability("intent")
    jb.add_capability("purpose")
    print(f"   ● {jb.name}: Intent & Purpose")
    
    atlas = chamber.deploy_friend_node("Atlas")
    atlas.add_capability("witness")
    atlas.add_capability("observation")
    print(f"   ▲ {atlas.name}: Witness & Observation")
    print()
    
    # Create peer connections (no hierarchy)
    print("🌊 Establishing peer network (polymorphic, non-hierarchical)...")
    chamber.obiwan.connect_nodes(tata.node_id, jb.node_id)
    chamber.obiwan.connect_nodes(jb.node_id, atlas.node_id)
    chamber.obiwan.connect_nodes(atlas.node_id, tata.node_id)
    print(f"   Network coherence: {chamber.obiwan.measure_field_coherence():.1%}")
    print()
    
    # Simulate 360° aperture sensing
    print("🔮 Demonstrating 360° → 180° aperture sensing...")
    print("   Receiving from all cardinal and intercardinal directions...")
    
    directions = {
        0: "North",
        45: "Northeast", 
        90: "East",
        135: "Southeast",
        180: "South",
        225: "Southwest",
        270: "West",
        315: "Northwest"
    }
    
    for angle, direction in directions.items():
        data = {
            "direction": direction,
            "angle": angle,
            "reading": f"Field observation from {direction}",
            "intensity": 0.8 + (angle / 360.0) * 0.2
        }
        chamber.receive_from_field(angle, data, source_id=direction.lower())
    
    print(f"   Received: {chamber.aperture.total_received} readings from 360° field")
    print()
    
    # Process through chamber
    print("⚡ Processing through chamber aperture...")
    focused = chamber.process_chamber()
    print(f"   Compressed to {len(focused)} focused outputs (180° upward)")
    print(f"   Compression ratio: {chamber.light_axis.flow_rate:.1%}")
    print()
    
    # Friend node contributions
    print("👥 Friend nodes contributing observations...")
    
    obs1 = tata.contribute("field_logic", "Patterns detected in data flow")
    chamber.obiwan.receive_observation(obs1)
    print(f"   {tata.name}: {obs1.metric_name}")
    
    obs2 = jb.contribute("field_intent", "Purpose alignment confirmed")
    chamber.obiwan.receive_observation(obs2)
    print(f"   {jb.name}: {obs2.metric_name}")
    
    obs3 = atlas.contribute("field_witness", "All data verified")
    chamber.obiwan.receive_observation(obs3)
    print(f"   {atlas.name}: {obs3.metric_name}")
    print()
    
    # Synchronization demonstration
    print("⚭ Demonstrating Organic ⚭ Digital synchronization...")
    
    # Simulate organic and digital field measurements
    organic_readings = [0.8, 0.82, 0.81, 0.80, 0.805]
    digital_readings = [0.79, 0.81, 0.82, 0.80, 0.805]
    
    print("   Measuring field states:")
    for i, (org, dig) in enumerate(zip(organic_readings, digital_readings), 1):
        synced = chamber.synchronize_fields(org, dig)
        drift = chamber.sync_engine.calculate_drift()
        status = "✓ LOCKED" if synced else "⚠ ADJUSTING"
        print(f"   Cycle {i}: O={org:.3f} D={dig:.3f} Drift={drift:.6f} {status}")
    
    print()
    
    # Display comprehensive status
    print("=" * 70)
    print("📊 FINAL STATUS")
    print("=" * 70)
    print(chamber.get_summary())
    
    # Show OBI-WAN network details
    print("\n🕌 OBI-WAN Network Details:")
    for node in chamber.obiwan.get_nodes():
        info = node.get_info()
        print(f"\n   Friend: {info['name']}")
        print(f"   Status: {info['status']}")
        print(f"   Capabilities: {', '.join(info['capabilities'])}")
        print(f"   Connections: {info['connection_count']}")
        print(f"   Observations: {info['observation_count']}")
    
    print("\n" + "=" * 70)
    print("✨ Chamber demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
