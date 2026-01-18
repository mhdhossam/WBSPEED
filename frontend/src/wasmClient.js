import init, { build_request_with_token, parse_response, hash_password } from "./wasm_pkg/wasm_connector.js";

let _ready = false;
export async function wasmReady() {
  if (!_ready) {
    await init();
    _ready = true;
  }
}

export function buildSealedRequest(route, obj, token) {
  const json = JSON.stringify(obj);
  return build_request_with_token(route, json, token ?? null);
}

export function decodeSealedResponse(raw) {
  const payloadJson = parse_response(raw); // returns JSON string payload
  return JSON.parse(payloadJson);
}

export function wasmHash(password) {
  return hash_password(password);
}
