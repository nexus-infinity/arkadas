#!/usr/bin/env python3
"""
ARKADAŠ King's Chamber Demo
============================

Demonstrates the core capabilities of the system:
- 360° to 180° aperture compression
- Organic ⚭ Digital synchronization
- OBI-WAN collective intelligence
"""

from aperture import Aperture, SensorReading, ApertureConfig
from synchronizer import Synchronizer, SynchronizerConfig
from obi_wan import ObiWanNetwork, SensorNode, SensorConfig, SensorType, CollectiveIntelligence


def demo_aperture():
    """Demonstrate aperture 360° → 180° compression."""
    print("=" * 70)
    print("🔷 APERTURE: 360° → 180° Compression Demo")
    print("=" * 70)
    
    # Create aperture with default config
    aperture = Aperture()
    
    # Create sensor readings around full circle
    readings = [
        SensorReading(angle=i * 30.0, intensity=0.5 + (i % 3) * 0.1)
        for i in range(12)
    ]
    
    print(f"\n📍 Input: {len(readings)} readings across 360°")
    for r in readings[:3]:
        print(f"   • Angle: {r.angle:6.1f}°, Intensity: {r.intensity:.2f}")
    print("   ...")
    
    # Compress to 180°
    focused = aperture.compress_readings(readings, resolution=10.0)
    
    print(f"\n🎯 Output: {len(focused)} focused readings in 180° space")
    for f in focused[:3]:
        print(f"   • Angle: {f.angle:6.1f}°, Intensity: {f.intensity:.2f}, " +
              f"Compressed from {len(f.original_angles)} readings")
    print("   ...")
    
    # Calculate efficiency
    efficiency = aperture.calculate_focal_efficiency(readings)
    
    # Get stats
    stats = aperture.get_compression_stats()
    
    print(f"\n📊 Statistics:")
    print(f"   • Compression ratio: {stats['compression_ratio']:.1f}x")
    print(f"   • Chamber ratio: {stats['chamber_ratio']:.3f}")
    print(f"   • Focal efficiency: {efficiency:.3f}")
    print(f"   • Mode: {stats['mode']}")
    

def demo_synchronizer():
    """Demonstrate organic ⚭ digital synchronization."""
    print("\n" + "=" * 70)
    print("⚭ SYNCHRONIZER: Organic ⚭ Digital Union Demo")
    print("=" * 70)
    
    # Create synchronizer
    sync = Synchronizer()
    
    print(f"\n🌿 Organic rhythm: {sync.config.organic_rate} Hz (human perception)")
    print(f"💻 Digital rhythm: {sync.config.digital_rate} Hz (computational)")
    print(f"🎵 Base frequency: {sync.config.base_frequency} Hz (Solfeggio)")
    print(f"👑 Chamber ratio: {sync.config.sync_ratio:.3f}")
    
    # Add organic pulses (simulating human perception rate)
    print(f"\n📥 Adding 10 organic pulses...")
    for i in range(10):
        sync.add_organic_pulse(value=float(i) * 0.1)
    
    # Add digital pulses (simulating computational rate)
    print(f"📥 Adding 100 digital pulses...")
    for i in range(100):
        sync.add_digital_pulse(value=float(i) * 0.01)
    
    # Synchronize
    unified = sync.synchronize()
    
    print(f"\n✨ Created {len(unified)} unified pulses")
    if unified:
        print(f"   • Sample unified value: {unified[0].value:.3f}")
        print(f"   • Frequency: {unified[0].frequency} Hz")
    
    # Get stats
    stats = sync.get_sync_stats()
    
    print(f"\n📊 Statistics:")
    print(f"   • Organic pulses: {stats['organic_count']}")
    print(f"   • Digital pulses: {stats['digital_count']}")
    print(f"   • Unified pulses: {stats['unified_count']}")
    print(f"   • Sync ratio: {stats['sync_ratio']:.3f}")
    print(f"   • Harmonic resonance: {stats['harmonic_resonance']:.3f}")


def demo_obi_wan():
    """Demonstrate OBI-WAN collective intelligence."""
    print("\n" + "=" * 70)
    print("🌐 OBI-WAN: Collective Intelligence Network Demo")
    print("=" * 70)
    
    # Create network
    network = ObiWanNetwork()
    
    print(f"\n🔸 Creating octagonal sensor network (8 nodes, 45° spacing)")
    
    # Create 8 sensor nodes in octagonal arrangement
    sensor_types = [
        SensorType.ELECTROMAGNETIC,
        SensorType.ACOUSTIC,
        SensorType.THERMAL,
        SensorType.ELECTROMAGNETIC,
        SensorType.ACOUSTIC,
        SensorType.THERMAL,
        SensorType.PROXIMITY,
        SensorType.PROXIMITY,
    ]
    
    for i in range(8):
        angle = i * 45.0  # 360° / 8 = 45°
        node = SensorNode(
            node_id=f"node_{i}",
            config=SensorConfig(sensor_type=sensor_types[i]),
            position=(angle, 0, 0)
        )
        network.register_node(node)
        
        # Generate some test readings
        node.sense(angle, 0.5 + i * 0.05)
    
    print(f"   ✓ Registered {len(network.nodes)} nodes")
    
    # Get network stats
    net_stats = network.get_network_stats()
    
    print(f"\n📊 Network Statistics:")
    print(f"   • Total nodes: {net_stats['total_nodes']}")
    print(f"   • Active nodes: {net_stats['active_nodes']}")
    print(f"   • Topology: {net_stats['topology']}")
    print(f"   • Total readings: {net_stats['total_readings']}")
    print(f"   • Sensor distribution:")
    for sensor_type, count in net_stats['sensor_distribution'].items():
        print(f"     - {sensor_type}: {count} nodes")
    
    # Create collective intelligence
    collective = CollectiveIntelligence(network)
    
    print(f"\n🧠 Generating collective insight...")
    insight = collective.generate_insight()
    
    if insight:
        print(f"   • Primary angle: {insight.angle:.1f}°")
        print(f"   • Intensity: {insight.intensity:.3f}")
        print(f"   • Confidence: {insight.confidence:.3f}")
        print(f"   • Sensor agreement: {insight.sensor_agreement:.3f}")
        print(f"   • Contributing sensors: {len(insight.contributing_sensors)}")
    
    # Get wisdom summary
    wisdom = collective.get_wisdom_summary()
    
    print(f"\n🌟 Wisdom Summary:")
    print(f"   • Total insights: {wisdom['total_insights']}")
    print(f"   • Average confidence: {wisdom['avg_confidence']:.3f}")
    print(f"   • Average agreement: {wisdom['avg_agreement']:.3f}")
    print(f"   • Coverage uniformity: {wisdom['coverage_analysis']['uniformity']:.3f}")


def main():
    """Run all demonstrations."""
    print("\n" + "🔺" * 35)
    print("👑 ARKADAŠ - The King's Chamber")
    print("Sacred Geometry at 1/3 Pyramid Height")
    print("🔺" * 35 + "\n")
    
    # Run demonstrations
    demo_aperture()
    demo_synchronizer()
    demo_obi_wan()
    
    print("\n" + "=" * 70)
    print("✅ All demonstrations completed successfully!")
    print("=" * 70)
    print("\n🎯 System operating at 1/3 height - where heaven and earth meet 👑\n")


if __name__ == "__main__":
    main()
