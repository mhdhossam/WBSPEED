import React, { useState } from "react";
import { wasmReady, buildSealedRequest, decodeSealedResponse, wasmHash } from "./wasmClient";

export default function App(){
  const [username,setUsername] = useState("");
  const [password,setPassword] = useState("");
  const [token,setToken] = useState(localStorage.getItem("access") || "");

  async function handleRegister(){
    await wasmReady();
    // pre-hash password in WASM before sending
    const clientHashed = wasmHash(password);
    const res = await fetch("http://127.0.0.1:8000/auth/register/", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ username, email: `${username}@example.com`, password: clientHashed, password2: clientHashed })
    });
    const data = await res.json();
    if(res.ok){
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      setToken(data.access);
      alert("Registered and logged in")
    } else {
      alert(JSON.stringify(data));
    }
  }

  async function handleLogin(){
    await wasmReady();
    const clientHashed = wasmHash(password);
    const res = await fetch("http://127.0.0.1:8000/auth/login/", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ username, password: clientHashed })
    });
    const data = await res.json();
    if(res.ok){
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      setToken(data.access);
      alert("Logged in");
    } else {
      alert(JSON.stringify(data));
    }
  }

  async function sendSealed(){
    await wasmReady();
    const tokenLocal = token || localStorage.getItem("access") || null;
    const sealed = buildSealedRequest("/api/data/", { name: "Mohamed" }, tokenLocal);
    const res = await fetch("http://127.0.0.1:8000/wasm_gateway/", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: sealed
    });
    const raw = await res.text();
    const obj = decodeSealedResponse(raw);
    alert("Server replied: " + JSON.stringify(obj));
  }

  return (
    <div style={{padding:20}}>
      <h1>Auth + WASM demo</h1>
      <input placeholder="username" value={username} onChange={e=>setUsername(e.target.value)} />
      <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin}>Login</button>
      <div style={{marginTop:20}}>
        <button onClick={sendSealed}>Send sealed request</button>
      </div>
    </div>
  );
}
