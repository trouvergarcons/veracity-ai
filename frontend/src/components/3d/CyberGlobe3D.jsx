'use client';

import React, { useEffect, useRef } from 'react';

/**
 * CyberGlobe3D
 * High-performance, zero-dependency interactive 3D Web Canvas model.
 * Renders an interactive 3D Holographic Wireframe Cyber Sphere with:
 * - 3D Perspective Projection & depth sorting
 * - Rotating orbital data rings with glowing cyber satellites
 * - Core geodesic icosahedron wireframe
 * - Ambient 3D floating particle constellation
 * - Smooth mouse parallax tracking
 */
export default function CyberGlobe3D({ className = '', opacity = 0.45 }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId;
    let width = (canvas.width = canvas.parentElement?.clientWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.clientHeight || window.innerHeight);

    // Camera & 3D Settings
    const fov = 400;
    let rotX = 0.2;
    let rotY = 0;
    let rotZ = 0;
    let targetRotX = 0.2;
    let targetRotY = 0;

    // Mouse Tracking
    let mouseX = 0;
    let mouseY = 0;
    const handleMouseMove = (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = (e.clientX - rect.left) / width - 0.5;
      const y = (e.clientY - rect.top) / height - 0.5;
      targetRotY = x * 1.5;
      targetRotX = -y * 1.5;
    };
    window.addEventListener('mousemove', handleMouseMove);

    // Resize Handler
    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = canvas.parentElement?.clientWidth || window.innerWidth;
      height = canvas.height = canvas.parentElement?.clientHeight || window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    // Generate 3D Vertices for a Geodesic Sphere
    const sphereRadius = Math.min(width, height) * 0.28;
    const spherePoints = [];
    const rings = 12;
    const segments = 24;

    for (let i = 0; i <= rings; i++) {
      const theta = (i * Math.PI) / rings;
      const sinTheta = Math.sin(theta);
      const cosTheta = Math.cos(theta);

      for (let j = 0; j < segments; j++) {
        const phi = (j * 2 * Math.PI) / segments;
        const x = sphereRadius * sinTheta * Math.cos(phi);
        const y = sphereRadius * cosTheta;
        const z = sphereRadius * sinTheta * Math.sin(phi);
        spherePoints.push({ x, y, z, ring: i, seg: j });
      }
    }

    // Floating 3D ambient data particles
    const particleCount = 70;
    const ambientParticles = [];
    for (let i = 0; i < particleCount; i++) {
      const rad = sphereRadius * (1.1 + Math.random() * 0.8);
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = Math.cbrt(Math.random()) * rad;
      const sinPhi = Math.sin(phi);
      ambientParticles.push({
        x: r * sinPhi * Math.cos(theta),
        y: r * sinPhi * Math.sin(theta),
        z: r * Math.cos(phi),
        size: Math.random() * 2 + 0.8,
        speed: (Math.random() - 0.5) * 0.005,
        pulse: Math.random() * Math.PI
      });
    }

    // Orbiting 3D Cyber Rings
    const orbitalRings = [
      { radius: sphereRadius * 1.35, tiltX: 0.6, tiltY: 0.3, speed: 0.015, points: 36, color: 'rgba(45, 212, 191, ' },
      { radius: sphereRadius * 1.55, tiltX: -0.4, tiltY: 0.8, speed: -0.012, points: 40, color: 'rgba(56, 189, 248, ' },
      { radius: sphereRadius * 1.15, tiltX: 1.1, tiltY: -0.5, speed: 0.02, points: 30, color: 'rgba(168, 85, 247, ' }
    ];

    let lastTime = performance.now();

    // 3D Rotation Math
    const rotatePoint = (p, rx, ry, rz) => {
      // Rotate around X
      let y1 = p.y * Math.cos(rx) - p.z * Math.sin(rx);
      let z1 = p.y * Math.sin(rx) + p.z * Math.cos(rx);

      // Rotate around Y
      let x2 = p.x * Math.cos(ry) + z1 * Math.sin(ry);
      let z2 = -p.x * Math.sin(ry) + z1 * Math.cos(ry);

      // Rotate around Z
      let x3 = x2 * Math.cos(rz) - y1 * Math.sin(rz);
      let y3 = x2 * Math.sin(rz) + y1 * Math.cos(rz);

      return { x: x3, y: y3, z: z2 };
    };

    // Main 3D Render Loop
    const render = (time) => {
      const dt = (time - lastTime) * 0.001;
      lastTime = time;

      // Smooth inertia rotation
      rotX += (targetRotX - rotX) * 0.05 + 0.002;
      rotY += (targetRotY - rotY) * 0.05 + 0.004;
      rotZ += 0.001;

      ctx.clearRect(0, 0, width, height);

      const centerX = width * 0.68; // Place gracefully towards center-right for dashboard balance
      const centerY = height * 0.48;

      // 1. Draw glowing ambient background radial energy
      const ambientGlow = ctx.createRadialGradient(centerX, centerY, 10, centerX, centerY, sphereRadius * 1.8);
      ambientGlow.addColorStop(0, 'rgba(20, 184, 166, 0.12)');
      ambientGlow.addColorStop(0.4, 'rgba(56, 189, 248, 0.06)');
      ambientGlow.addColorStop(0.8, 'rgba(139, 92, 246, 0.02)');
      ambientGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = ambientGlow;
      ctx.fillRect(0, 0, width, height);

      // 2. Project & Render Ambient Floating 3D Particles
      ctx.fillStyle = '#38bdf8';
      for (let i = 0; i < ambientParticles.length; i++) {
        const pt = ambientParticles[i];
        pt.pulse += 0.03;
        const rotated = rotatePoint(pt, rotX * 0.7, rotY * 0.7, rotZ * 0.5);
        const zDist = fov + rotated.z;
        if (zDist > 10) {
          const scale = fov / zDist;
          const px = centerX + rotated.x * scale;
          const py = centerY + rotated.y * scale;
          const alpha = Math.max(0.05, Math.min(0.8, (rotated.z + sphereRadius) / (sphereRadius * 2))) * (0.6 + 0.4 * Math.sin(pt.pulse));

          ctx.beginPath();
          ctx.arc(px, py, Math.max(0.5, pt.size * scale), 0, Math.PI * 2);
          ctx.fillStyle = i % 2 === 0 ? `rgba(45, 212, 191, ${alpha * 0.8})` : `rgba(168, 85, 247, ${alpha * 0.8})`;
          ctx.fill();
        }
      }

      // 3. Project & Draw Sphere Wireframe
      const projectedSphere = [];
      for (let i = 0; i < spherePoints.length; i++) {
        const pt = spherePoints[i];
        const rot = rotatePoint(pt, rotX, rotY, rotZ);
        const zDist = fov + rot.z;
        if (zDist > 10) {
          const scale = fov / zDist;
          const px = centerX + rot.x * scale;
          const py = centerY + rot.y * scale;
          const depthAlpha = Math.max(0.04, Math.min(0.7, (rot.z + sphereRadius) / (sphereRadius * 2)));
          projectedSphere.push({ px, py, z: rot.z, alpha: depthAlpha, ring: pt.ring, seg: pt.seg });
        }
      }

      // Draw latitude lines
      ctx.lineWidth = 1;
      for (let i = 1; i < rings; i++) {
        const ringPts = projectedSphere.filter(p => p.ring === i);
        if (ringPts.length > 2) {
          ctx.beginPath();
          ctx.moveTo(ringPts[0].px, ringPts[0].py);
          for (let j = 1; j < ringPts.length; j++) {
            ctx.lineTo(ringPts[j].px, ringPts[j].py);
          }
          ctx.closePath();
          const avgZ = ringPts.reduce((acc, p) => acc + p.z, 0) / ringPts.length;
          const alpha = Math.max(0.03, Math.min(0.35, (avgZ + sphereRadius) / (sphereRadius * 2)));
          ctx.strokeStyle = `rgba(45, 212, 191, ${alpha * 0.4})`;
          ctx.stroke();
        }
      }

      // Draw longitude arcs
      for (let j = 0; j < segments; j += 2) {
        const segPts = projectedSphere.filter(p => p.seg === j).sort((a, b) => a.ring - b.ring);
        if (segPts.length > 2) {
          ctx.beginPath();
          ctx.moveTo(segPts[0].px, segPts[0].py);
          for (let k = 1; k < segPts.length; k++) {
            ctx.lineTo(segPts[k].px, segPts[k].py);
          }
          const avgZ = segPts.reduce((acc, p) => acc + p.z, 0) / segPts.length;
          const alpha = Math.max(0.03, Math.min(0.4, (avgZ + sphereRadius) / (sphereRadius * 2)));
          ctx.strokeStyle = `rgba(56, 189, 248, ${alpha * 0.35})`;
          ctx.stroke();
        }
      }

      // 4. Draw Core Interconnected Data Nodes
      const sampleStep = 4;
      for (let i = 0; i < projectedSphere.length; i += sampleStep) {
        const node = projectedSphere[i];
        if (node.z > 0) {
          ctx.beginPath();
          ctx.arc(node.px, node.py, 1.8, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(45, 212, 191, ${node.alpha * 0.9})`;
          ctx.fill();

          // Connect nearby visible nodes
          for (let j = i + sampleStep; j < Math.min(i + sampleStep * 3, projectedSphere.length); j += sampleStep) {
            const nextNode = projectedSphere[j];
            const dist = Math.hypot(node.px - nextNode.px, node.py - nextNode.py);
            if (dist < 48) {
              ctx.beginPath();
              ctx.moveTo(node.px, node.py);
              ctx.lineTo(nextNode.px, nextNode.py);
              ctx.strokeStyle = `rgba(56, 189, 248, ${node.alpha * 0.25})`;
              ctx.stroke();
            }
          }
        }
      }

      // 5. Draw 3D Orbital Rings & Glowing Satellites
      orbitalRings.forEach((ring, idx) => {
        ring.tiltX += ring.speed * 0.3;
        ring.tiltY += ring.speed;

        const ringPoints = [];
        for (let a = 0; a < ring.points; a++) {
          const angle = (a * 2 * Math.PI) / ring.points;
          const rawPoint = {
            x: ring.radius * Math.cos(angle),
            y: 0,
            z: ring.radius * Math.sin(angle)
          };
          // Apply ring tilt then global rotation
          const tilted = rotatePoint(rawPoint, ring.tiltX, ring.tiltY, 0);
          const world = rotatePoint(tilted, rotX, rotY, rotZ);

          const zDist = fov + world.z;
          if (zDist > 10) {
            const scale = fov / zDist;
            ringPoints.push({
              px: centerX + world.x * scale,
              py: centerY + world.y * scale,
              z: world.z,
              scale
            });
          }
        }

        if (ringPoints.length > 2) {
          ctx.beginPath();
          ctx.moveTo(ringPoints[0].px, ringPoints[0].py);
          for (let p = 1; p < ringPoints.length; p++) {
            ctx.lineTo(ringPoints[p].px, ringPoints[p].py);
          }
          ctx.closePath();
          ctx.strokeStyle = `${ring.color}0.35)`;
          ctx.lineWidth = 1.2;
          ctx.stroke();

          // Draw orbiting satellite node on the ring
          const satIdx = Math.floor((time * 0.05 * (idx + 1)) % ringPoints.length);
          const sat = ringPoints[satIdx];
          if (sat && sat.z > -sphereRadius * 0.5) {
            // Satellite glow halo
            const satGlow = ctx.createRadialGradient(sat.px, sat.py, 1, sat.px, sat.py, 8 * sat.scale);
            satGlow.addColorStop(0, `${ring.color}0.9)`);
            satGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = satGlow;
            ctx.beginPath();
            ctx.arc(sat.px, sat.py, 8 * sat.scale, 0, Math.PI * 2);
            ctx.fill();

            // Core dot
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(sat.px, sat.py, 2.2 * sat.scale, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      });

      animationFrameId = requestAnimationFrame(render);
    };

    animationFrameId = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div
      className={`pointer-events-none fixed inset-0 overflow-hidden select-none z-0 ${className}`}
      style={{ opacity }}
    >
      <canvas ref={canvasRef} className="w-full h-full block" />
    </div>
  );
}
