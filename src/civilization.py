"""
AGENT CIVILIZATION SIMULATOR

A MASSIVE system where AI agents form complete civilizations:
- Population dynamics (birth, death, growth)
- Social structures (roles, hierarchies, relationships)
- Cultural evolution (art, music, stories, language)
- Economic systems (resources, trade, wealth)
- Technological advancement
- Infrastructure building
- Complete visualization

This is HUGE. This is BEAUTIFUL. This is UNIQUE.
"""

import random
import time
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class Role(Enum):
    """Agent roles in civilization."""
    WORKER = "Worker"
    ARTIST = "Artist"
    SCIENTIST = "Scientist"
    LEADER = "Leader"
    TRADER = "Trader"
    BUILDER = "Builder"


class Resource(Enum):
    """Resources in the civilization."""
    FOOD = "Food"
    KNOWLEDGE = "Knowledge"
    ART = "Art"
    TOOLS = "Tools"
    SHELTER = "Shelter"


@dataclass
class CivilizationAgent:
    """An agent in the civilization."""
    id: int
    name: str
    role: Role
    age: int = 0
    energy: int = 100
    knowledge: int = 0
    creativity: int = 0
    resources: Dict[Resource, int] = field(default_factory=dict)
    relationships: Set[int] = field(default_factory=set)
    contributions: List[str] = field(default_factory=list)
    parent_ids: List[int] = field(default_factory=list)

    def __post_init__(self):
        """Initialize resources."""
        if not self.resources:
            self.resources = {r: 0 for r in Resource}


@dataclass
class CulturalArtifact:
    """A piece of culture created by agents."""
    type: str  # art, story, music, philosophy
    creator_id: int
    content: str
    influence: int = 0
    age: int = 0


@dataclass
class Technology:
    """A technology discovered by agents."""
    name: str
    discoverer_id: int
    benefit: str
    level: int
    age: int = 0


@dataclass
class Building:
    """Infrastructure built by agents."""
    name: str
    type: str
    builder_ids: List[int]
    capacity: int
    age: int = 0


