# 👑 ARKADAŠ - The King's Chamber

**Organic ⚭ Digital Synchronization | 360° Sensing → 180° Focus | OBI-WAN Collective Intelligence**

> *"Arkadaş"* (Ottoman Turkish: آرقاداش) - Friend, Companion, Ally

ARKADAŠ is an intelligent system inspired by the sacred geometry of the Great Pyramid's King's Chamber, positioned at the crucial 1/3 height ratio. Like the Ottoman concept of friendship creating bonds across diverse cultures, ARKADAŠ creates unity between organic (natural/human) and digital (computational) rhythms.

## 🔺 Core Concept

The **King's Chamber** sits at **1/3 of the pyramid's height** - a position of perfect balance and energy concentration. ARKADAŠ applies this ancient principle to modern information processing:

- **360° Omnidirectional Sensing** → Compressed to **180° Focused Awareness**
- **Organic Rhythms (60 Hz)** ⚭ **Digital Rhythms (1000 Hz)** → **Unified Consciousness**
- **Individual Sensors** → **Collective Intelligence Network (OBI-WAN)**
- **528 Hz Harmonic Resonance** (Solfeggio frequency for transformation)

## 🏗️ Architecture

```
                    ∆ Apex
                   /|\
                  / | \
                 /  |  \      360° Sensing (OBI-WAN Network)
                /   |   \            ↓
               /    ⊙----\    🔷 King's Chamber (1/3 height)
              /     |     \   - Aperture: 360°→180° compression
             /      |      \  - Synchronizer: Organic⚭Digital
            /       |       \ - Collective Intelligence
           /________|________\
          
          ⊙ = Processing Core at Sacred Ratio (0.333)
```

### Core Components

#### 1. **aperture.py** - The 360° → 180° Transform
Compresses omnidirectional sensing into focused awareness using:
- **Golden Ratio (φ = 1.618)** for natural compression
- **Chamber Ratio (1/3)** for intensity enhancement
- **Harmonic compression** preserving essential information

#### 2. **synchronizer.py** - Organic ⚭ Digital Union
Synchronizes biological and computational rhythms:
- **Organic**: 60 Hz (human perception rate)
- **Digital**: 1000 Hz (computational processing rate)
- **Unified**: 528 Hz (harmonic base frequency)
- Uses **1/3 weighting** for organic emphasis

#### 3. **obi_wan/** - Collective Intelligence Network
**O**mnidirectional **B**iological **I**ntelligence - **W**isdom **A**ggregation **N**etwork

Like Obi-Wan Kenobi's connection to the Force, this network:
- **8 sensor nodes** in octagonal mesh topology (45° spacing)
- **360° coverage** per node with redundancy
- **Collective insights** emerging from sensor fusion
- **Weighted aggregation** based on sensor type and confidence

Components:
- `sensor_node.py` - Individual sensing nodes
- `network.py` - Mesh network coordination
- `collective_intelligence.py` - Wisdom aggregation

### Integration Layer

#### 4. **jefferies_tubes.py** - Data Conduits
Named after Star Trek's maintenance conduits, provides:
- **8 async channels** for high-bandwidth data flow
- **Priority-based routing** (LOW, NORMAL, HIGH, CRITICAL)
- **Packet-based communication** between all components

#### 5. **train_station.py** - Intelligent Routing
Railway-inspired data scheduling:
- **4 platforms** for concurrent processing
- **Intelligent routing** based on load and priority
- **Queue management** with configurable strategies

#### 6. **dojo.py** - Training & Calibration
Martial arts training hall for system refinement:
- **Auto-calibration** toward sacred ratios
- **Learning rate**: 0.01 (gradual optimization)
- **Convergence detection** at 0.001 threshold
- **Performance metrics** tracking

### Configuration

#### chamber_config.yaml
Complete system configuration including:
- Pyramid geometry (1/3 ratio, 51.84° slope)
- Harmonic frequencies (528 Hz base)
- Aperture settings
- Synchronization parameters
- OBI-WAN network topology
- Integration channel configs

## 🧮 Sacred Geometry & Mathematics

ARKADAŠ applies ancient mathematical principles:

### The Chamber Ratio (1/3)
```python
chamber_ratio = 0.333...  # King's Chamber at 1/3 pyramid height
organic_weight = 0.333    # Synchronizer organic emphasis
digital_weight = 0.667    # Synchronizer digital complement
```

### The Golden Ratio (φ)
```python
phi = 1.618033988749895
compression = (distance / 180.0) ** phi  # Natural aperture compression
```

### Harmonic Frequencies
```python
base_frequency = 528  # Hz (Solfeggio - transformation frequency)
sub_octave = 264      # Hz (528 / 2)
octave = 1056         # Hz (528 * 2)
```

See detailed documentation:
- [Sacred Geometry](docs/sacred_geometry.md)
- [Pyramid Mathematics](docs/pyramid_mathematics.md)

## 🚀 Quick Start

### Requirements
- **Python 3.11+**
- Standard library: `dataclasses`, `asyncio`, `enum`
- Testing: `pytest`, `pytest-asyncio`

