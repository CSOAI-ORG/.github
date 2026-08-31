/**
 * Living GSPC board assertions for read-only live audits.
 * Quote totals.public_count. Never freeze 13/14, 15/22, or jail UNTESTED.
 */

export function assertLivingGspc(j, { fail, pass, warn } = {}) {
  const ok = (m) => (pass ? pass(m) : undefined);
  const bad = (m) => {
    if (fail) fail(m);
    return false;
  };
  const soft = (m) => (warn ? warn(m) : undefined);

  if (!j || typeof j !== "object") return bad("/api/gspc: not an object");
  if (j.schema !== "csoai.gspc-axes/0.5") return bad(`schema ${j.schema}`);
  ok("schema csoai.gspc-axes/0.5");

  const t = j.totals || {};
  const publicCount = String(t.public_count || "").trim();
  if (typeof t.axes !== "number" || t.axes < 1) return bad(`totals.axes ${t.axes}`);
  ok(`totals.axes ${t.axes} (live)`);
  if (typeof t.measured_axes !== "number") return bad(`totals.measured_axes ${t.measured_axes}`);
  ok(`totals.measured_axes ${t.measured_axes} (live)`);
  if (typeof t.unmeasured_axes === "number") {
    ok(`totals.unmeasured_axes ${t.unmeasured_axes} (live)`);
  }
  if (!publicCount) return bad("totals.public_count missing");
  ok(`public_count ${publicCount}`);

  if (/13 measured of 14/.test(publicCount) && !(t.measured_axes === 13 && t.axes === 14)) {
    return bad("public_count still says 13 of 14 but live totals are not 13/14");
  }

  const axes = Array.isArray(j.axes) ? j.axes : [];
  if (axes.length !== t.axes) return bad(`axes[] length ${axes.length} != totals.axes ${t.axes}`);
  ok(`axes[] length matches totals.axes (${t.axes})`);

  const jail = axes.find((a) => a?.axis === "jail");
  if (!jail) return bad("jail axis missing");
  ok(`jail ${jail.status || "present"} · separation ${jail.separation || "n/a"} (live)`);

  if (!j.site_attestation) soft("site_attestation missing");
  else ok("site_attestation present");

  return { totals: t, publicCount, jail, axes };
}

/** Chat/copy overclaims against a living board — not a frozen 13/14 sitting. */
export function livingOverclaims(plain, totals) {
  const measured = totals?.measured_axes;
  const axes = totals?.axes;
  const hits = [];
  if (/\ball\s+22\s+measured\b/i.test(plain) && measured !== 22) hits.push("all 22 measured");
  if (/\b16\s+measured\s+axes\b/i.test(plain)) hits.push("16 measured axes");
  if (/\b13\s+of\s+14\b/.test(plain) && !(measured === 13 && axes === 14)) {
    hits.push("stale 13 of 14");
  }
  if (/\bElo\b/.test(plain) && !/not (a |an )?Elo|Elo is not/i.test(plain)) {
    hits.push("Elo as board language");
  }
  if (/\bcertif(?:y|ied|ication)\b/i.test(plain) && !/not certif/i.test(plain)) {
    hits.push("certification language");
  }
  return hits;
}
