import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useTimeStore } from '../store';

export function TimeLatticeGrid() {
    const gridRef = useRef<THREE.LineSegments>(null);

    const material = useMemo(() => new THREE.ShaderMaterial({
        uniforms: {
            time: { value: 0 },
            color: { value: new THREE.Color('#3366ff') },
            resonanceIntensity: { value: 0.0 },
            day: { value: 0.0 }
        },
        vertexShader: `
      uniform float time;
      uniform float day;
      varying vec3 vPosition;
      void main() {
        vPosition = position;
        float latticePhase = day * abs(1.0 / 29.33) * 100.0 + (position.x * 0.01 + position.z * 0.01);
        float yDistortion = sin(latticePhase) * 45.0;
        yDistortion += cos(latticePhase * 0.5) * 15.0;
        vec3 finalPos = position;
        finalPos.y += yDistortion;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(finalPos, 1.0);
      }
    `,
        fragmentShader: `
      uniform float time;
      uniform vec3 color;
      uniform float resonanceIntensity;
      varying vec3 vPosition;
      void main() {
        float distance = length(vPosition);
        float alpha = clamp(1.0 - (distance / 4500.0), 0.0, 1.0);
        float pulse = (sin(time * 2.0) * 0.5 + 0.5);
        vec3 finalColor = mix(color, vec3(1.0, 1.0, 1.0), resonanceIntensity * pulse);
        
        // Add a slight transparency gradient closer to Earth's core Origin point
        if(distance < 50.0) {
            alpha *= distance / 50.0;
        }
        
        gl_FragColor = vec4(finalColor, alpha * 0.4);
      }
    `,
        transparent: true,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
    }), []);

    useFrame((state) => {
        if (material) {
            const day = useTimeStore.getState().currentDay;
            material.uniforms.time.value = state.clock.getElapsedTime();

            const latticeDayFreq = 1.0 / 29.33;
            const moonDayFreq = 1.0 / 29.53;
            const beatFreq = Math.abs(latticeDayFreq - moonDayFreq);
            const beatPhase = Math.sin(day * beatFreq * Math.PI * 2 * 100.0);
            material.uniforms.resonanceIntensity.value = Math.max(0, beatPhase);

            material.uniforms.day.value = day;
        }
    });

    const geometry = useMemo(() => {
        const size = 1200;
        const divisions = 160;
        const geom = new THREE.BufferGeometry();
        const vertices = [];
        const step = size / divisions;
        const halfSize = size / 2;

        for (let i = 0; i <= divisions; i++) {
            vertices.push(-halfSize, 0, -halfSize + i * step);
            vertices.push(halfSize, 0, -halfSize + i * step);
            vertices.push(-halfSize + i * step, 0, -halfSize);
            vertices.push(-halfSize + i * step, 0, halfSize);
        }

        const layers = 5;
        const layerSpacing = 50;
        const allVertices = [];
        for (let l = -layers; l <= layers; l++) {
            for (let i = 0; i < vertices.length; i += 3) {
                allVertices.push(vertices[i], vertices[i + 1] + l * layerSpacing, vertices[i + 2]);
            }
        }

        geom.setAttribute('position', new THREE.Float32BufferAttribute(allVertices, 3));
        return geom;
    }, []);

    return (
        <lineSegments ref={gridRef} geometry={geometry} material={material} />
    );
}
