// wasmClient.js
import * as wasm from "../../wasm_connector/pkg/wasm_connector.js";

let ready = false;

export async function initWasm() {
  if (!ready) {
    // wasm-pack glue code auto-loads the wasm
    // if async init is needed:
    if (wasm.default) await wasm.default(); // some versions of wasm-pack output
    ready = true;
  }
}

export async function buildPacket(route, payload, token = null) {
  await initWasm();
  return wasm.build_request_with_token(route, JSON.stringify(payload), token);
}

export async function decodePacket(raw) {
  await initWasm();
  return JSON.parse(wasm.parse_response(raw));
}

export async function hashPassword(password) {
  await initWasm();
  return wasm.hash_password(password);
}