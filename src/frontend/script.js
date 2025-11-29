const API = "http://127.0.0.1:8000";

function el(id){ return document.getElementById(id); }
function setStatus(s){ el("status").textContent = "Status: " + s; }

async function post(path, payload){
  setStatus("working...");
  try {
    const res = await fetch(API + path, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    const contentType = res.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      const json = await res.json();
      setStatus("idle");
      return json;
    } else {
      const text = await res.text();
      setStatus("idle");
      return { raw: text };
    }
  } catch (err) {
    setStatus("error");
    return { error: String(err) };
  }
}

async function validateURL(){
  const url = el("url").value.trim();
  if (!url){ alert("Paste a YouTube URL first"); return; }
  setStatus("validating");
  const r = await post("/validate", { url });
  if (r.error) {
    el("output").textContent = "Validate error: " + r.error;
    return;
  }
  if (r.status === "valid" || r.status === "ok"){
    el("afterValidate").classList.remove("hidden");
    el("metaBox").innerHTML = `<strong>${r.meta.title || r.meta.id}</strong>\nChannel: ${r.meta.uploader || "N/A"}\nDuration: ${r.meta.duration || "N/A"} sec`;
    el("output").textContent = "Link valid. Choose an action below.";
    setStatus("validated");
  } else {
    el("output").textContent = JSON.stringify(r, null, 2);
    setStatus("idle");
  }
}

// Buttons actions
async function fetchMeta(){
  const url = el("url").value.trim();
  const r = await post("/validate", { url });
  el("output").textContent = JSON.stringify(r, null, 2);
}

async function downloadAudio(){
  const url = el("url").value.trim();
  const r = await post("/download", { url });
  el("output").textContent = JSON.stringify(r, null, 2);
}

async function getTranscript(){
  const url = el("url").value.trim();
  el("output").textContent = "Processing transcript... (this may take a while)";
  const r = await post("/transcribe", { url });
  if (r.transcript) el("output").textContent = r.transcript;
  else el("output").textContent = JSON.stringify(r, null, 2);
}

async function getSummary(){
  const url = el("url").value.trim();
  el("output").textContent = "Generating summary... (this may take a while)";
  const r = await post("/summarize", { url });
  if (r.summary) el("output").textContent = r.summary;
  else el("output").textContent = JSON.stringify(r, null, 2);
}