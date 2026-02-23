import React, { useMemo } from 'react';
import * as THREE from 'three';

// Procedurally generate some constellation lines that sit far back in the z-plane
export function Constellations() {
    const linesGeometry = useMemo(() => {
        const geometry = new THREE.BufferGeometry();
        const vertices: number[] = [];

        const numConstellations = 12;
        for (let c = 0; c < numConstellations; c++) {
            // Random center for constellation far away
            const cx = (Math.random() - 0.5) * 4000;
            const cy = (Math.random() - 0.5) * 2000;
            const cz = (Math.random() - 0.5) * 4000;

            // Push constellation to the outer shell but keep it visible
            const dir = new THREE.Vector3(cx, cy, cz).normalize();
            const dist = 1800 + Math.random() * 500;
            const center = dir.multiplyScalar(dist);

            const numStars = Math.floor(Math.random() * 5) + 4;
            const stars: THREE.Vector3[] = [];

            for (let i = 0; i < numStars; i++) {
                stars.push(new THREE.Vector3(
                    center.x + (Math.random() - 0.5) * 300,
                    center.y + (Math.random() - 0.5) * 300,
                    center.z + (Math.random() - 0.5) * 300
                ));
            }

            // Connect them in a path
            for (let i = 0; i < numStars - 1; i++) {
                vertices.push(stars[i].x, stars[i].y, stars[i].z);
                vertices.push(stars[i + 1].x, stars[i + 1].y, stars[i + 1].z);
            }
            // Randomly close the loop occasionally
            if (Math.random() > 0.5) {
                vertices.push(stars[numStars - 1].x, stars[numStars - 1].y, stars[numStars - 1].z);
                vertices.push(stars[0].x, stars[0].y, stars[0].z);
            }
        }

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        return geometry;
    }, []);

    return (
        <lineSegments geometry={linesGeometry}>
            <lineBasicMaterial color="#ffffff" transparent opacity={0.15} linewidth={1} />
        </lineSegments>
    );
}
