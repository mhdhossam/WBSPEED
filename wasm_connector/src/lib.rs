use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};
use base64::{engine::general_purpose, Engine as _};
use sha2::{Sha256, Digest};

#[derive(Serialize, Deserialize)]
struct Packet {
    route: String,
    payload: String,       // base64 encoded payload
    token: Option<String>, // JWT optional
}

#[wasm_bindgen]
pub fn build_request_with_token(route: &str, payload_json: &str, token: Option<String>) -> String {
    let payload_b64 = general_purpose::STANDARD.encode(payload_json.as_bytes());
    let packet = Packet {
        route: route.to_string(),
        payload: payload_b64,
        token,
    };
    serde_json::to_string(&packet).unwrap()
}

#[wasm_bindgen]
pub fn parse_response(response_text: &str) -> String {
    let v: serde_json::Value = serde_json::from_str(response_text).unwrap();
    let payload_b64 = v.get("payload").and_then(|p| p.as_str()).unwrap_or("");
    let decoded = general_purpose::STANDARD.decode(payload_b64).unwrap();
    String::from_utf8(decoded).unwrap()
}

// optional client-side pre-hash function
#[wasm_bindgen]
pub fn hash_password(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    let result = hasher.finalize();
    hex::encode(result)
}
