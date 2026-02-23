import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import { TimeLatticeGrid } from './components/TimeLatticeGrid';
import { GalaxyField } from './components/GalaxyField';
import { CelestialBodies } from './components/CelestialBodies';
import { Constellations } from './components/Constellations';
import { Clock, Play, Pause } from 'lucide-react';
import { useTimeStore } from './store';
import './index.css';

function App() {
  const { currentDay, isPlaying, setDay, togglePlay } = useTimeStore();

  return (
    <div className="app-container">
      <div className="ui-hud">
        <h1 className="title">3D TEMPORAL LATTICE</h1>

        <div className="time-controls">
          <div className="scrub-container">
            <button className="play-btn" onClick={togglePlay}>
              {isPlaying ? <Pause size={18} /> : <Play size={18} />}
            </button>
            <input
              type="range"
              min="0"
              max="29.53"
              step="0.01"
              value={currentDay}
              onChange={(e) => setDay(parseFloat(e.target.value))}
              className="time-slider"
            />
          </div>
          <div className="day-display">
            Day {(currentDay).toFixed(2)}
          </div>
        </div>

        <div className="stat-panel">
          <div className="stat-row">
            <Clock size={16} /> <span>Lattice Period:</span> <span className="highlight">29.33 Days</span>
          </div>
          <div className="stat-row">
            <Clock size={16} /> <span>Moon Orbit:</span> <span className="highlight">29.53 Days</span>
          </div>
          <p className="description">
            Drag the slider to manually scrub through the phases and identify dimensional resonance patterns. Uses scroll to zoom out into deep space.
          </p>

          <div className="legend-panel">
            <div className="legend-title">Galaxy Data Index</div>
            <div className="legend-row">
              <div className="legend-dot" style={{ color: '#88ccff', backgroundColor: '#88ccff' }} />
              <span>Euclid General Survey</span>
            </div>
            <div className="legend-row">
              <div className="legend-dot" style={{ color: '#ff4444', backgroundColor: '#ff4444' }} />
              <span>JWST Early Universe</span>
            </div>
            <div className="legend-row">
              <div className="legend-dot" style={{ color: '#ffcc00', backgroundColor: '#ffcc00' }} />
              <span>Rubin Time-Domain Anomalies</span>
            </div>
          </div>
        </div>
      </div>

      <Canvas camera={{ position: [0, 80, 200], fov: 60 }} dpr={[1, 2]}>
        <color attach="background" args={['#02040a']} />
        <fog attach="fog" args={['#02040a', 100, 4000]} />

        <Suspense fallback={null}>
          <Stars radius={2500} depth={500} count={12000} factor={8} saturation={0} fade speed={1} />
          <Constellations />
          <TimeLatticeGrid />
          <GalaxyField />
          <CelestialBodies />
        </Suspense>

        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          maxDistance={4500}
          minDistance={20}
        />
      </Canvas>
    </div>
  );
}

export default App;
