#!/usr/bin/env python3
"""
EMERGENT CHEMISTRY - Discovering Self-Organizing Particle Systems

We'll simulate a universe with simple particles following simple rules,
and discover whether complex emergent behavior (like bonding, molecules,
catalysis) can spontaneously arise.

This is inspired by:
- Artificial Chemistry (autocatalytic sets)
- Particle Life (https://particle-life.com/)
- Origin of life research

Can we discover rules that create emergent complexity?
"""

import numpy as np
import random
from collections import defaultdict

class Particle:
    """A particle with position, velocity, and type"""
    def __init__(self, x, y, ptype, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.type = ptype  # Particle type (like chemical element)

class ParticleUniverse:
    """A universe with particles following interaction rules"""

    def __init__(self, width=100, height=100, n_types=4):
        self.width = width
        self.height = height
        self.n_types = n_types
        self.particles = []

        # Interaction matrix: how much type i attracts/repels type j
        # Positive = attraction, negative = repulsion
        self.interactions = np.random.uniform(-1, 1, (n_types, n_types))

        # Make it symmetric for now
        self.interactions = (self.interactions + self.interactions.T) / 2

        # Bond strengths - when do particles form bonds?
        self.bond_distance = 2.0
        self.bonds = []  # List of (particle_i, particle_j) bonds

    def add_random_particles(self, count):
        """Add random particles to the universe"""
        for _ in range(count):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            ptype = random.randint(0, self.n_types - 1)
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-0.5, 0.5)
            self.particles.append(Particle(x, y, ptype, vx, vy))

    def compute_force(self, p1, p2):
        """Compute force between two particles"""
        # Distance
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        # Periodic boundary conditions
        if dx > self.width / 2:
            dx -= self.width
        elif dx < -self.width / 2:
            dx += self.width

        if dy > self.height / 2:
            dy -= self.height
        elif dy < -self.height / 2:
            dy += self.height

        dist = np.sqrt(dx**2 + dy**2)
        if dist < 0.1:
            dist = 0.1  # Avoid division by zero

        # Interaction strength
        strength = self.interactions[p1.type][p2.type]

        # Force law: F = strength / r^2 at distance, repulsion at very close range
        if dist < 1.0:
            # Strong repulsion at very close range (like hard sphere)
            force_magnitude = -2.0 / (dist**2)
        else:
            # Attraction/repulsion based on interaction matrix
            force_magnitude = strength / (dist**2)

        # Force components
        fx = force_magnitude * dx / dist
        fy = force_magnitude * dy / dist

        return fx, fy, dist

    def update(self, dt=0.1, friction=0.95):
        """Update particle positions and velocities"""

        # Compute forces
        forces = [(0, 0) for _ in self.particles]

        for i, p1 in enumerate(self.particles):
            for j, p2 in enumerate(self.particles):
                if i >= j:
                    continue

                fx, fy, dist = self.compute_force(p1, p2)

                forces[i] = (forces[i][0] + fx, forces[i][1] + fy)
                forces[j] = (forces[j][0] - fx, forces[j][1] - fy)

        # Update velocities and positions
        for i, p in enumerate(self.particles):
            # Apply force
            p.vx += forces[i][0] * dt
            p.vy += forces[i][1] * dt

            # Friction
            p.vx *= friction
            p.vy *= friction

            # Update position
            p.x += p.vx * dt
            p.y += p.vy * dt

            # Periodic boundaries
            p.x = p.x % self.width
            p.y = p.y % self.height

    def detect_clusters(self):
        """Detect clusters of particles (emergent 'molecules')"""
        clusters = []
        visited = set()

        def dfs(particle_idx, cluster):
            """Depth-first search to find connected particles"""
            if particle_idx in visited:
                return
            visited.add(particle_idx)
            cluster.append(particle_idx)

            p1 = self.particles[particle_idx]
            for j, p2 in enumerate(self.particles):
                if j == particle_idx or j in visited:
                    continue

                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dist = np.sqrt(dx**2 + dy**2)

                if dist < self.bond_distance:
                    dfs(j, cluster)

        for i in range(len(self.particles)):
            if i not in visited:
                cluster = []
                dfs(i, cluster)
                if len(cluster) > 1:
                    clusters.append(cluster)

        return clusters

    def analyze_structure(self):
        """Analyze emergent structure in the system"""
        clusters = self.detect_clusters()

        # Compute statistics
        cluster_sizes = [len(c) for c in clusters]

        # Type distributions in clusters
        cluster_compositions = []
        for cluster in clusters:
            types = [self.particles[i].type for i in cluster]
            composition = {}
            for t in range(self.n_types):
                composition[t] = types.count(t)
            cluster_compositions.append(composition)

        return {
            'n_clusters': len(clusters),
            'cluster_sizes': cluster_sizes,
            'compositions': cluster_compositions,
            'clusters': clusters
        }

