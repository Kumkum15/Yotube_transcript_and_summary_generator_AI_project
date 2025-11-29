const API = "http://127.0.0.1:8000";

function setStatus(t){ document.getElementById("status").innerText = "Status: " + t; }

async function post(endpoint, body) {
  setStatus(endpoint + "…");
  const res = await fetch(API + endpoint, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    const text = await res.text();
    setStatus("Error");
    throw new Error(text || "Request failed");
  }
  const j = await res.json();
  setStatus("Done");
  return j;
}

document.getElementById("validateBtn").addEventListener("click", async ()=>{
  const url = document.getElementById("urlInput").value.trim();
  if (!url) return alert("Paste a YouTube URL");
  try {
    const r = await post("/validate", {url});
    document.getElementById("metaOut").innerText = JSON.stringify(r.meta, null, 2);
  } catch (e) { alert(e.message) }
});

document.getElementById("downloadBtn").addEventListener("click", async ()=>{
  const url = document.getElementById("urlInput").value.trim(); if(!url) return alert("Paste URL");
  try {
    const r = await post("/download", {url});
    alert("Audio saved: " + r.audio_path);
  } catch(e){ alert(e.message) }
});

document.getElementById("transcribeBtn").addEventListener("click", async ()=>{
  const url = document.getElementById("urlInput").value.trim(); if(!url) return alert("Paste URL");
  try {
    const r = await post("/transcribe", {url});
    document.getElementById("transcriptOut").innerText = r.transcript;
  } catch(e){ alert(e.message) }
});

document.getElementById("summaryBtn").addEventListener("click", async ()=>{
  const url = document.getElementById("urlInput").value.trim(); if(!url) return alert("Paste URL");
  try {
    const r = await post("/summarize", {url});
    document.getElementById("summaryOut").innerText = r.summary.raw || JSON.stringify(r.summary, null, 2);
  } catch(e){ alert(e.message) }
});

document.getElementById("metaBtn").addEventListener("click", async ()=>{
  const url = document.getElementById("urlInput").value.trim(); if(!url) return alert("Paste URL");
  try {
    const r = await post("/validate", {url});
    document.getElementById("metaOut").innerText = JSON.stringify(r.meta, null, 2);
  } catch(e){ alert(e.message) }
});