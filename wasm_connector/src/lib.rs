use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};
use base64::{engine::general_purpose, Engine as _};
use sha2::{Sha256, Digest};
use js_sys::Promise;
use wasm_bindgen_futures::JsFuture;
use web_sys::{Request, RequestInit, RequestMode, Response};

#[wasm_bindgen]
extern "C" {
    // console.log for debugging
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

#[derive(Serialize, Deserialize)]
struct Packet {
    route: String,
    payload: String,
    token: Option<String>,
}

/// Build a JSON packet with optional token and base64 encode the payload
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

/// Decode response payload from Convex
#[wasm_bindgen]
pub fn parse_response(response_text: &str) -> String {
    let v: serde_json::Value = serde_json::from_str(response_text).unwrap();
    let payload_b64 = v.get("payload").and_then(|p| p.as_str()).unwrap_or("");
    let decoded = general_purpose::STANDARD.decode(payload_b64).unwrap();
    String::from_utf8(decoded).unwrap()
}

/// Hash a string (e.g., password) using SHA256
#[wasm_bindgen]
pub fn hash_password(input: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input.as_bytes());
    hex::encode(hasher.finalize())
}

/// Send packet directly to Convex from WASM (browser-compatible)
#[wasm_bindgen]
pub async fn send_to_convex(route: &str, payload: &str, token: Option<String>) -> JsValue {
    let convex_url = "https://groovy-wildebeest-80.convex.site"; // hidden inside WASM

    let body_json = build_request_with_token(route, payload, token);

    let mut opts = RequestInit::new();
    opts.method("POST");
    opts.mode(RequestMode::Cors);
    opts.body(Some(&JsValue::from_str(&body_json)));

    let request = Request::new_with_str_and_init(convex_url, &opts).unwrap();
    request
        .headers()
        .set("Content-Type", "application/json")
        .unwrap();

    // Perform fetch
    let resp_value = JsFuture::from(web_sys::window().unwrap().fetch_with_request(&request))
        .await
        .unwrap();
    let resp: Response = resp_value.dyn_into().unwrap();

    let text = JsFuture::from(resp.text().unwrap()).await.unwrap();
    text
}