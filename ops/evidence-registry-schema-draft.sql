-- P7 DRAFT — evidence_registry Postgres schema (free lane)
-- Spec pointer: GSPC-Drift-Product-Spec §2.1 (effort M; infra not provisioned)
-- Does NOT create a live DB. No spend. No DOI remint.
-- Aligns with instrument evidence cells (sov_instrument.py) + signed board attestation.

-- Append-only measurement ledger. Deletion is an attack; soft tombstones only via corrections.

CREATE TABLE IF NOT EXISTS evidence_cell (
  cell_hash   CHAR(64) PRIMARY KEY,           -- SHA-256 hex of cell body (excl. cell_hash)
  prev_hash   CHAR(64) NOT NULL,              -- GENESIS = 64×'0' for first cell
  model       TEXT NOT NULL,
  lens        TEXT NOT NULL CHECK (lens IN ('governance','defence','provenance','continuity')),
  item_id     TEXT NOT NULL,
  provision   TEXT NOT NULL,                  -- e.g. EU-AIAct-Art50
  passed      BOOLEAN NOT NULL,
  corpus_hash TEXT NOT NULL,
  ts          TIMESTAMPTZ NOT NULL DEFAULT now(),
  grader      TEXT,                           -- e.g. signature_alg, survival_check
  payload     JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS evidence_cell_lens_ts ON evidence_cell (lens, ts DESC);
CREATE INDEX IF NOT EXISTS evidence_cell_prev ON evidence_cell (prev_hash);

CREATE TABLE IF NOT EXISTS evidence_correction (
  id          BIGSERIAL PRIMARY KEY,
  cell_hash   CHAR(64) NOT NULL REFERENCES evidence_cell(cell_hash),
  reason      TEXT NOT NULL,
  corrected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  -- Corrections append; they never rewrite evidence_cell rows.
  note        TEXT
);

-- REST sketch (not implemented here):
--   GET  /api/evidence-registry/cells?lens=&limit=
--   GET  /api/evidence-registry/cells/{cell_hash}
--   GET  /api/evidence-registry/verify-chain?from=&to=
--   POST /api/evidence-registry/cells  (signed ingest; owner-gated)
-- Verify: recompute cell_hash + walk prev_hash to GENESIS.

-- Owner gate: provision Postgres + bind REST only after Nick CONFIRM (infra/cost).
