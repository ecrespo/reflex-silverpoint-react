/* reflex-silverpoint-react — sp_trigger: a native <button> drawn as SpButton, that keeps every prop.
 *
 * An overlay of @silverpoint/react clones its trigger with aria-haspopup, aria-expanded,
 * aria-controls, onPointerDown and onClick (useTrigger, REQ-500). SpButton 0.7.0 keeps only its own
 * props, so those would be lost on it; this button renders the very tree @silverpoint/core's
 * uiButtonView builds (resolveUi resolves ground, substrate, mode, size, frame variant and palette)
 * and adds everything else it is given to the native element.
 */
const SP_TRIGGER_ATTRS = { class: "className", for: "htmlFor", readonly: "readOnly", tabindex: "tabIndex" };

function spTriggerStyle(text) {
  const out = {};
  for (const declaration of (text || "").split(";")) {
    const colon = declaration.indexOf(":");
    if (colon > 0) out[declaration.slice(0, colon).trim()] = declaration.slice(colon + 1).trim();
  }
  return out;
}

function spTriggerNode(node, content, extra) {
  if ("text" in node) return node.text;
  if ("slot" in node) return node.slot === "content" ? content : null;
  const props = {};
  for (const [name, value] of Object.entries(node.attrs)) {
    if (value === undefined) continue;
    props[SP_TRIGGER_ATTRS[name] || name] = name === "style" ? spTriggerStyle(value) : value;
  }
  if (extra) {
    const { style, ...rest } = extra;
    Object.assign(props, rest);
    if (style) props.style = { ...(props.style || {}), ...style };
  }
  return createElement(node.tag, props, ...node.children.map((child) => spTriggerNode(child, content)));
}

function useSpTriggerForced() {
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

const SilverpointTrigger = forwardRef(function SilverpointTrigger(
  { ground, substrate, mode, size, seed, palette, variant, chevron, disabled, label, children, className, id, ...rest },
  ref,
) {
  const forcedPrecision = useSpTriggerForced();
  const props = { ground, substrate, mode, size, seed, palette, variant, disabled, label, className, id, type: "button" };
  const resolved = resolveUi(props, { forcedPrecision });
  const text = typeof children === "string" || typeof children === "number" ? String(children) : children == null ? undefined : "·";
  const view = uiButtonView(props, resolved, { text });
  // The chevron sits beside the label, as SpButton's own danger cross does.
  const tree = chevron
    ? { ...view, children: [...view.children, { tag: "svg", attrs: { part: "sp-mark", "data-glyph": "chevronDown", viewBox: "0 0 16 16", "aria-hidden": "true" }, children: [{ tag: "path", attrs: { d: UI_GLYPHS.chevronDown }, children: [] }] }] }
    : view;
  return spTriggerNode(tree, children, { ...rest, ref });
});
