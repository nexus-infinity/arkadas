# arkadas
👑 ARKADAŞ - The King's Chamber | Organic ⚭ Digital Synchronization | 360° sensing → 180° focus | OBI-WAN Network | Friend intelligence at 1/3 pyramid height

## Overview

ARKADAŞ (Turkish for "friend") implements the King's Chamber system positioned at the optimal 1/3 height in pyramid geometry. It provides a framework for synchronizing organic (biological/human) and digital (computational/machine) systems through sacred geometric principles.

## Key Features

- **360° → 180° Aperture**: Convert omnidirectional awareness to focused attention
- **Organic ⚭ Digital Sync**: Bridge biological and computational domains
- **OBI-WAN Network**: Wide Area observation and intelligence network
- **Friend Network**: Distributed agent learning with trust relationships
- **Sacred Geometry**: Based on pyramid proportions and frequency resonance
- **Integration Layers**: Connect to external systems (Train Station, DOJO, Trident)

## Quick Start

### Installation

```bash
git clone https://github.com/nexus-infinity/arkadas.git
cd arkadas
pip install -r requirements.txt  # pytest, numpy
```

### Run the Demo

```bash
PYTHONPATH=. python examples/demo_integration.py
```

### Run Tests

```bash
python -m pytest tests/ -v
```

## Architecture

```
nexus-infinity/arkadas/
├── chamber/                 # Core synchronization logic
│   ├── aperture.py         # 360° → 180° conversion
│   ├── synchronizer.py     # Organic ⚭ Digital sync
│   └── light_axis.py       # Vertical energy flow
│
├── obi_wan/                # Observation network
│   ├── sensor_array.py     # 360° sensing
│   ├── metrics.py          # Measurement interface
│   ├── feedback.py         # Communication layer
│   └── wan_network.py      # Network coordination
│
├── friends/                # Friend intelligence network
│   ├── dal_friend.py       # DAL agent protocol
│   ├── trust_web.py        # Trust relationships
│   └── emergence.py        # Collective intelligence
│
├── geometry/               # Sacred geometry
│   ├── pyramid.py          # 1/3 height calculations
│   ├── aperture_math.py    # Angle transforms
│   └── resonance.py        # Frequency alignment
│
├── integration/            # External connections
│   ├── train_station.py    # Downward integration
│   ├── dojo.py            # Upward integration
│   ├── jefferies_tubes.py # Pulse sync channels
│   └── trident.py         # Validation system
│
├── config/                 # Configuration files
├── docs/                   # Documentation
├── examples/               # Usage examples
└── tests/                  # Test suite
```

## Usage Examples

### Basic Aperture Conversion

```python
from chamber.aperture import ApertureConverter

# Initialize aperture pointing north (0°)
aperture = ApertureConverter(focus_direction=0.0)

# 360° sensor data
sensor_data = {
    0.0: 1.0,
    90.0: 0.5,
    180.0: 0.2,
    270.0: 0.7
}

# Convert to 180° focused view
focused = aperture.convert(sensor_data)
intensity = aperture.calculate_intensity(focused)
```

### Organic-Digital Synchronization

```python
from chamber.synchronizer import OrganicDigitalSync

sync = OrganicDigitalSync(sync_frequency=1.0)

# Organic input (biometrics)
sync.sync_organic_input({
    'heart_rate': 72,
    'attention': 0.8
})

# Digital input (system metrics)
sync.sync_digital_input({
    'cpu_usage': 45,
    'attention': 0.75
})

# Check synchronization
if sync.is_synchronized():
    print(f"Coherence: {sync.get_coherence():.1%}")
```

### Friend Network

```python
from friends.dal_friend import DALFriend
from friends.trust_web import TrustWeb

# Create friends
alice = DALFriend("alice", capabilities=["sensing", "learning"])
bob = DALFriend("bob", capabilities=["processing"])

# Connect and share knowledge
alice.connect_friend(bob)
alice.share_knowledge("observation", {"target": "detected"})

# Establish trust
trust_web = TrustWeb()
trust_web.establish_trust("alice", "bob", initial_trust=0.7)
```

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture and design
- [OBI_WAN.md](docs/OBI_WAN.md) - Observation network details
- [SYNCHRONIZATION.md](docs/SYNCHRONIZATION.md) - Organic-digital sync process
- [SACRED_GEOMETRY.md](docs/SACRED_GEOMETRY.md) - Mathematical foundations

## Configuration

System behavior can be configured via YAML files in `config/`:

- `chamber_config.yaml` - Chamber parameters
- `frequency_map.yaml` - Chakra frequencies and harmonics
- `network_topology.yaml` - Friend network structure

## Testing

The project includes comprehensive tests:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_aperture.py -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## Key Concepts

### 1/3 Pyramid Height

The King's Chamber is positioned at 1/3 of the pyramid's height, a geometrically significant point where:
- Energy concentration is optimal
- Pressure/mass balance is achieved
- Harmonic resonance patterns converge

### 360° → 180° Aperture

Mirrors human attention:
- **360°**: Peripheral awareness (unconscious monitoring)
- **180°**: Focused attention (conscious processing)
- **Dynamic**: Adjustable focus direction

### Organic ⚭ Digital

Bridges two domains:
- **Organic**: Biological rhythms, intuition, consciousness
- **Digital**: Computational precision, speed, logic
- **Synchronization**: Coherent alignment between both

## Use Cases

- Meditation and biometric integration systems
- Multi-agent AI coordination with trust
- Distributed sensor networks
- Learning and skill development platforms
- Collective decision-making systems

## Contributing

Contributions are welcome! Please read the documentation and ensure all tests pass before submitting PRs.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

Based on sacred geometry principles found in ancient pyramid structures and modern consciousness research.
