//! The separate, checksum-pinned files in the web release. No language data in the WASM.
use wasm_bindgen::JsCast;
use wasm_bindgen_futures::JsFuture;

// The LibreOffice/dictionaries revision in craft-i18n's manifest, also the browser cache key.
const DIRECTORY: &str = "language-packs/4f1df64b2e8e1475/de-CH";

async fn file(name: &str, max: u32) -> Result<Vec<u8>, String> {
    let window = web_sys::window().ok_or("no browser window")?;
    let url = format!("{DIRECTORY}/{name}");
    let response = JsFuture::from(window.fetch_with_str(&url)).await.map_err(|_| format!("could not fetch {name}"))?;
    let response: web_sys::Response = response.dyn_into().map_err(|_| "invalid browser response")?;
    if !response.ok() {
        return Err(format!("{name}: HTTP {}", response.status()));
    }
    let buffer = JsFuture::from(response.array_buffer().map_err(|_| "missing response body")?).await.map_err(|_| "incomplete response body")?;
    let bytes = js_sys::Uint8Array::new(&buffer);
    if bytes.length() > max {
        return Err(format!("{name} is too large"));
    }
    Ok(bytes.to_vec())
}

pub(super) async fn load() -> Result<(), String> {
    let aff = file("de_CH_frami.aff", 1 << 20).await?;
    let dic = file("de_CH_frami.dic", 16 << 20).await?;
    let notice = String::from_utf8(file("NOTICE.txt", 1 << 20).await?).map_err(|_| "invalid licence notice")?;
    wordcraft_proof::packs::install_spelling_pack("de-CH", &aff, &dic, notice)
}
