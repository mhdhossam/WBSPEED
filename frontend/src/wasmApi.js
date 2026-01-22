import {
  wasmReady,
  buildSealedRequest,
  decodeSealedResponse
} from "./wasmClient";

const BACKEND = "http://127.0.0.1:8000";

export async function sendConvex(route, payload) {
  await wasmReady();

  const sealed = buildSealedRequest(route, payload, null);

  const res = await fetch(`${BACKEND}/wasm_gateway/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: sealed,
  });

  const json = await res.json();
  if (!json.payload) throw new Error("No payload");

  return decodeSealedResponse(JSON.stringify(json));
}
