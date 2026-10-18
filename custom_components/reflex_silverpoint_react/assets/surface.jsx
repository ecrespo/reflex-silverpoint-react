/* reflex-silverpoint-react — the surface every Reflex-composed silverpoint component is built on.
 *
 * A surface is the root markup contract of @silverpoint/grounds/ui.css:
 *   .sp-ui.sp-<name>.sp-ground-<ground>[data-substrate][data-mode][data-size][data-frame]
 * with an optional hand-inked frame (<span part="sp-frame" data-kind>) and tone
 * (<span part="sp-tone" data-tone>) laid over its box. Ground, substrate, mode and frame variant are
 * resolved by @silverpoint/core's own resolveUi, so a surface draws exactly as an Sp component does,
 * and switches to precision under prefers-contrast: more / forced-colors: active.
 */
const SP_REFLEX_CSS_ID = "sp-reflex-surfaces";

function spInjectReflexCss(css) {
  if (typeof document === "undefined" || document.getElementById(SP_REFLEX_CSS_ID)) return;
  const style = document.createElement("style");
  style.id = SP_REFLEX_CSS_ID;
  style.textContent = css;
  document.head.appendChild(style);
}

function useSpForcedPrecision() {
  const [forced, setForced] = useState(false);
  useEffect(() => {
    if (typeof matchMedia !== "function") return undefined;
    const query = matchMedia(FORCED_PRECISION_QUERY);
    const update = () => setForced(query.matches);
    update();
    query.addEventListener?.("change", update);
    return () => query.removeEventListener?.("change", update);
  }, []);
  return forced;
}

function SilverpointSurface({
  element = "div", name, ground, substrate, mode, size, seed, frame, tone, className, children, id, ...rest
}) {
  useEffect(() => spInjectReflexCss(SP_REFLEX_CSS), []);
  const forced = useSpForcedPrecision();
  const r = resolveUi({ ground, substrate, mode, size, seed, id }, { forcedPrecision: forced });
  const Tag = element;
  const classes = ["sp-ui", "sp-surface", name ? `sp-${name}` : null, `sp-ground-${r.ground}`, className]
    .filter(Boolean).join(" ");
  return (
    <Tag
      id={id}
      className={classes}
      data-ground={r.ground}
      data-substrate={r.substrate}
      data-mode={r.mode}
      data-size={r.size}
      data-frame={String(r.frame)}
      {...rest}
    >
      {tone ? <span part="sp-tone" data-tone={String(tone)} data-kind={frame || "box"} aria-hidden="true" /> : null}
      {frame ? <span part="sp-frame" data-kind={frame} aria-hidden="true" /> : null}
      {children}
    </Tag>
  );
}

/* A drawn mark: the same 16×16 glyphs as the Sp components (UI_GLYPHS), plus a few of our own. */
const SP_EXTRA_GLYPHS = {
  plus: "M8,3.5V12.5M3.5,8H12.5",
  chevronDown: "M4,6L8,10L12,6",
  chevronRight: "M6,4L10,8L6,12",
  chevronLeft: "M10,4L6,8L10,12",
  arrowUp: "M8,12.5V3.5M4.5,7L8,3.5L11.5,7",
  arrowDown: "M8,3.5V12.5M4.5,9L8,12.5L11.5,9",
  sortUp: "M5,9.5L8,5.5L11,9.5Z",
  sortDown: "M5,6.5L8,10.5L11,6.5Z",
  sort: "M5,7L8,3.5L11,7Z M5,9L8,12.5L11,9Z",
  ellipsis: "M3.5,8V8 M8,8V8 M12.5,8V8",
};

function SilverpointGlyph({ glyph, className, ...rest }) {
  const d = SP_EXTRA_GLYPHS[glyph] || UI_GLYPHS[glyph] || "";
  return (
    <svg part="sp-mark" data-glyph={glyph} viewBox="0 0 16 16" aria-hidden="true" focusable="false" className={className} {...rest}>
      <path d={d} />
    </svg>
  );
}

/* Pagination: the page window is computed here, so `current` can be a state var. */
function spPageWindow(count, current, siblings) {
  const pages = [];
  const first = Math.max(2, current - siblings);
  const last = Math.min(count - 1, current + siblings);
  pages.push(1);
  if (first > 2) pages.push("prev-gap");
  for (let p = first; p <= last; p++) pages.push(p);
  if (last < count - 1) pages.push("next-gap");
  if (count > 1) pages.push(count);
  return pages;
}

