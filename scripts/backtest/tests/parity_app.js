// Runs the APP's own rule code (extracted from index.html) on bars supplied by parity_app_vs_engine.py.
// Usage: node parity_app.js INDEX_HTML CASES_JSON  → prints JSON results
const fs = require("fs");
const src = fs.readFileSync(process.argv[2], "utf8");
const grab = (start, end) => { const a = src.indexOf(start), b = src.indexOf(end, a); if (a < 0 || b < 0) throw new Error("not found: " + start); return src.slice(a, b); };
const code = [
  grab("const SCORE_WEIGHTS = {", "\n};") + "\n};",
  grab("const fmt = n =>", "\n"),
  grab("const daysUntil = (ymd)", "\n"),
  "const secFd = () => null;",
  grab("const computeIndicators = (b) => {", "\n// ═══"),
  grab("const parseEntryDate = (s) => {", "\nconst runRuleEngine"),
  grab("const runRuleEngine = (d, marketData", "\nconst claudeExplain"),
  grab("const idxStatus = (b) => {", "\nconst marketFromIndexes"),
  "module.exports = { computeIndicators, runRuleEngine, idxStatus };",
].join("\n");
const m = { exports: {} }; new Function("module", code)(m);
const { computeIndicators, runRuleEngine, idxStatus } = m.exports;
const cases = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const far = new Date(Date.now() + 60 * 864e5).toISOString().slice(0, 10);
const out = cases.map(k => {
  if (k.kind === "market") { const a = idxStatus(k.spy), b = idxStatus(k.qqq);
    return { id: k.id, market: (a.st === "CORRECTION" && b.st === "CORRECTION") ? "CORRECTION" : (a.st !== "UPTREND" || b.st !== "UPTREND") ? "PRESSURE" : "UPTREND" }; }
  const b = k.bars, L = b[b.length - 1], ind = computeIndicators(b);
  const d = { price: L.c, volume: L.v, avgVolume: ind.avgVol50, volumePartial: false, ...ind, bars: b };
  const md = { marketStatus: k.market, marketSource: "rules", fundamentals: { epsLatest: 2, epsYearAgo: 1 }, nextEarningsDate: far };
  const r = runRuleEngine(d, md, "entry");
  return { id: k.id, rating: r.rating, setup: r.setupType, stop: r.stopLoss ?? null, pivot: ind.pivot, sma50: ind.sma50, sma200: ind.sma200, atr: ind.atr, rsi: ind.rsi };
});
console.log(JSON.stringify(out));
