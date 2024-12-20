import igv from "https://esm.sh/igv@3.1.2";

/**
 * @typedef Config
 * @property {string} genome
 * @property {(string | Array<string>)=} locus
 * @property {Array<Record<string, unknown>>} tracks
 */

/**
 * @typedef Model
 * @property {Config} config
 */

/** @type {import("npm:@anywidget/types").Render<Model>} */
async function render({ model, el }) {
  const browser = await igv.createBrowser(el, model.get("config"));
  return () => {
    igv.removeBrowser(browser);
  };
}

export default { render };
