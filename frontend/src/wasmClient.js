import init, {
  build_request_with_token,
  parse_response
} from "./wasm_pkg/wasm_connector.js";

let ready = false;

export async function wasmReady() {
  if (!ready) {
    await init();
    ready = true;
  }
}

export function buildSealedRequest(route, payload, token) {
  return build_request_with_token(
    route,
    JSON.stringify(payload),
    token
  );
}

export function decodeSealedResponse(raw) {
  return JSON.parse(parse_response(raw));
}