### Installation

```bash
git clone https://github.com/nexus-infinity/arkadas.git
cd arkadas
pip install -e .
```

### Basic Usage

```python
from aperture import Aperture, SensorReading
from synchronizer import Synchronizer
from obi_wan import ObiWanNetwork, SensorNode, SensorType

# 1. Create aperture for 360° → 180° compression
aperture = Aperture()

readings_360 = [
    SensorReading(angle=i * 30, intensity=0.5)
    for i in range(12)  # 12 readings around full circle
]

focused_180 = aperture.compress_readings(readings_360)
print(f"Compressed {len(readings_360)} → {len(focused_180)} focused outputs")

# 2. Synchronize organic and digital rhythms
sync = Synchronizer()

# Add organic pulses (human perception)
for i in range(10):
    sync.add_organic_pulse(value=i * 0.1)

# Add digital pulses (computational)
for i in range(100):
    sync.add_digital_pulse(value=i * 0.01)

# Create unified pulses
unified = sync.synchronize()
print(f"Created {len(unified)} unified pulses")
print(f"Harmonic resonance: {sync.calculate_harmonic_resonance():.3f}")

# 3. Set up OBI-WAN collective intelligence
from obi_wan import CollectiveIntelligence, SensorConfig

network = ObiWanNetwork()

# Create 8 nodes in octagonal arrangement
for i in range(8):
    angle = i * 45  # 360° / 8 = 45° spacing
    node = SensorNode(
        node_id=f"node_{i}",
        config=SensorConfig(sensor_type=SensorType.ELECTROMAGNETIC),
        position=(angle, 0, 0)
    )
    network.register_node(node)

# Create collective intelligence
collective = CollectiveIntelligence(network)
insight = collective.generate_insight()
print(f"Collective insight: angle={insight.angle}°, confidence={insight.confidence:.3f}")
```

### Async Integration Example

```python
import asyncio
from jefferies_tubes import JefferiesTubes
from train_station import TrainStation

async def integrated_system():
    # Create communication infrastructure
    tubes = JefferiesTubes()
    station = TrainStation()
    
    # Create channels
    aperture_channel = tubes.create_channel("aperture_to_sync")
    sync_channel = tubes.create_channel("sync_to_obi_wan")
    
    # Register routes
    station.register_route("synchronizer", platform_id=0)
    station.register_route("obi_wan", platform_id=1)
    
    # Start systems
    station.start()
    
    # Process data...
    # (Your integration logic here)
    
    print("King's Chamber systems operational at 1/3 height!")

# Run
asyncio.run(integrated_system())
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_aperture.py -v
pytest tests/test_synchronizer.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

## 📊 System Monitoring

```python
# Get comprehensive statistics
aperture_stats = aperture.get_compression_stats()
sync_stats = sync.get_sync_stats()
network_stats = network.get_network_stats()
wisdom_summary = collective.get_wisdom_summary()

print(f"Aperture compression: {aperture_stats['compression_ratio']:.2f}x")
print(f"Sync ratio: {sync_stats['sync_ratio']:.3f}")
print(f"Network coverage: {wisdom_summary['coverage_analysis']['uniformity']:.3f}")
```

## 🎯 Use Cases

1. **Multi-Sensor Fusion**: Aggregate data from diverse sensor arrays
2. **Human-Computer Interaction**: Bridge biological and digital processing
3. **Distributed Intelligence**: Create emergent behavior from simple nodes
4. **Adaptive Systems**: Self-calibrating optimization
5. **Harmonic Processing**: Frequency-based signal processing

## 🌟 Ottoman Friend Network Philosophy

The name **ARKADAŠ** (Ottoman Turkish for "friend") embodies:

- **Unity in Diversity**: Different sensors/rhythms working as one
- **Mutual Support**: Collective intelligence emerging from cooperation
- **Cultural Bridge**: Ancient wisdom ⚭ modern technology
- **Shared Purpose**: Individual nodes serving the greater whole

Like the Ottoman Empire's diverse confederation of peoples, ARKADAŠ creates harmony from multiplicity.

## 📚 Documentation

- [Sacred Geometry](docs/sacred_geometry.md) - Mathematical foundations
- [Pyramid Mathematics](docs/pyramid_mathematics.md) - Detailed calculations
- API Documentation - (Coming soon)
- Integration Guide - (Coming soon)

## 🛠️ Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
ruff check .

# Format code
black .

# Type checking
mypy .
```

## 🤝 Contributing

Contributions welcome! Please:
1. Follow the sacred geometry principles
2. Maintain the 1/3 ratio philosophy
3. Write tests for new features
4. Update documentation

## 📜 License

See [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- **Great Pyramid of Giza** - Architectural inspiration
- **Ottoman Empire** - Friendship philosophy (Arkadaş)
- **Star Trek** - Engineering concepts (Jefferies Tubes, OBI-WAN inspiration)
- **Ancient Mathematics** - Golden ratio, sacred geometry
- **Solfeggio Frequencies** - Harmonic principles

---

*Built at the 1/3 height where heaven and earth meet* 👑