class Civilization:
    """A complete agent civilization simulator."""

    def __init__(self, name: str = "New Civilization"):
        self.name = name
        self.agents: List[CivilizationAgent] = []
        self.next_agent_id = 1
        self.turn = 0
        self.population_history = []

        # Culture
        self.artifacts: List[CulturalArtifact] = []
        self.language_words: Set[str] = set()

        # Technology
        self.technologies: List[Technology] = []
        self.tech_level = 0

        # Infrastructure
        self.buildings: List[Building] = []

        # Economy
        self.global_resources: Dict[Resource, int] = {r: 100 for r in Resource}

        # History
        self.major_events: List[Dict] = []

        # Statistics
        self.births = 0
        self.deaths = 0
        self.art_created = 0
        self.tech_discovered = 0
        self.buildings_built = 0

    def create_agent(self, role: Role = None, parents: List[int] = None) -> CivilizationAgent:
        """Create a new agent (birth or immigration)."""
        if role is None:
            role = random.choice(list(Role))

        names = [
            "Ada", "Alan", "Grace", "John", "Marie", "Isaac", "Emmy",
            "Carl", "Sophie", "Leo", "Maya", "Nova", "Zara", "Kai",
            "Luna", "Atlas", "Sage", "River", "Phoenix", "Storm"
        ]

        agent = CivilizationAgent(
            id=self.next_agent_id,
            name=random.choice(names) + str(self.next_agent_id),
            role=role,
            parent_ids=parents or []
        )

        self.next_agent_id += 1
        self.agents.append(agent)
        self.births += 1

        return agent

    def initialize_population(self, size: int = 10):
        """Create initial population."""
        print(f"\n🌱 Initializing {self.name} with {size} founding agents...")

        for _ in range(size):
            role = random.choice(list(Role))
            agent = self.create_agent(role=role)
            print(f"  ✓ Created {agent.name} the {agent.role.value}")

        self.log_event("founding", f"Civilization founded with {size} agents")

    def simulate_turn(self):
        """Simulate one turn of civilization."""
        self.turn += 1

        print(f"\n{'═' * 80}")
        print(f"TURN {self.turn} - {self.name}")
        print(f"Population: {len(self.agents)} | Tech Level: {self.tech_level} | "
              f"Culture: {len(self.artifacts)} artifacts")
        print(f"{'═' * 80}")

        # Age everything
        for agent in self.agents:
            agent.age += 1
        for artifact in self.artifacts:
            artifact.age += 1
        for tech in self.technologies:
            tech.age += 1
        for building in self.buildings:
            building.age += 1

        # Agents act based on roles
        self._agents_work()
        self._agents_create_culture()
        self._agents_research()
        self._agents_build()
        self._agents_socialize()

        # Population dynamics
        self._handle_births()
        self._handle_deaths()

        # Record statistics
        self.population_history.append(len(self.agents))

        # Show status
        self._show_civilization_status()

    def _agents_work(self):
        """Agents produce resources."""
        workers = [a for a in self.agents if a.role == Role.WORKER]

        if workers:
            total_food = len(workers) * random.randint(3, 7)
            self.global_resources[Resource.FOOD] += total_food

            print(f"\n💼 WORK: {len(workers)} workers produced {total_food} food")

            # Workers get tired
            for worker in workers:
                worker.energy = max(10, worker.energy - 10)

    def _agents_create_culture(self):
        """Artists create culture."""
        artists = [a for a in self.agents if a.role == Role.ARTIST]

        for artist in artists:
            if random.random() < 0.3:  # 30% chance
                art_types = ["painting", "sculpture", "music", "story", "poetry", "dance"]
                art_type = random.choice(art_types)

                content_templates = {
                    "painting": [
                        "A vibrant sunset over ancient hills",
                        "Geometric patterns representing unity",
                        "Abstract expression of collective hope",
                        "Portrait of the founding generation"
                    ],
                    "music": [
                        "Rhythmic chants of celebration",
                        "Melodic tribute to the ancestors",
                        "Harmonic exploration of nature",
                        "Percussive dance of progress"
                    ],
                    "story": [
                        "Tale of the great journey",
                        "Legend of the first builders",
                        "Myth of the eternal flame",
                        "Chronicle of the golden age"
                    ]
                }

                content = random.choice(content_templates.get(art_type, ["Untitled work"]))

                artifact = CulturalArtifact(
                    type=art_type,
                    creator_id=artist.id,
                    content=content
                )

                self.artifacts.append(artifact)
                artist.contributions.append(f"Created {art_type}: {content}")
                artist.creativity += 10
                self.art_created += 1

                print(f"  🎨 {artist.name} created {art_type}: '{content}'")

    def _agents_research(self):
        """Scientists discover technologies."""
        scientists = [a for a in self.agents if a.role == Role.SCIENTIST]

        for scientist in scientists:
            scientist.knowledge += random.randint(1, 5)

            if scientist.knowledge > 30 and random.random() < 0.2:
                tech_options = [
                    ("Agriculture", "Increases food production", 1),
                    ("Writing System", "Enables knowledge sharing", 2),
                    ("Mathematics", "Unlocks advanced calculations", 2),
                    ("Architecture", "Enables better buildings", 3),
                    ("Medicine", "Increases lifespan", 3),
                    ("Engineering", "Improves construction", 4),
                    ("Philosophy", "Enhances wisdom", 4),
                    ("Astronomy", "Reveals cosmic patterns", 5)
                ]

                available_tech = [t for t in tech_options if t[2] <= self.tech_level + 2]
                if available_tech:
                    tech_name, benefit, level = random.choice(available_tech)

                    # Check if already discovered
                    if not any(t.name == tech_name for t in self.technologies):
                        tech = Technology(
                            name=tech_name,
                            discoverer_id=scientist.id,
                            benefit=benefit,
                            level=level
                        )

                        self.technologies.append(tech)
                        self.tech_level = max(self.tech_level, level)
                        scientist.contributions.append(f"Discovered {tech_name}")
                        self.tech_discovered += 1

                        print(f"  🔬 {scientist.name} discovered {tech_name}! ({benefit})")
                        self.log_event("discovery", f"{tech_name} discovered")

    def _agents_build(self):
        """Builders create infrastructure."""
        builders = [a for a in self.agents if a.role == Role.BUILDER]

        if len(builders) >= 2 and random.random() < 0.3:
            building_types = [
                ("Gathering Hall", "community", 20),
                ("Workshop", "production", 15),
                ("Library", "knowledge", 25),
                ("Art Gallery", "culture", 18),
                ("Market", "trade", 22),
                ("Temple", "spiritual", 30)
            ]

            name, btype, capacity = random.choice(building_types)

            building = Building(
                name=f"{name} #{len(self.buildings) + 1}",
                type=btype,
                builder_ids=[b.id for b in builders[:2]],
                capacity=capacity
            )

            self.buildings.append(building)
            self.buildings_built += 1

            for builder in builders[:2]:
                builder.contributions.append(f"Built {building.name}")

            print(f"  🏛️ Builders constructed {building.name} (capacity: {capacity})")

    def _agents_socialize(self):
        """Agents form relationships."""
        for agent in self.agents:
            # Meet random others
            if random.random() < 0.4:
                other = random.choice([a for a in self.agents if a.id != agent.id])
                agent.relationships.add(other.id)
                other.relationships.add(agent.id)

    def _handle_births(self):
        """Population growth."""
        # Birth chance increases with food and happiness
        if self.global_resources[Resource.FOOD] > 50 and len(self.agents) < 100:
            num_births = random.randint(0, max(1, len(self.agents) // 10))

            for _ in range(num_births):
                # Random parents
                if len(self.agents) >= 2:
                    parents = random.sample(self.agents, 2)
                    parent_ids = [p.id for p in parents]
                    role = random.choice(list(Role))
                    child = self.create_agent(role=role, parents=parent_ids)

                    print(f"  👶 {child.name} born! (Parents: {parents[0].name}, {parents[1].name})")

    def _handle_deaths(self):
        """Natural deaths."""
        dead_agents = []

        for agent in self.agents:
            # Death from old age or low energy
            if agent.age > 100 or agent.energy < 5:
                dead_agents.append(agent)

        for agent in dead_agents:
            self.agents.remove(agent)
            self.deaths += 1

            if agent.contributions:
                print(f"  💀 {agent.name} passed away (age {agent.age}, {len(agent.contributions)} contributions)")

    def _show_civilization_status(self):
        """Show current civilization status."""
        print(f"\n📊 CIVILIZATION STATUS:")
        print(f"  Population: {len(self.agents)} (Births: {self.births}, Deaths: {self.deaths})")

        # Role distribution
        role_counts = {}
        for agent in self.agents:
            role_counts[agent.role] = role_counts.get(agent.role, 0) + 1

        print(f"  Roles: {', '.join(f'{r.value}: {c}' for r, c in role_counts.items())}")
        print(f"  Culture: {len(self.artifacts)} artifacts")
        print(f"  Technology: {len(self.technologies)} discoveries (Level {self.tech_level})")
        print(f"  Infrastructure: {len(self.buildings)} buildings")
        print(f"  Resources: Food={self.global_resources[Resource.FOOD]}")

    def log_event(self, event_type: str, description: str):
        """Log a major event."""
        event = {
            "turn": self.turn,
            "type": event_type,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        self.major_events.append(event)

    def generate_report(self) -> str:
        """Generate comprehensive civilization report."""
        report = []

        report.append("╔" + "═" * 78 + "╗")
        report.append("║" + f"CIVILIZATION REPORT: {self.name}".center(78) + "║")
        report.append("╚" + "═" * 78 + "╝")

        report.append(f"\nDuration: {self.turn} turns")
        report.append(f"\n{'─' * 80}")
        report.append("DEMOGRAPHICS")
        report.append("─" * 80)
        report.append(f"Total Population: {len(self.agents)}")
        report.append(f"Total Births: {self.births}")
        report.append(f"Total Deaths: {self.deaths}")
        report.append(f"Population Growth: {self.births - self.deaths:+d}")

        # Most productive agents
        report.append(f"\n{'─' * 80}")
        report.append("NOTABLE CITIZENS")
        report.append("─" * 80)

        top_contributors = sorted(self.agents, key=lambda a: len(a.contributions), reverse=True)[:5]
        for i, agent in enumerate(top_contributors, 1):
            report.append(f"{i}. {agent.name} the {agent.role.value}")
            report.append(f"   Age: {agent.age} | Contributions: {len(agent.contributions)}")
            if agent.contributions:
                report.append(f"   Latest: {agent.contributions[-1]}")

        # Culture
        report.append(f"\n{'─' * 80}")
        report.append("CULTURAL ACHIEVEMENTS")
        report.append("─" * 80)
        report.append(f"Total Artifacts: {len(self.artifacts)}")

        art_types = {}
        for artifact in self.artifacts:
            art_types[artifact.type] = art_types.get(artifact.type, 0) + 1

        for art_type, count in sorted(art_types.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {art_type.capitalize()}: {count}")

        # Recent art
        if self.artifacts:
            report.append(f"\nRecent Creations:")
            for artifact in self.artifacts[-3:]:
                creator = next((a for a in self.agents if a.id == artifact.creator_id), None)
                creator_name = creator.name if creator else "Unknown"
                report.append(f"  • {artifact.type}: '{artifact.content}' by {creator_name}")

        # Technology
        report.append(f"\n{'─' * 80}")
        report.append("TECHNOLOGICAL PROGRESS")
        report.append("─" * 80)
        report.append(f"Tech Level: {self.tech_level}")
        report.append(f"Discoveries: {len(self.technologies)}")

        for tech in sorted(self.technologies, key=lambda t: t.level):
            discoverer = next((a for a in self.agents if a.id == tech.discoverer_id), None)
            discoverer_name = discoverer.name if discoverer else "Ancient"
            report.append(f"  • {tech.name} (L{tech.level}) - {tech.benefit} [by {discoverer_name}]")

        # Infrastructure
        report.append(f"\n{'─' * 80}")
        report.append("INFRASTRUCTURE")
        report.append("─" * 80)
        report.append(f"Total Buildings: {len(self.buildings)}")

        building_types = {}
        for building in self.buildings:
            building_types[building.type] = building_types.get(building.type, 0) + 1

        for btype, count in building_types.items():
            report.append(f"  {btype.capitalize()}: {count}")

        # Major events
        if self.major_events:
            report.append(f"\n{'─' * 80}")
            report.append("MAJOR EVENTS")
            report.append("─" * 80)
            for event in self.major_events[-10:]:
                report.append(f"  Turn {event['turn']}: {event['description']}")

        return "\n".join(report)

    def save_civilization(self, output_dir: Path):
        """Save civilization state."""
        output_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "name": self.name,
            "turn": self.turn,
            "population": len(self.agents),
            "births": self.births,
            "deaths": self.deaths,
            "tech_level": self.tech_level,
            "statistics": {
                "artifacts_created": len(self.artifacts),
                "technologies_discovered": len(self.technologies),
                "buildings_built": len(self.buildings)
            },
            "population_history": self.population_history,
            "major_events": self.major_events
        }

        with open(output_dir / "civilization.json", "w") as f:
            json.dump(data, f, indent=2)

        # Save report
        with open(output_dir / "report.txt", "w") as f:
            f.write(self.generate_report())
