// wasmApi.js
import { buildPacket, decodePacket } from "./wasmClient";

const API_URL = "http://localhost:8000/wasm_gateway/";

export async function sendConvex(route, payload = {}, token = null) {
  const packet = await buildPacket(route, payload, token);

  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: packet
  });

  const raw = await res.text();

  if (!res.ok) throw new Error("Gateway error: " + raw);

  return decodePacket(raw);
}