function SilverpointPagination({
  total = 0, pageSize = 10, current, defaultCurrent = 1, siblings = 1, onChange, label = "Pagination",
  previousLabel = "Previous page", nextLabel = "Next page", pageLabel = "Page", showTotal = false, totalTemplate = "{start}–{end} of {total}",
  disabled = false, ...surface
}) {
  const [held, setHeld] = useState(defaultCurrent);
  const count = Math.max(1, Math.ceil(Number(total) / Math.max(1, Number(pageSize))));
  const page = Math.min(Math.max(1, Number(current ?? held) || 1), count);
  const go = (next) => {
    const target = Math.min(Math.max(1, next), count);
    if (target === page || disabled) return;
    if (current === undefined || current === null) setHeld(target);
    onChange?.(target);
  };
  const start = total ? (page - 1) * pageSize + 1 : 0;
  const end = Math.min(total, page * pageSize);
  const summary = totalTemplate.replace("{start}", start).replace("{end}", end).replace("{total}", total);
  const button = (key, content, target, extra = {}) => (
    <li key={key}>
      <button type="button" className="sp-ui-page" disabled={disabled || extra.disabled} onClick={() => go(target)} {...extra.attrs}>
        <span part="sp-frame" data-kind="control" aria-hidden="true" />
        {content}
      </button>
    </li>
  );
  return (
    <SilverpointSurface element="nav" name="pagination" aria-label={label} data-disabled={disabled ? "true" : undefined} {...surface}>
      {showTotal ? <span className="sp-ui-page-total">{summary}</span> : null}
      <ul className="sp-ui-pages">
        {button("prev", <SilverpointGlyph glyph="chevronLeft" />, page - 1, { disabled: page <= 1, attrs: { "aria-label": previousLabel } })}
        {spPageWindow(count, page, siblings).map((p) =>
          typeof p === "string" ? (
            <li key={p} className="sp-ui-page-gap" aria-hidden="true">…</li>
          ) : p === page ? (
            <li key={p}>
              <span className="sp-ui-page" aria-current="page" aria-label={`${pageLabel} ${p}`}>
                <span part="sp-frame" data-kind="control" aria-hidden="true" />
                <span part="sp-heighten" className="sp-ui-page-label">{p}</span>
              </span>
            </li>
          ) : (
            button(p, <span className="sp-ui-page-label">{p}</span>, p, { attrs: { "aria-label": `${pageLabel} ${p}` } })
          ),
        )}
        {button("next", <SilverpointGlyph glyph="chevronRight" />, page + 1, { disabled: page >= count, attrs: { "aria-label": nextLabel } })}
      </ul>
    </SilverpointSurface>
  );
}

/* InputNumber: a native number input with exact − / + steppers; the value is clamped and rounded. */
function spRound(value, precision) {
  if (precision === undefined || precision === null) return value;
  const f = 10 ** precision;
  return Math.round(value * f) / f;
}

function SilverpointInputNumber({
  value, defaultValue, min, max, step = 1, precision, onChange, placeholder, label, message, invalid = false,
  disabled = false, readOnly = false, name, inputId, decrementLabel = "Decrease", incrementLabel = "Increase", ...surface
}) {
  const [held, setHeld] = useState(defaultValue ?? null);
  const controlled = value !== undefined;
  const current = controlled ? value : held;
  const clamp = (n) => {
    let v = n;
    if (min !== undefined && min !== null) v = Math.max(min, v);
    if (max !== undefined && max !== null) v = Math.min(max, v);
    return spRound(v, precision);
  };
  const commit = (next) => {
    if (!controlled) setHeld(next);
    onChange?.(next);
  };
  const stepBy = (direction) => {
    if (disabled || readOnly) return;
    const base = typeof current === "number" && Number.isFinite(current) ? current : (min ?? 0);
    commit(clamp(base + direction * step));
  };
  const messageId = message && inputId ? `${inputId}--message` : undefined;
  return (
    <SilverpointSurface element="span" name="input" className="sp-input-number" data-invalid={invalid ? "true" : undefined} {...surface}>
      <span className="sp-ui-box">
        <span part="sp-frame" data-kind="control" aria-hidden="true" />
        <button type="button" className="sp-ui-stepper" aria-label={decrementLabel} disabled={disabled || readOnly || (min !== undefined && min !== null && current !== null && current <= min)} onClick={() => stepBy(-1)}>
          <SilverpointGlyph glyph="dash" />
        </button>
        <input
          className="sp-ui-control"
          type="number"
          inputMode="decimal"
          id={inputId}
          name={name}
          min={min}
          max={max}
          step={step}
          value={current === null || current === undefined ? "" : current}
          placeholder={placeholder}
          disabled={disabled}
          readOnly={readOnly}
          aria-label={label}
          aria-invalid={invalid ? "true" : undefined}
          aria-describedby={messageId}
          onChange={(event) => {
            const raw = event.target.value;
            if (raw === "") return commit(null);
            const n = Number(raw);
            if (Number.isFinite(n)) commit(n);
          }}
          onBlur={() => {
            if (typeof current === "number") {
              const fixed = clamp(current);
              if (fixed !== current) commit(fixed);
            }
          }}
        />
        <button type="button" className="sp-ui-stepper" aria-label={incrementLabel} disabled={disabled || readOnly || (max !== undefined && max !== null && current !== null && current >= max)} onClick={() => stepBy(1)}>
          <SilverpointGlyph glyph="plus" />
        </button>
      </span>
      {message ? <span className="sp-ui-message" id={messageId}>{message}</span> : null}
    </SilverpointSurface>
  );
}
