from flask import Flask, request, jsonify

app = Flask(__name__)

# Route für die Hauptseite
@app.route('/')
def home():
    return """<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Dino (offline) — Ein Datei</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial}
    html,body,#game {height:100%}
    body{display:flex;align-items:center;justify-content:center;min-height:100vh;background:linear-gradient(#e9f2ff,#f5f5f7);color:#222}
    .container{width:95%;max-width:900px;padding:20px;text-align:center}
    h1{margin-bottom:8px;font-size:1.6rem}
    .hint{margin-bottom:12px;color:#444}
    .game-wrap{position:relative;background:#fff;border-radius:8px;box-shadow:0 8px 30px rgba(10,20,40,0.08);overflow:hidden}
    canvas{display:block;width:100%;height:auto;background:linear-gradient(#fff,#f0f5ff)}
    .overlay{position:absolute;top:8px;left:8px;right:8px;display:flex;justify-content:space-between;align-items:center;pointer-events:none}
    #score{background:rgba(0,0,0,0.6);color:#fff;padding:6px 10px;border-radius:6px;font-weight:600;pointer-events:auto}
    #restartBtn{pointer-events:auto;padding:6px 10px;border-radius:6px;border:0;background:#0078d4;color:#fff;cursor:pointer}
    #restartBtn.hidden{display:none}
    .credits{margin-top:12px;color:#666;font-size:0.9rem}
    @media (max-width:600px){h1{font-size:1.2rem}}
  </style>
</head>
<body>
  <div class="container">
    <h1>Offline Dino (eine Datei)</h1>
    <p class="hint">Leertaste, Pfeil oben oder Tippen zum Springen. Pfeil runter zum Ducken.</p>
    <div class="game-wrap">
      <canvas id="gameCanvas" width="800" height="200"></canvas>
      <div class="overlay">
        <div id="score">Punkte: 0</div>
        <button id="restartBtn">Neustart</button>
      </div>
    </div>
    <p class="credits">Kein Internet erforderlich — funktioniert offline.</p>
  </div>

  <script>
  (function(){
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    let WIDTH = canvas.width;
    let HEIGHT = canvas.height;

    function resizeCanvas() {
      const rect = canvas.getBoundingClientRect();
      canvas.width = Math.floor(rect.width);
      canvas.height = Math.floor(rect.height);
      WIDTH = canvas.width;
      HEIGHT = canvas.height;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    let running = true;
    let score = 0;
    let highScore = 0;
    let gameSpeed = 6;

    const player = { x:50, y: HEIGHT-50, w:40, h:40, vy:0, gravity:0.8, jumpForce:-14, grounded:true, ducking:false };
    let obstacles = [];
    let spawnTimer = 0;

    function resetGame(){
      running=true; score=0; obstacles=[]; spawnTimer=0; gameSpeed=6;
      player.y = HEIGHT - player.h - 10; player.vy=0; player.grounded=true;
      document.getElementById('restartBtn').classList.add('hidden');
    }

    let keys = {};
    window.addEventListener('keydown', (e)=>{ keys[e.code]=true; if (['Space','ArrowUp'].includes(e.code)) e.preventDefault(); });
    window.addEventListener('keyup', (e)=>{ keys[e.code]=false; });

    window.addEventListener('touchstart', (e)=>{ e.preventDefault(); if (!running) return; jump(); });

    function jump(){ if (player.grounded){ player.vy = player.jumpForce; player.grounded=false; } }
    function duck(on){ player.ducking = on; player.h = on ? 24 : 40; }

    function spawnObstacle(){ const h = Math.random()>0.5 ? 30 : 18; const w = Math.random()>0.5 ? 24 : 14; obstacles.push({x: WIDTH+20, y: HEIGHT - h - 10, w, h}); }

    function update(dt){ if (!running) return; score += dt * 0.01; gameSpeed += dt * 0.0003;
      player.vy += player.gravity; player.y += player.vy;
      if (player.y + player.h >= HEIGHT - 10){ player.y = HEIGHT - player.h - 10; player.vy = 0; player.grounded = true; }
      if ((keys['Space'] || keys['ArrowUp']) && player.grounded) jump(); duck(keys['ArrowDown']);
      spawnTimer -= dt; if (spawnTimer <= 0){ spawnObstacle(); spawnTimer = 800 + Math.random()*1200 / (1 + score * 0.02); }
      for (let i = obstacles.length - 1; i >= 0; i--){ const o = obstacles[i]; o.x -= gameSpeed + Math.floor(score * 0.02); if (o.x + o.w < -50) obstacles.splice(i,1);
        if (rectsCollide(player.x, player.y, player.w, player.h, o.x, o.y, o.w, o.h)){ running=false; document.getElementById('restartBtn').classList.remove('hidden'); highScore = Math.max(highScore, Math.floor(score)); document.getElementById('score').textContent = `Punkte: ${Math.floor(score)} — Game Over (Best: ${highScore})`; }
      }
      if (running) document.getElementById('score').textContent = `Punkte: ${Math.floor(score)}`;
    }

    function rectsCollide(x1,y1,w1,h1,x2,y2,w2,h2){ return x1 < x2 + w2 && x1 + w1 > x2 && y1 < y2 + h2 && y1 + h1 > y2; }

    function draw(){ ctx.clearRect(0,0,WIDTH,HEIGHT);
      const grad = ctx.createLinearGradient(0,0,0,HEIGHT); grad.addColorStop(0,'#f6fbff'); grad.addColorStop(1,'#eef6ff'); ctx.fillStyle = grad; ctx.fillRect(0,0,WIDTH,HEIGHT);
      ctx.fillStyle = '#dedede'; ctx.fillRect(0, HEIGHT - 10, WIDTH, 10);
      ctx.fillStyle = '#222'; ctx.fillRect(player.x, player.y, player.w, player.h);
      ctx.fillStyle = '#333'; for (const o of obstacles) ctx.fillRect(o.x, o.y, o.w, o.h);
      ctx.fillStyle = '#ffd54a'; ctx.beginPath(); ctx.arc(WIDTH - 60, 40, 20, 0, Math.PI*2); ctx.fill(); }

    let lastTime = performance.now(); function loop(now){ const dt = now - lastTime; lastTime = now; update(dt); draw(); requestAnimationFrame(loop); }
    requestAnimationFrame(loop);

    const restartBtn = document.getElementById('restartBtn'); restartBtn.addEventListener('click', ()=> resetGame());
    player.y = HEIGHT - player.h - 10;
    setInterval(()=>{ if (player.y > HEIGHT - player.h - 10) player.y = HEIGHT - player.h - 10; },500);
    window.addEventListener('keydown', (e) => { if (['ArrowUp','ArrowDown','Space'].includes(e.code)) e.preventDefault(); });
    window.addEventListener('load', ()=>{ const s = localStorage.getItem('dino_highscore'); if (s) highScore = Number(s); });
    window.addEventListener('beforeunload', ()=>{ localStorage.setItem('dino_highscore', highScore); });
  })();
  </script>
</body>
</html>"""


@app.route('/Profil')
def gym():
    return "Eray hat schwache Arme."

# Route zum Empfangen von Nachrichten
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.json
    message = data.get('message', '')
    print(f"Empfangen: {message}")
    response_message = f"Echo: {message}"
    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # Server starten

