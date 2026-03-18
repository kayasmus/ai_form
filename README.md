<!doctype html>
<html lang="en" class="h-full">
 <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Form — Real-Time Exercise Form Correction</title>
  <script src="https://cdn.tailwindcss.com/3.4.17"></script>
  <script src="https://cdn.jsdelivr.net/npm/lucide@0.263.0/dist/umd/lucide.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&amp;family=Outfit:wght@300;400;500;600;700;800&amp;display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    .font-display { font-family: 'Outfit', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }

    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse-glow {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 0.8; }
    }
    @keyframes skeleton-move {
      0% { transform: rotate(-3deg); }
      50% { transform: rotate(3deg); }
      100% { transform: rotate(-3deg); }
    }
    @keyframes float-up {
      0% { transform: translateY(0); }
      50% { transform: translateY(-8px); }
      100% { transform: translateY(0); }
    }

    .anim-fade { animation: fadeUp 0.7s ease-out both; }
    .anim-d1 { animation-delay: 0.1s; }
    .anim-d2 { animation-delay: 0.2s; }
    .anim-d3 { animation-delay: 0.3s; }
    .anim-d4 { animation-delay: 0.4s; }
    .anim-d5 { animation-delay: 0.5s; }
    .anim-d6 { animation-delay: 0.6s; }

    .skeleton-figure { animation: skeleton-move 3s ease-in-out infinite; }
    .float-anim { animation: float-up 4s ease-in-out infinite; }

    .code-block {
      background: #0d1117;
      border: 1px solid #21262d;
      border-radius: 8px;
      overflow-x: auto;
    }

    .gradient-text {
      background: linear-gradient(135deg, #f97316, #ec4899);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .card-hover {
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card-hover:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 40px rgba(249, 115, 22, 0.15);
    }

    .section-observer {
      opacity: 0;
      transform: translateY(40px);
      transition: opacity 0.6s ease, transform 0.6s ease;
    }
    .section-observer.visible {
      opacity: 1;
      transform: translateY(0);
    }

    table { border-collapse: separate; border-spacing: 0; }
    th, td { text-align: left; }
  </style>
  <style>body { box-sizing: border-box; }</style>
  <script src="/_sdk/data_sdk.js" type="text/javascript"></script>
  <script src="/_sdk/element_sdk.js" type="text/javascript"></script>
 </head>
 <body class="h-full font-display" style="background-color: #080b12; color: #e2e8f0;">
  <div id="app-wrapper" class="w-full h-full overflow-auto">
   <!-- Hero Section -->
   <header class="relative w-full overflow-hidden" style="min-height: 90%;">
    <div class="absolute inset-0" style="background: radial-gradient(ellipse at 30% 20%, rgba(249,115,22,0.12) 0%, transparent 60%), radial-gradient(ellipse at 70% 80%, rgba(168,85,247,0.1) 0%, transparent 50%);"></div><!-- Grid pattern -->
    <div class="absolute inset-0 opacity-10" style="background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px); background-size: 60px 60px;"></div>
    <div class="relative z-10 max-w-5xl mx-auto px-6 py-20 flex flex-col items-center justify-center" style="min-height: 90%;">
     <!-- Floating badge -->
     <div class="anim-fade anim-d1 inline-flex items-center gap-2 px-4 py-2 rounded-full border mb-8" style="background: rgba(249,115,22,0.1); border-color: rgba(249,115,22,0.3);">
      <span class="w-2 h-2 rounded-full" style="background: #f97316; animation: pulse-glow 2s infinite;"></span> <span class="text-sm font-medium" style="color: #f97316;">Supervised Learning System</span>
     </div>
     <h1 id="hero-title" class="anim-fade anim-d2 text-5xl md:text-7xl font-extrabold text-center leading-tight mb-2"><span class="gradient-text">AI FORM</span></h1>
     <p id="hero-subtitle" class="anim-fade anim-d3 text-xl md:text-2xl font-light text-center mb-6" style="color: #94a3b8;">Real-Time Exercise Form Correction</p>
     <p id="hero-description" class="anim-fade anim-d4 text-base md:text-lg text-center max-w-2xl mb-12" style="color: #64748b;">A supervised learning system that watches your movement and corrects it in real time — using only your camera.</p><!-- Animated skeleton SVG -->
     <div class="anim-fade anim-d5 relative w-64 h-64 mx-auto">
      <svg viewbox="0 0 200 200" class="w-full h-full">
       <!-- Orange skeleton (current form) --> <g class="skeleton-figure" transform-origin="100 100" opacity="0.9">
        <circle cx="90" cy="40" r="12" fill="none" stroke="#f97316" stroke-width="2.5" />
        <line x1="90" y1="52" x2="90" y2="100" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
        <line x1="90" y1="65" x2="60" y2="50" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
        <line x1="60" y1="50" x2="45" y2="70" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
        <line x1="90" y1="65" x2="120" y2="55" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
        <line x1="120" y1="55" x2="135" y2="75" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
        <line x1="90" y1="100" x2="70" y2="140" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
        <line x1="70" y1="140" x2="65" y2="170" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
        <line x1="90" y1="100" x2="110" y2="140" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
        <line x1="110" y1="140" x2="115" y2="170" stroke="#f97316" stroke-width="2.5" stroke-linecap="round" />
       </g> <!-- Purple skeleton (corrected form) --> <g class="float-anim" opacity="0.7">
        <circle cx="110" cy="38" r="12" fill="none" stroke="#a855f7" stroke-width="2" stroke-dasharray="4 3" />
        <line x1="110" y1="50" x2="110" y2="98" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
        <line x1="110" y1="63" x2="80" y2="42" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
        <line x1="80" y1="42" x2="70" y2="60" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
        <line x1="110" y1="63" x2="140" y2="42" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
        <line x1="140" y1="42" x2="150" y2="60" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
        <line x1="110" y1="98" x2="95" y2="138" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
        <line x1="95" y1="138" x2="92" y2="168" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
        <line x1="110" y1="98" x2="125" y2="138" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
        <line x1="125" y1="138" x2="128" y2="168" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 3" />
       </g>
      </svg>
      <div class="absolute bottom-0 left-0 right-0 flex justify-center gap-6 text-xs font-mono">
       <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 inline-block" style="background:#f97316;"></span><span style="color:#f97316;">Your form</span></span> <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 inline-block" style="background:#a855f7;"></span><span style="color:#a855f7;">Corrected</span></span>
      </div>
     </div><!-- Scroll indicator -->
     <div class="anim-fade anim-d6 mt-12 flex flex-col items-center gap-2" style="color: #475569;">
      <span class="text-xs tracking-widest uppercase">Scroll to explore</span> <i data-lucide="chevron-down" style="width:20px; height:20px;"></i>
     </div>
    </div>
   </header><!-- Problem Section -->
   <section class="section-observer w-full py-20 px-6">
    <div class="max-w-4xl mx-auto">
     <div class="flex items-center gap-3 mb-8">
      <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background: rgba(239,68,68,0.15);">
       <i data-lucide="alert-triangle" style="width:20px; height:20px; color:#ef4444;"></i>
      </div>
      <h2 id="problem-title" class="text-3xl md:text-4xl font-bold">The Problem</h2>
     </div>
     <p class="text-lg mb-10" style="color:#94a3b8;">Beginner gym-goers don't know if their form is good. Online videos show what good form <em>looks like</em> — but not if <strong style="color:#e2e8f0;">you</strong> are doing it right.</p>
     <div class="grid md:grid-cols-3 gap-5">
      <div class="card-hover rounded-xl p-6" style="background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.15);">
       <p class="text-3xl font-bold font-mono mb-2" style="color:#ef4444;">5,400+</p>
       <p class="text-sm" style="color:#94a3b8;">Gym injuries per year linked to poor form</p>
      </div>
      <div class="card-hover rounded-xl p-6" style="background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.15);">
       <p class="text-3xl font-bold font-mono mb-2" style="color:#ef4444;">¥10,000</p>
       <p class="text-sm" style="color:#94a3b8;">Average cost of a personal trainer per session</p>
      </div>
      <div class="card-hover rounded-xl p-6" style="background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.15);">
       <p class="text-3xl font-bold font-mono mb-2" style="color:#ef4444;">Zero</p>
       <p class="text-sm" style="color:#94a3b8;">Real-time feedback for solo training</p>
      </div>
     </div>
    </div>
   </section><!-- Solution Section -->
   <section class="section-observer w-full py-20 px-6">
    <div class="max-w-4xl mx-auto">
     <div class="flex items-center gap-3 mb-8">
      <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background: rgba(34,197,94,0.15);">
       <i data-lucide="check-circle" style="width:20px; height:20px; color:#22c55e;"></i>
      </div>
      <h2 id="solution-title" class="text-3xl md:text-4xl font-bold">The Solution</h2>
     </div>
     <p class="text-lg mb-10" style="color:#94a3b8;">AI Form is a <strong style="color:#e2e8f0;">supervised regression model</strong> that:</p>
     <div class="grid md:grid-cols-3 gap-5">
      <div class="card-hover rounded-xl p-6" style="background: rgba(249,115,22,0.06); border: 1px solid rgba(249,115,22,0.18);">
       <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4" style="background: rgba(249,115,22,0.15);">
        <i data-lucide="eye" style="width:24px; height:24px; color:#f97316;"></i>
       </div>
       <p class="font-semibold text-lg mb-2" style="color:#f97316;">SEES</p>
       <p class="text-sm" style="color:#94a3b8;">Detects your pose using live camera input</p>
      </div>
      <div class="card-hover rounded-xl p-6" style="background: rgba(168,85,247,0.06); border: 1px solid rgba(168,85,247,0.18);">
       <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4" style="background: rgba(168,85,247,0.15);">
        <i data-lucide="cpu" style="width:24px; height:24px; color:#a855f7;"></i>
       </div>
       <p class="font-semibold text-lg mb-2" style="color:#a855f7;">THINKS</p>
       <p class="text-sm" style="color:#94a3b8;">Identifies specific form errors across 8 joint features</p>
      </div>
      <div class="card-hover rounded-xl p-6" style="background: rgba(34,197,94,0.06); border: 1px solid rgba(34,197,94,0.18);">
       <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-4" style="background: rgba(34,197,94,0.15);">
        <i data-lucide="pen-tool" style="width:24px; height:24px; color:#22c55e;"></i>
       </div>
       <p class="font-semibold text-lg mb-2" style="color:#22c55e;">DOES</p>
       <p class="text-sm" style="color:#94a3b8;">Generates a corrective skeleton overlay in real time</p>
      </div>
     </div>
    </div>
   </section><!-- How It Works Section -->
   <section class="section-observer w-full py-20 px-6">
    <div class="max-w-4xl mx-auto">
     <div class="flex items-center gap-3 mb-12">
      <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background: rgba(168,85,247,0.15);">
       <i data-lucide="zap" style="width:20px; height:20px; color:#a855f7;"></i>
      </div>
      <h2 id="how-title" class="text-3xl md:text-4xl font-bold">How It Works</h2>
     </div><!-- Step 1 -->
     <div class="mb-16">
      <div class="flex items-center gap-3 mb-4">
       <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold font-mono" style="background: rgba(249,115,22,0.2); color:#f97316;">1</span>
       <h3 class="text-xl font-semibold">Pose Estimation</h3>
      </div>
      <p class="mb-4" style="color:#94a3b8;">MediaPipe extracts <strong style="color:#e2e8f0;">33 body landmarks</strong> per frame — each with x, y, z coordinates representing horizontal position, vertical position, and depth.</p><!-- Landmark visualization -->
      <div class="rounded-xl p-6 flex justify-center" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);">
       <svg viewbox="0 0 160 260" class="w-40">
        <circle cx="80" cy="25" r="14" fill="none" stroke="#f97316" stroke-width="1.5" /> <circle cx="80" cy="25" r="2" fill="#f97316" /> <!-- Spine --> <line x1="80" y1="39" x2="80" y2="70" stroke="#475569" stroke-width="1.5" /> <line x1="80" y1="70" x2="80" y2="130" stroke="#475569" stroke-width="1.5" /> <!-- Shoulders --> <line x1="80" y1="55" x2="45" y2="55" stroke="#475569" stroke-width="1.5" /> <line x1="80" y1="55" x2="115" y2="55" stroke="#475569" stroke-width="1.5" /> <!-- Arms --> <line x1="45" y1="55" x2="30" y2="90" stroke="#475569" stroke-width="1.5" /> <line x1="30" y1="90" x2="22" y2="120" stroke="#475569" stroke-width="1.5" /> <line x1="115" y1="55" x2="130" y2="90" stroke="#475569" stroke-width="1.5" /> <line x1="130" y1="90" x2="138" y2="120" stroke="#475569" stroke-width="1.5" /> <!-- Hips --> <line x1="80" y1="130" x2="60" y2="130" stroke="#475569" stroke-width="1.5" /> <line x1="80" y1="130" x2="100" y2="130" stroke="#475569" stroke-width="1.5" /> <!-- Legs --> <line x1="60" y1="130" x2="55" y2="185" stroke="#475569" stroke-width="1.5" /> <line x1="55" y1="185" x2="50" y2="240" stroke="#475569" stroke-width="1.5" /> <line x1="100" y1="130" x2="105" y2="185" stroke="#475569" stroke-width="1.5" /> <line x1="105" y1="185" x2="110" y2="240" stroke="#475569" stroke-width="1.5" /> <!-- Landmark dots --> <g fill="#f97316">
         <circle cx="80" cy="55" r="3" />
         <circle cx="45" cy="55" r="3" />
         <circle cx="115" cy="55" r="3" />
         <circle cx="30" cy="90" r="3" />
         <circle cx="130" cy="90" r="3" />
         <circle cx="22" cy="120" r="3" />
         <circle cx="138" cy="120" r="3" />
         <circle cx="80" cy="130" r="3" />
         <circle cx="60" cy="130" r="3" />
         <circle cx="100" cy="130" r="3" />
         <circle cx="55" cy="185" r="3" />
         <circle cx="105" cy="185" r="3" />
         <circle cx="50" cy="240" r="3" />
         <circle cx="110" cy="240" r="3" />
        </g> <text x="80" y="258" text-anchor="middle" fill="#64748b" font-size="9" font-family="JetBrains Mono, monospace">
         33 landmarks
        </text>
       </svg>
      </div>
     </div><!-- Step 2 -->
     <div class="mb-16">
      <div class="flex items-center gap-3 mb-4">
       <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold font-mono" style="background: rgba(249,115,22,0.2); color:#f97316;">2</span>
       <h3 class="text-xl font-semibold">Feature Extraction</h3>
      </div>
      <p class="mb-6" style="color:#94a3b8;">From the 33 landmarks, <strong style="color:#e2e8f0;">8 joint angle features</strong> are computed per frame:</p>
      <div class="overflow-x-auto rounded-xl" style="border: 1px solid rgba(255,255,255,0.08);">
       <table class="w-full text-sm">
        <thead>
         <tr style="background: rgba(255,255,255,0.04);">
          <th class="px-5 py-3 font-mono font-medium text-xs uppercase tracking-wider" style="color:#f97316;">Feature</th>
          <th class="px-5 py-3 font-medium text-xs uppercase tracking-wider" style="color:#94a3b8;">Description</th>
         </tr>
        </thead>
        <tbody>
         <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
          <td class="px-5 py-3 font-mono text-xs" style="color:#f97316;">left_arm_raise</td>
          <td class="px-5 py-3" style="color:#94a3b8;">Angle at left shoulder (hip → shoulder → elbow)</td>
         </tr>
         <tr style="border-top: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.015);">
          <td class="px-5 py-3 font-mono text-xs" style="color:#f97316;">right_arm_raise</td>
          <td class="px-5 py-3" style="color:#94a3b8;">Angle at right shoulder (hip → shoulder → elbow)</td>
         </tr>
         <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
          <td class="px-5 py-3 font-mono text-xs" style="color:#f97316;">left_elbow_angle</td>
          <td class="px-5 py-3" style="color:#94a3b8;">Angle at left elbow (shoulder → elbow → wrist)</td>
         </tr>
         <tr style="border-top: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.015);">
          <td class="px-5 py-3 font-mono text-xs" style="color:#f97316;">right_elbow_angle</td>
          <td class="px-5 py-3" style="color:#94a3b8;">Angle at right elbow (shoulder → elbow → wrist)</td>
         </tr>
         <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
          <td class="px-5 py-3 font-mono text-xs" style="color:#f97316;">torso_lean</td>
          <td class="px-5 py-3" style="color:#94a3b8;">Spine vector deviation from vertical</td>
         </tr>
         <tr style="border-top: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.015);">
          <td class="px-5 py-3 font-mono text-xs" style="color:#f97316;">arm_symmetry</td>
          <td class="px-5 py-3" style="color:#94a3b8;">Absolute difference between left and right raise</td>
         </tr>
         <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
          <td class="px-5 py-3 font-mono text-xs" style="color:#f97316;">left_wrist_above_shoulder</td>
          <td class="px-5 py-3" style="color:#94a3b8;">Vertical distance (shoulder.y − wrist.y)</td>
         </tr>
         <tr style="border-top: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.015);">
          <td class="px-5 py-3 font-mono text-xs" style="color:#f97316;">right_wrist_above_shoulder</td>
          <td class="px-5 py-3" style="color:#94a3b8;">Vertical distance (shoulder.y − wrist.y)</td>
         </tr>
        </tbody>
       </table>
      </div>
     </div><!-- Step 3 -->
     <div class="mb-16">
      <div class="flex items-center gap-3 mb-4">
       <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold font-mono" style="background: rgba(249,115,22,0.2); color:#f97316;">3</span>
       <h3 class="text-xl font-semibold">The Model</h3>
      </div>
      <p class="mb-2" style="color:#94a3b8;"><strong style="color:#e2e8f0;">Type:</strong> Keras Sequential — supervised regression</p>
      <div class="code-block p-5 my-6 font-mono text-sm leading-relaxed">
       <pre style="color:#e2e8f0;"><span style="color:#f97316;">Input</span>(8)
  → <span style="color:#a855f7;">Dense</span>(64, <span style="color:#22c55e;">relu</span>)
  → <span style="color:#64748b;">Dropout</span>(0.15)
  → <span style="color:#a855f7;">Dense</span>(64, <span style="color:#22c55e;">relu</span>)
  → <span style="color:#64748b;">Dropout</span>(0.15)
  → <span style="color:#a855f7;">Dense</span>(32, <span style="color:#22c55e;">relu</span>)
  → <span style="color:#a855f7;">Dense</span>(8, <span style="color:#3b82f6;">linear</span>)</pre>
      </div>
      <div class="grid md:grid-cols-3 gap-4 text-sm">
       <div class="rounded-lg p-4" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);">
        <p class="font-semibold mb-1" style="color:#f97316;">Input</p>
        <p style="color:#94a3b8;">8 bad-form joint angles</p>
       </div>
       <div class="rounded-lg p-4" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);">
        <p class="font-semibold mb-1" style="color:#a855f7;">Output</p>
        <p style="color:#94a3b8;">8 corrected good-form joint angles</p>
       </div>
       <div class="rounded-lg p-4" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);">
        <p class="font-semibold mb-1" style="color:#22c55e;">Loss</p>
        <p style="color:#94a3b8;">MSE (training) | MAE + Max Error (eval)</p>
       </div>
      </div>
     </div><!-- Step 4 -->
     <div>
      <div class="flex items-center gap-3 mb-4">
       <span class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold font-mono" style="background: rgba(249,115,22,0.2); color:#f97316;">4</span>
       <h3 class="text-xl font-semibold">Output — Two Skeletons</h3>
      </div>
      <div class="grid md:grid-cols-2 gap-4">
       <div class="card-hover rounded-xl p-5 flex items-center gap-4" style="background: rgba(249,115,22,0.06); border: 1px solid rgba(249,115,22,0.18);">
        <div class="w-5 h-5 rounded-full" style="background: #f97316;"></div>
        <div>
         <p class="font-semibold" style="color:#f97316;">Orange Skeleton</p>
         <p class="text-sm" style="color:#94a3b8;">Your current form</p>
        </div>
       </div>
       <div class="card-hover rounded-xl p-5 flex items-center gap-4" style="background: rgba(168,85,247,0.06); border: 1px solid rgba(168,85,247,0.18);">
        <div class="w-5 h-5 rounded-full" style="background: #a855f7;"></div>
        <div>
         <p class="font-semibold" style="color:#a855f7;">Purple Skeleton</p>
         <p class="text-sm" style="color:#94a3b8;">Corrected target form</p>
        </div>
       </div>
      </div>
     </div>
    </div>
   </section><!-- Data Pipeline Section -->
   <section class="section-observer w-full py-20 px-6">
    <div class="max-w-4xl mx-auto">
     <div class="flex items-center gap-3 mb-8">
      <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background: rgba(59,130,246,0.15);">
       <i data-lucide="database" style="width:20px; height:20px; color:#3b82f6;"></i>
      </div>
      <h2 id="data-title" class="text-3xl md:text-4xl font-bold">Data Pipeline</h2>
     </div>
     <div class="rounded-xl p-6 mb-8" style="background: rgba(59,130,246,0.06); border: 1px solid rgba(59,130,246,0.15);">
      <p class="font-semibold mb-2" style="color:#3b82f6;">🚨 The Challenge</p>
      <p style="color:#94a3b8;">Bad form data is <strong style="color:#e2e8f0;">rare, dangerous, and often unlabeled.</strong> We couldn't ask people to intentionally injure themselves.</p>
     </div>
     <h3 class="text-xl font-semibold mb-4">Synthetic Bad-Form Generation</h3>
     <p class="mb-4" style="color:#94a3b8;">We filmed good form only — then mathematically corrupted it:</p>
     <div class="code-block p-5 mb-8 font-mono text-sm">
      <pre style="color:#e2e8f0;"><span style="color:#64748b;">// Corruption formula</span>
