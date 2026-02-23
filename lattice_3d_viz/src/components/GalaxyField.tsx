import React, { useMemo, useRef, useEffect, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface GalaxyData {
    x: number;
    y: number;
    z: number;
    color: string;
    size: number;
}

export function GalaxyField() {
    const [galaxies, setGalaxies] = useState<GalaxyData[]>([]);
    const meshRef = useRef<THREE.InstancedMesh>(null);

    useEffect(() => {
        fetch('/galaxies.json')
            .then(res => res.json())
            .then(data => setGalaxies(data))
            .catch(err => console.error("Error loading galaxies", err));
    }, []);

    const dummy = useMemo(() => new THREE.Object3D(), []);

    const colorArray = useMemo(() => {
        if (galaxies.length === 0) return new Float32Array(0);
        const array = new Float32Array(galaxies.length * 3);
        const tempColor = new THREE.Color();
        galaxies.forEach((g, i) => {
            tempColor.set(g.color);
            array[i * 3] = tempColor.r;
            array[i * 3 + 1] = tempColor.g;
            array[i * 3 + 2] = tempColor.b;
        });
        return array;
    }, [galaxies]);

    useEffect(() => {
        if (meshRef.current && galaxies.length > 0) {
            galaxies.forEach((g, i) => {
                dummy.position.set(g.x, g.y, g.z);
                dummy.scale.set(g.size, g.size, g.size);
                dummy.updateMatrix();
                meshRef.current!.setMatrixAt(i, dummy.matrix);
            });
            meshRef.current.instanceMatrix.needsUpdate = true;
            if (meshRef.current.geometry.attributes.color) {
                meshRef.current.geometry.attributes.color.needsUpdate = true;
            }
        }
    }, [galaxies, dummy]);

    useFrame(({ clock }) => {
        if (meshRef.current) {
            meshRef.current.rotation.y = clock.getElapsedTime() * 0.005;
            meshRef.current.rotation.z = clock.getElapsedTime() * 0.002;
        }
    });

    if (galaxies.length === 0) return null;

    return (
        <instancedMesh ref={meshRef} args={[undefined, undefined, galaxies.length]}>
            <sphereGeometry args={[1, 16, 16]}>
                <instancedBufferAttribute attach="attributes-color" args={[colorArray, 3]} />
            </sphereGeometry>
            <meshBasicMaterial toneMapped={false} vertexColors={true} />
        </instancedMesh>
    );
}
