'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Sparkles, Rotate3d, ShieldCheck, Cpu } from 'lucide-react';

/**
 * HoloCore3D
 * An interactive, draggable 3D Holographic Core widget.
 * Features an animated wireframe polyhedron with rotating cyber-rings,
 * glowing nodal vertices, and "Designed by Divyanshu Yadav" branding.
 */
export default function HoloCore3D({ className = '' }) {
  const canvasRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [rotationSpeed, setRotationSpeed] = useState(1);
  const lastMousePos = useRef({ x: 0, y: 0 });
  const rotRef = useRef({ x: 0.3, y: 0.5, z: 0 });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animId;
    const width = (canvas.width = 240);
    const height = (canvas.height = 240);
    const fov = 260;
    const radius = 64;

    // Define 3D Octahedron / Polyhedron Vertices
    const vertices = [
      { x: 0, y: -radius, z: 0 },
      { x: radius, y: 0, z: 0 },
      { x: 0, y: 0, z: radius },
      { x: -radius, y: 0, z: 0 },
      { x: 0, y: 0, z: -radius },
      { x: 0, y: radius, z: 0 },
    ];

    // Inner core vertices (Cube)
    const innerRadius = radius * 0.45;
    const innerVertices = [
      { x: -innerRadius, y: -innerRadius, z: -innerRadius },
      { x: innerRadius, y: -innerRadius, z: -innerRadius },
      { x: innerRadius, y: innerRadius, z: -innerRadius },
      { x: -innerRadius, y: innerRadius, z: -innerRadius },
      { x: -innerRadius, y: -innerRadius, z: innerRadius },
      { x: innerRadius, y: -innerRadius, z: innerRadius },
      { x: innerRadius, y: innerRadius, z: innerRadius },
      { x: -innerRadius, y: innerRadius, z: innerRadius },
    ];

    // Edges connecting outer vertices
    const edges = [
      [0, 1], [0, 2], [0, 3], [0, 4],
      [5, 1], [5, 2], [5, 3], [5, 4],
      [1, 2], [2, 3], [3, 4], [4, 1]
    ];

    // Inner cube edges
    const innerEdges = [
      [0, 1], [1, 2], [2, 3], [3, 0],
      [4, 5], [5, 6], [6, 7], [7, 4],
      [0, 4], [1, 5], [2, 6], [3, 7]
    ];

    const rotate3D = (p, rx, ry, rz) => {
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

    let time = 0;

    const render = () => {
      time += 0.02 * rotationSpeed;
      if (!isDragging) {
        rotRef.current.y += 0.015 * rotationSpeed;
        rotRef.current.x += 0.008 * rotationSpeed;
      }

      ctx.clearRect(0, 0, width, height);

      const cx = width / 2;
      const cy = height / 2;

      // Glow halo
      const radial = ctx.createRadialGradient(cx, cy, 5, cx, cy, radius * 1.5);
      radial.addColorStop(0, 'rgba(45, 212, 191, 0.25)');
      radial.addColorStop(0.5, 'rgba(56, 189, 248, 0.1)');
      radial.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = radial;
      ctx.fillRect(0, 0, width, height);

      // Project outer vertices
      const proj = vertices.map(v => {
        const r = rotate3D(v, rotRef.current.x, rotRef.current.y, rotRef.current.z);
        const scale = fov / (fov + r.z);
        return {
          x: cx + r.x * scale,
          y: cy + r.y * scale,
          z: r.z,
          scale
        };
      });

      // Draw outer edges
      edges.forEach(([i, j]) => {
        const p1 = proj[i];
        const p2 = proj[j];
        const avgZ = (p1.z + p2.z) / 2;
        const alpha = Math.max(0.15, Math.min(0.9, (avgZ + radius) / (radius * 2)));

        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.strokeStyle = `rgba(45, 212, 191, ${alpha})`;
        ctx.lineWidth = 1.6;
        ctx.stroke();
      });

      // Project inner vertices (counter-rotating)
      const innerProj = innerVertices.map(v => {
        const r = rotate3D(v, -rotRef.current.x * 1.2, -rotRef.current.y * 1.2, time);
        const scale = fov / (fov + r.z);
        return {
          x: cx + r.x * scale,
          y: cy + r.y * scale,
          z: r.z,
          scale
        };
      });

      // Draw inner edges
      innerEdges.forEach(([i, j]) => {
        const p1 = innerProj[i];
        const p2 = innerProj[j];
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.strokeStyle = `rgba(168, 85, 247, 0.5)`;
        ctx.lineWidth = 1;
        ctx.stroke();
      });

      // Draw glowing outer vertex dots
      proj.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 3 * p.scale, 0, Math.PI * 2);
        ctx.fillStyle = p.z > 0 ? '#5eead4' : '#2dd4bf';
        ctx.shadowColor = '#2dd4bf';
        ctx.shadowBlur = p.z > 0 ? 8 : 2;
        ctx.fill();
        ctx.shadowBlur = 0;
      });

      // Orbiting particles ring
      const ringPoints = 20;
      ctx.beginPath();
      for (let i = 0; i < ringPoints; i++) {
        const angle = (i * 2 * Math.PI) / ringPoints + time * 1.5;
        const rx = Math.cos(angle) * (radius * 1.25);
        const rz = Math.sin(angle) * (radius * 1.25);
        const pt = rotate3D({ x: rx, y: 0, z: rz }, rotRef.current.x * 0.5, rotRef.current.y * 0.5, 0.4);
        const scale = fov / (fov + pt.z);
        const px = cx + pt.x * scale;
        const py = cy + pt.y * scale;
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
      ctx.setLineDash([3, 4]);
      ctx.stroke();
      ctx.setLineDash([]);

      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);

    return () => cancelAnimationFrame(animId);
  }, [isDragging, rotationSpeed]);

  const handleMouseDown = (e) => {
    setIsDragging(true);
    lastMousePos.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    const dx = e.clientX - lastMousePos.current.x;
    const dy = e.clientY - lastMousePos.current.y;
    rotRef.current.y += dx * 0.02;
    rotRef.current.x += dy * 0.02;
    lastMousePos.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  return (
    <div
      className={`relative rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-950/95 border border-teal-500/30 p-4 shadow-xl backdrop-blur-md flex flex-col items-center justify-between group overflow-hidden ${className}`}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
    >
      {/* Background ambient glow */}
      <div className="absolute -top-12 -right-12 w-32 h-32 rounded-full bg-teal-500/10 blur-2xl pointer-events-none" />

      {/* Top Header Tag */}
      <div className="w-full flex items-center justify-between text-[11px] font-semibold text-teal-400 mb-1 z-10">
        <span className="flex items-center gap-1.5 uppercase tracking-wider">
          <Cpu className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          Neural Holographic Core
        </span>
        <span className="text-[10px] text-slate-400 font-mono bg-white/5 px-2 py-0.5 rounded-full border border-white/5">
          Interactive
        </span>
      </div>

      {/* 3D Canvas */}
      <div className="relative cursor-grab active:cursor-grabbing my-1">
        <canvas
          ref={canvasRef}
          className="rounded-xl transition-transform duration-200 group-hover:scale-105"
        />
        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 text-[9px] text-slate-400/80 bg-slate-950/80 px-2 py-0.5 rounded-full border border-white/5 pointer-events-none whitespace-nowrap">
          Drag to Rotate
        </div>
      </div>

      {/* Signature Design by Divyanshu Yadav */}
      <div className="w-full pt-3 mt-1 border-t border-white/10 flex items-center justify-between z-10">
        <div className="flex flex-col">
          <div className="flex items-center gap-1 text-[11px] font-bold text-white">
            <Sparkles className="w-3 h-3 text-amber-400" />
            <span>Designed by Divyanshu Yadav</span>
          </div>
          <span className="text-[10px] text-teal-400/90 font-mono">
            Roll No: 25MCA00PY0036
          </span>
        </div>

        <button
          onClick={(e) => {
            e.stopPropagation();
            setRotationSpeed(prev => (prev === 1 ? 2.5 : prev === 2.5 ? 0.3 : 1));
          }}
          className="p-1.5 rounded-lg bg-teal-500/10 border border-teal-500/30 text-teal-300 hover:bg-teal-500/20 text-[10px] flex items-center gap-1 transition"
          title="Toggle rotation speed"
        >
          <Rotate3d className="w-3.5 h-3.5" />
          <span>Speed</span>
        </button>
      </div>
    </div>
  );
}