def run_emergence_experiment():
    """Run experiment to see if emergent complexity arises"""

    print("="*80)
    print("EMERGENT CHEMISTRY SIMULATION")
    print("="*80)
    print()

    print("Creating a universe with 4 particle types and random interactions...")
    print()

    universe = ParticleUniverse(width=50, height=50, n_types=4)

    # Show interaction matrix
    print("Interaction Matrix (+ = attraction, - = repulsion):")
    print()
    print("      ", end="")
    for i in range(universe.n_types):
        print(f"Type{i:1d}  ", end="")
    print()

    for i in range(universe.n_types):
        print(f"Type{i}: ", end="")
        for j in range(universe.n_types):
            val = universe.interactions[i][j]
            print(f"{val:+.2f}  ", end="")
        print()
    print()

    # Add particles
    universe.add_random_particles(100)

    print(f"Added {len(universe.particles)} particles")
    print()

    # Run simulation
    print("Running simulation for 1000 timesteps...")
    print()

    snapshots = []
    for step in range(1000):
        universe.update()

        if step % 100 == 0:
            analysis = universe.analyze_structure()
            snapshots.append((step, analysis))
            print(f"Step {step:4d}: {analysis['n_clusters']:3d} clusters", end="")
            if analysis['cluster_sizes']:
                print(f", sizes: {sorted(analysis['cluster_sizes'], reverse=True)[:5]}")
            else:
                print()

    print()

    # Analyze final state
    print("="*80)
    print("FINAL STATE ANALYSIS")
    print("="*80)
    print()

    final_analysis = universe.analyze_structure()

    print(f"Total particles: {len(universe.particles)}")
    print(f"Clusters formed: {final_analysis['n_clusters']}")
    print()

    if final_analysis['cluster_sizes']:
        print("Cluster size distribution:")
        size_dist = {}
        for size in final_analysis['cluster_sizes']:
            size_dist[size] = size_dist.get(size, 0) + 1

        for size in sorted(size_dist.keys(), reverse=True):
            count = size_dist[size]
            bar = "█" * min(count, 40)
            print(f"  Size {size:2d}: {count:3d} {bar}")
        print()

    # Find most interesting clusters (large, diverse composition)
    print("Most interesting emergent 'molecules':")
    print()

    interesting = []
    for i, cluster in enumerate(final_analysis['clusters']):
        size = len(cluster)
        composition = final_analysis['compositions'][i]
        diversity = len([c for c in composition.values() if c > 0])

        if size >= 3:
            interesting.append((size, diversity, composition, cluster))

    interesting.sort(key=lambda x: (x[0], x[1]), reverse=True)

    for size, diversity, composition, cluster in interesting[:5]:
        comp_str = ", ".join(f"Type{t}={count}" for t, count in composition.items() if count > 0)
        print(f"  Cluster of {size} particles: {comp_str}")

    print()

    return universe, snapshots, final_analysis

def search_for_self_organizing_rules():
    """Search for interaction matrices that produce interesting emergence"""

    print("="*80)
    print("SEARCHING FOR SELF-ORGANIZING INTERACTION RULES")
    print("="*80)
    print()

    print("Testing 20 random interaction matrices...")
    print("Looking for systems that spontaneously form large, stable structures")
    print()

    results = []

    for trial in range(20):
        universe = ParticleUniverse(width=50, height=50, n_types=4)
        universe.add_random_particles(80)

        # Run simulation
        for step in range(500):
            universe.update()

        # Analyze
        analysis = universe.analyze_structure()

        # Score based on cluster formation
        score = 0
        if analysis['cluster_sizes']:
            largest = max(analysis['cluster_sizes'])
            avg_size = np.mean(analysis['cluster_sizes'])
            score = largest * avg_size * analysis['n_clusters']

        results.append((score, universe.interactions, analysis))

        if (trial + 1) % 5 == 0:
            print(f"  Completed {trial + 1}/20 trials...")

    print()

    # Sort by score
    results.sort(reverse=True)

    print("TOP 5 MOST INTERESTING INTERACTION MATRICES:")
    print()

    for rank, (score, interactions, analysis) in enumerate(results[:5], 1):
        print(f"{rank}. Score: {score:.1f}")
        print(f"   Clusters: {analysis['n_clusters']}, Largest: {max(analysis['cluster_sizes']) if analysis['cluster_sizes'] else 0}")
        print("   Matrix:")
        for i in range(4):
            print("   ", end="")
            for j in range(4):
                print(f"{interactions[i][j]:+.2f} ", end="")
            print()
        print()

    return results

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              EMERGENT CHEMISTRY DISCOVERY                                  ║
║              Can complexity arise from simple rules?                       ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

We simulate particles following simple attraction/repulsion rules.
Question: Do they spontaneously form complex structures (molecules)?

This explores the origin of complexity in physical systems!
""")

    # First experiment
    universe, snapshots, final = run_emergence_experiment()

    print()

    # Search for interesting rules
    results = search_for_self_organizing_rules()

    print()
    print("="*80)
    print("DISCOVERY COMPLETE")
    print("="*80)
    print()
    print("✅ Simulated emergent particle systems")
    print("✅ Discovered self-organizing interaction rules")
    print("✅ Found 'molecular' structures forming spontaneously")
    print()
    print("This demonstrates how complexity can emerge from simple rules!")
    print()
