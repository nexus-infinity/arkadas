#!/usr/bin/env python
"""
Example demonstration of ARKADAŞ system integration.

This script shows how all components work together to create
an organic-digital synchronization system with 360° awareness.
"""

from chamber.aperture import ApertureConverter
from chamber.synchronizer import OrganicDigitalSync
from chamber.light_axis import LightAxis, FlowDirection

from obi_wan.sensor_array import SensorArray
from obi_wan.metrics import MetricsInterface
from obi_wan.feedback import FeedbackLayer, FeedbackType
from obi_wan.wan_network import WANCoordinator

from friends.dal_friend import DALFriend
from friends.trust_web import TrustWeb
from friends.emergence import CollectiveIntelligence

from geometry.pyramid import PyramidGeometry
from geometry.resonance import FrequencyResonance, Chakra

from integration.train_station import TrainStationInterface
from integration.dojo import DOJOInterface


def main():
    """Run comprehensive system demonstration."""
    
    print("=" * 70)
    print("ARKADAŞ - The King's Chamber System")
    print("Organic ⚭ Digital Synchronization at 1/3 Pyramid Height")
    print("=" * 70)
    print()
    
    # 1. Initialize Pyramid Geometry
    print("1. PYRAMID GEOMETRY")
    print("-" * 70)
    pyramid = PyramidGeometry(base_length=230.4, height=146.5)
    chamber_pos = pyramid.get_chamber_position()
    print(f"Chamber Height: {chamber_pos['height']:.2f} meters")
    print(f"Chamber Ratio: {chamber_pos['height_ratio']:.3f}")
    print(f"Cross-section Area: {chamber_pos['cross_section_area']:.2f} m²")
    print()
    
    # 2. Initialize Chamber Components
    print("2. CHAMBER INITIALIZATION")
    print("-" * 70)
    aperture = ApertureConverter(focus_direction=0.0)
    synchronizer = OrganicDigitalSync(sync_frequency=1.0)
    light_axis = LightAxis(chamber_height_ratio=1/3)
    print("✓ Aperture converter ready (360° → 180°)")
    print("✓ Synchronizer ready (Organic ⚭ Digital)")
    print("✓ Light axis ready (Peak ↔ Chamber)")
    print()
    
    # 3. Initialize OBI-WAN Network
    print("3. OBI-WAN NETWORK")
    print("-" * 70)
    sensor_array = SensorArray(num_sensors=36)
    metrics = MetricsInterface()
    feedback = FeedbackLayer()
    wan = WANCoordinator("ARKADAS_WAN")
    
    # Register some nodes
    wan.register_node("node_alpha", "sector_north")
    wan.register_node("node_beta", "sector_south")
    wan.register_node("node_gamma", "sector_east")
    wan.connect_nodes("node_alpha", "node_beta")
    wan.connect_nodes("node_beta", "node_gamma")
    
    status = wan.get_network_status()
    print(f"✓ Network '{status['network_name']}' online")
    print(f"  Nodes: {status['online_nodes']}/{status['total_nodes']}")
    print(f"  Connections: {status['total_connections']}")
    print()
    
    # 4. Demonstrate 360° Sensing → 180° Focus
    print("4. APERTURE TRANSFORMATION (360° → 180°)")
    print("-" * 70)
    sensor_readings = sensor_array.sense_360()
    print(f"✓ 360° sensor sweep complete: {len(sensor_readings)} readings")
    
    focused_data = aperture.convert(sensor_readings)
    intensity = aperture.calculate_intensity(focused_data)
    print(f"✓ Focused to 180° aperture: {len(focused_data)} data points")
    print(f"  Focus direction: {aperture.focus_direction}°")
    print(f"  Average intensity: {intensity:.3f}")
    print()
    
    # 5. Demonstrate Organic-Digital Synchronization
    print("5. ORGANIC ⚭ DIGITAL SYNCHRONIZATION")
    print("-" * 70)
    
    # Simulate organic input (biometrics)
    organic_data = {
        'heart_rate': 72,      # BPM
        'breath_rate': 16,     # breaths/min
        'attention': 0.8,      # focus level
        'arousal': 0.6         # alertness
    }
    synchronizer.sync_organic_input(organic_data)
    print("✓ Organic state synchronized")
    print(f"  Heart rate: {organic_data['heart_rate']} BPM")
    print(f"  Attention: {organic_data['attention']:.1%}")
    
    # Simulate digital input (system metrics)
    digital_data = {
        'cpu_usage': 45,       # percent
        'attention': 0.75,     # matching organic attention
        'processing': 0.9,     # computational load
        'latency': 12          # ms
    }
    synchronizer.sync_digital_input(digital_data)
    print("✓ Digital state synchronized")
    print(f"  CPU usage: {digital_data['cpu_usage']}%")
    print(f"  Processing: {digital_data['processing']:.1%}")
    
    coherence = synchronizer.get_coherence()
    is_synced = synchronizer.is_synchronized()
    print(f"✓ Coherence score: {coherence:.1%}")
    print(f"  Status: {'SYNCHRONIZED' if is_synced else 'ADJUSTING'}")
    print()
    
    # 6. Light Axis Energy Flow
    print("6. LIGHT AXIS ENERGY FLOW")
    print("-" * 70)
    light_axis.set_peak_energy(1.0)
    light_axis.set_chamber_energy(0.5)
    flow_state = light_axis.get_flow_state()
    print(f"✓ Peak energy: {flow_state['peak_energy']:.2f}")
    print(f"✓ Chamber energy: {flow_state['chamber_energy']:.2f}")
    print(f"  Flow direction: {flow_state['flow_direction']}")
    print(f"  Flow rate: {flow_state['flow_rate']:.2f}")
    print()
    
    # 7. Friend Network
    print("7. FRIEND NETWORK")
    print("-" * 70)
    
    # Create friends
    friend_alice = DALFriend("alice", capabilities=["sensing", "learning"])
    friend_bob = DALFriend("bob", capabilities=["processing", "communication"])
    friend_charlie = DALFriend("charlie", capabilities=["learning", "storage"])
    
    # Connect friends
    friend_alice.connect_friend(friend_bob)
    friend_bob.connect_friend(friend_charlie)
    
    # Share knowledge
    friend_alice.share_knowledge("observation", {"target": "detected", "confidence": 0.9})
    
    print(f"✓ Friend 'alice' created with {len(friend_alice.capabilities)} capabilities")
    print(f"✓ Friend 'bob' created with {len(friend_bob.capabilities)} capabilities")
    print(f"✓ Friend 'charlie' created with {len(friend_charlie.capabilities)} capabilities")
    print(f"  Knowledge shared: {len(friend_alice.shared_knowledge)} items")
    print()
    
    # 8. Trust Web
    print("8. TRUST WEB")
    print("-" * 70)
    trust_web = TrustWeb()
    trust_web.establish_trust("alice", "bob", initial_trust=0.7)
    trust_web.establish_trust("bob", "charlie", initial_trust=0.8)
    trust_web.establish_trust("alice", "charlie", initial_trust=0.6)
    
    alice_reputation = trust_web.get_reputation("alice")
    trusted_by_alice = trust_web.get_trusted_friends("alice", min_trust=0.6)
    
    print(f"✓ Trust relationships established")
    print(f"  Alice's reputation: {alice_reputation:.2f}")
    print(f"  Friends trusted by Alice: {len(trusted_by_alice)}")
    print()
    
    # 9. Collective Intelligence
    print("9. COLLECTIVE INTELLIGENCE")
    print("-" * 70)
    collective = CollectiveIntelligence()
    
    # Make collective decision
    votes = {
        "alice": "option_A",
        "bob": "option_A",
        "charlie": "option_B"
    }
    
    decision = collective.collective_decision(
        "Which direction to explore?",
        votes,
        weights={"alice": 0.7, "bob": 0.8, "charlie": 0.6}
    )
    
    print(f"✓ Collective decision made: {decision}")
    
    # Aggregate knowledge
    contributions = {"alice": 0.8, "bob": 0.9, "charlie": 0.7}
    aggregated = collective.aggregate_knowledge(contributions, "average")
    print(f"✓ Knowledge aggregated: {aggregated:.2f}")
    print()
    
    # 10. Frequency Resonance
    print("10. FREQUENCY RESONANCE")
    print("-" * 70)
    resonance = FrequencyResonance(base_frequency=432)
    
    # Align to heart chakra
    heart_alignment = resonance.align_to_chakra(Chakra.HEART)
    print(f"✓ Chakra: {heart_alignment['chakra']}")
    print(f"  Frequency: {heart_alignment['target_frequency']} Hz")
    print(f"  Color: {heart_alignment['color']}")
    print(f"  Aligned: {heart_alignment['aligned']}")
    print()
    
    # 11. Integration Layers
    print("11. INTEGRATION LAYERS")
    print("-" * 70)
    
    # Train Station (downward)
    train_station = TrainStationInterface()
    train_id = train_station.send_to_lower_layer(
        {"message": "Status update", "value": 42},
        priority="normal"
    )
    print(f"✓ Train Station: Dispatched train {train_id}")
    
    # DOJO (upward)
    dojo = DOJOInterface()
    dojo.register_skill("meditation", difficulty=5)
    dojo.start_training_session("chakra_alignment")
    dojo.practice_skill("meditation", quality=0.8)
    dojo_status = dojo.get_dojo_status()
    print(f"✓ DOJO: Training session active")
    print(f"  Mastery level: {dojo_status['mastery_level']:.1%}")
    print()
    
    # 12. Metrics Summary
    print("12. METRICS SUMMARY")
    print("-" * 70)
    metrics.record_metric("system_coherence", coherence)
    metrics.record_metric("light_axis_flow", flow_state['flow_rate'])
    metrics.record_metric("network_nodes", status['online_nodes'])
    
    summary = metrics.get_all_metrics()
    print(f"✓ Metrics tracked: {len(summary)}")
    for name, data in summary.items():
        print(f"  {name}: {data['current']:.3f}")
    print()
    
    # Final Status
    print("=" * 70)
    print("SYSTEM STATUS: OPERATIONAL")
    print("=" * 70)
    print(f"Chamber Position: 1/3 height ({chamber_pos['height']:.1f}m)")
    print(f"Synchronization: {'✓ SYNCHRONIZED' if is_synced else '⚠ ADJUSTING'}")
    print(f"Coherence: {coherence:.1%}")
    print(f"Network: {status['online_nodes']} nodes online")
    print(f"Friends: 3 active, {len(trust_web.friends)} in trust web")
    print("=" * 70)


if __name__ == "__main__":
    main()
