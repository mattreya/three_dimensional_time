import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Sphere } from '@react-three/drei';
import { useTimeStore } from '../store';

export function CelestialBodies() {
    const moonRef = useRef<THREE.Group>(null);
    const flashMaterialRef = useRef<THREE.MeshBasicMaterial>(null);

    const tetherMaterial = useMemo(() => new THREE.ShaderMaterial({
        uniforms: {
            time: { value: 0 },
            resonance: { value: 0 }
        },
        vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
        fragmentShader: `
      uniform float time;
      uniform float resonance;
      varying vec2 vUv;
      void main() {
        float falloff = 1.0 - vUv.y;
        float glow = sin(time * 10.0 - vUv.y * 20.0) * 0.5 + 0.5;
        vec3 col = mix(vec3(0.2, 0.5, 1.0), vec3(1.0, 1.0, 0.5), resonance);
        gl_FragColor = vec4(col, falloff * glow * resonance * 0.8);
      }
    `,
        transparent: true,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
        side: THREE.DoubleSide
    }), []);

    useFrame((state, delta) => {
        let day = useTimeStore.getState().currentDay;
        if (useTimeStore.getState().isPlaying) {
            day = (day + delta * 2) % 29.53; // Arbitrary speed up
            useTimeStore.getState().setDay(day);
        }

        // Moon orbit syncs to exactly 29.53 days per cycle
        const angle = (day / 29.53) * 2 * Math.PI;
        const distance = 40;

        if (moonRef.current) {
            moonRef.current.position.set(distance * Math.cos(angle), 0, distance * Math.sin(angle));
            moonRef.current.rotation.y += 0.01;
        }

        // Mathematical definition
        const latticeDayFreq = 1.0 / 29.33;
        const moonDayFreq = 1.0 / 29.53;
        const beatFreq = Math.abs(latticeDayFreq - moonDayFreq);
        const beatPhase = Math.sin(day * beatFreq * Math.PI * 2 * 100.0);
        const resonance = Math.max(0, Math.pow(beatPhase, 10));

        if (tetherMaterial) {
            tetherMaterial.uniforms.time.value = state.clock.getElapsedTime();
            tetherMaterial.uniforms.resonance.value = resonance;
        }

        if (flashMaterialRef.current) {
            flashMaterialRef.current.opacity = resonance * 0.4;
        }
    });

    return (
        <>
            <Sphere args={[10, 32, 32]} position={[0, 0, 0]}>
                <meshStandardMaterial color="#113355" emissive="#002244" emissiveIntensity={0.2} wireframe={true} />
            </Sphere>

            <Sphere args={[12, 32, 32]} position={[0, 0, 0]}>
                <meshBasicMaterial ref={flashMaterialRef} color="#ffffff" transparent={true} opacity={0} blending={THREE.AdditiveBlending} depthWrite={false} />
            </Sphere>

            <group ref={moonRef}>
                <Sphere args={[2, 16, 16]} position={[0, 0, 0]}>
                    <meshStandardMaterial color="#dddddd" />
                </Sphere>
                <mesh position={[0, 0, -20]} rotation={[-Math.PI / 2, 0, 0]}>
                    <cylinderGeometry args={[0.2, 2, 40, 16, 1, true]} />
                    <primitive object={tetherMaterial} attach="material" />
                </mesh>
            </group>

            <ambientLight intensity={0.5} />
            <pointLight position={[100, 100, 100]} intensity={2.0} color="#ffeedd" />
            <pointLight position={[-100, -100, -100]} intensity={0.5} color="#44aaff" />
        </>
    );
}