<span style="color:#f97316;">bad_angle</span> = <span style="color:#22c55e;">good_angle</span> + <span style="color:#a855f7;">bias</span> + <span style="color:#3b82f6;">N</span>(0, noise_std)</pre>
     </div>
     <h4 class="font-semibold mb-4" style="color:#94a3b8;">5 error templates applied (3 randomly per frame):</h4>
     <div class="overflow-x-auto rounded-xl mb-10" style="border: 1px solid rgba(255,255,255,0.08);">
      <table class="w-full text-sm">
       <thead>
        <tr style="background: rgba(255,255,255,0.04);">
         <th class="px-5 py-3 font-medium text-xs uppercase tracking-wider text-left" style="color:#a855f7;">Error Type</th>
         <th class="px-5 py-3 font-medium text-xs uppercase tracking-wider text-left" style="color:#94a3b8;">Bias Range</th>
        </tr>
       </thead>
       <tbody>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
         <td class="px-5 py-3" style="color:#e2e8f0;">Arms too high</td>
         <td class="px-5 py-3 font-mono" style="color:#f97316;">+20° to +40°</td>
        </tr>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.015);">
         <td class="px-5 py-3" style="color:#e2e8f0;">Arms too low</td>
         <td class="px-5 py-3 font-mono" style="color:#f97316;">−20° to −35°</td>
        </tr>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
         <td class="px-5 py-3" style="color:#e2e8f0;">Elbows too bent</td>
         <td class="px-5 py-3 font-mono" style="color:#f97316;">−20° to −40°</td>
        </tr>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.015);">
         <td class="px-5 py-3" style="color:#e2e8f0;">Torso swinging</td>
         <td class="px-5 py-3 font-mono" style="color:#f97316;">+10° to +25°</td>
        </tr>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
         <td class="px-5 py-3" style="color:#e2e8f0;">Asymmetric raise</td>
         <td class="px-5 py-3 font-mono" style="color:#f97316;">+15° to +30°</td>
        </tr>
       </tbody>
      </table>
     </div>
     <h4 class="font-semibold mb-4">Final Dataset</h4>
     <div class="overflow-x-auto rounded-xl" style="border: 1px solid rgba(255,255,255,0.08);">
      <table class="w-full text-sm">
       <thead>
        <tr style="background: rgba(255,255,255,0.04);">
         <th class="px-5 py-3 font-medium text-xs uppercase tracking-wider text-left" style="color:#3b82f6;">Source</th>
         <th class="px-5 py-3 font-medium text-xs uppercase tracking-wider text-left" style="color:#94a3b8;">Frames</th>
        </tr>
       </thead>
       <tbody>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
         <td class="px-5 py-3" style="color:#94a3b8;">Real paired (bad + good)</td>
         <td class="px-5 py-3 font-mono" style="color:#e2e8f0;">451</td>
        </tr>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.015);">
         <td class="px-5 py-3" style="color:#94a3b8;">Good-form only (67 videos)</td>
         <td class="px-5 py-3 font-mono" style="color:#e2e8f0;">2,855</td>
        </tr>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05);">
         <td class="px-5 py-3" style="color:#94a3b8;">Synthetic bad-form</td>
         <td class="px-5 py-3 font-mono" style="color:#e2e8f0;">8,565</td>
        </tr>
        <tr style="border-top: 1px solid rgba(255,255,255,0.05); background: rgba(249,115,22,0.06);">
         <td class="px-5 py-3 font-bold" style="color:#f97316;">Total</td>
         <td class="px-5 py-3 font-mono font-bold" style="color:#f97316;">11,115</td>
        </tr>
       </tbody>
      </table>
     </div>
    </div>
   </section><!-- Results Section -->
   <section class="section-observer w-full py-20 px-6">
    <div class="max-w-4xl mx-auto">
     <div class="flex items-center gap-3 mb-8">
      <div class="w-10 h-10 rounded-lg flex items-center justify-center" style="background: rgba(34,197,94,0.15);">
       <i data-lucide="trending-up" style="width:20px; height:20px; color:#22c55e;"></i>
      </div>
      <h2 id="results-title" class="text-3xl md:text-4xl font-bold">Results</h2>
     </div>
     <div class="grid md:grid-cols-3 gap-5 mb-10">
      <div class="card-hover rounded-xl p-6 text-center" style="background: rgba(34,197,94,0.06); border: 1px solid rgba(34,197,94,0.18);">
       <p class="text-4xl font-bold font-mono mb-2" style="color:#22c55e;">2.63°</p>
       <p class="text-xs uppercase tracking-wider" style="color:#94a3b8;">MAE (avg across 8 features)</p>
      </div>
      <div class="card-hover rounded-xl p-6 text-center" style="background: rgba(249,115,22,0.06); border: 1px solid rgba(249,115,22,0.18);">
       <p class="text-4xl font-bold font-mono mb-2" style="color:#f97316;">7.72°</p>
       <p class="text-xs uppercase tracking-wider" style="color:#94a3b8;">Mean Max Error</p>
      </div>
      <div class="card-hover rounded-xl p-6 text-center" style="background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.18);">
       <p class="text-4xl font-bold font-mono mb-2" style="color:#ef4444;">32.71°</p>
       <p class="text-xs uppercase tracking-wider" style="color:#94a3b8;">Worst-case Error</p>
      </div>
     </div><!-- Improvement bars -->
     <div class="rounded-xl p-6" style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);">
      <h4 class="font-semibold mb-6">Improvement over V1</h4>
      <div class="space-y-5">
       <div>
        <div class="flex justify-between text-sm mb-2">
         <span style="color:#94a3b8;">MAE &amp; Mean Max Error</span> <span class="font-mono font-bold" style="color:#22c55e;">55% ↓</span>
        </div>
        <div class="w-full h-3 rounded-full overflow-hidden" style="background: rgba(255,255,255,0.06);">
         <div class="h-full rounded-full transition-all duration-1000" id="bar-mae" style="width: 0%; background: linear-gradient(90deg, #22c55e, #16a34a);"></div>
        </div>
       </div>
       <div>
        <div class="flex justify-between text-sm mb-2">
         <span style="color:#94a3b8;">Worst-case Error</span> <span class="font-mono font-bold" style="color:#f97316;">27% ↓</span>
        </div>
        <div class="w-full h-3 rounded-full overflow-hidden" style="background: rgba(255,255,255,0.06);">
         <div class="h-full rounded-full transition-all duration-1000" id="bar-worst" style="width: 0%; background: linear-gradient(90deg, #f97316, #ea580c);"></div>
        </div>
       </div>
      </div>
     </div>
    </div>
   </section><!-- Footer -->
   <footer class="w-full py-12 px-6 text-center" style="border-top: 1px solid rgba(255,255,255,0.06);">
    <p class="gradient-text font-bold text-2xl mb-2">AI FORM</p>
    <p class="text-sm" style="color:#475569;">Real-Time Exercise Form Correction — Supervised Learning System</p>
   </footer>
  </div>
  <script>
    // Intersection observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');

          // Animate progress bars when results section appears
          if (entry.target.querySelector('#bar-mae')) {
            setTimeout(() => {
              document.getElementById('bar-mae').style.width = '55%';
              document.getElementById('bar-worst').style.width = '27%';
            }, 300);
          }
        }
      });
    }, { threshold: 0.15 });

    document.querySelectorAll('.section-observer').forEach(el => observer.observe(el));

    // Init Lucide icons
    lucide.createIcons();
  </script>
 <script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'9de0f8076600e3a7',t:'MTc3MzgwMjYzNS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>
