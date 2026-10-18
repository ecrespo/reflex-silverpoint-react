/* reflex-silverpoint-react — hand-inked frames for Knight Lab TimelineJS (sp_timeline, phase 2).
 *
 * TimelineJS builds its own DOM, so it cannot carry silverpoint's frame markup. The ground's frames
 * and tones are CSS masks whose images @silverpoint/grounds/ui.css assigns to
 * [part='sp-frame'][data-kind] and [part='sp-tone'][data-tone] inside an .sp-ui surface. This
 * component renders one hidden probe of each, reads the resolved mask variables from them, and
 * republishes them on the timeline's surface as --sp-kl-* custom properties. timeline.css then
 * paints TimelineJS's markers, eras and slides with the very same hand-drawn pieces. The probe is
 * re-read whenever the surface's ground, substrate, mode or frame variant changes.
 */
const SP_TIMELINE_CSS_ID = "sp-reflex-timeline";

function spInjectTimelineCss(css) {
  if (typeof document === "undefined" || document.getElementById(SP_TIMELINE_CSS_ID)) return;
  const style = document.createElement("style");
  style.id = SP_TIMELINE_CSS_ID;
  style.textContent = css;
  document.head.appendChild(style);
}

const SP_KL_FRAMES = ["control", "card", "round", "box", "pill"];
const SP_KL_TONES = ["1", "2", "3", "4"];

function SilverpointTimelineInk({ inked = true }) {
  const probeRef = useRef(null);
  useEffect(() => {
    spInjectTimelineCss(SP_TIMELINE_CSS);
    const probe = probeRef.current;
    const host = probe ? probe.closest(".sp-kl-timeline") : null;
    if (!host) return undefined;
    const read = () => {
      let any = false;
      for (const kind of SP_KL_FRAMES) {
        const piece = probe.querySelector(`[part='sp-frame'][data-kind='${kind}']`);
        const style = piece ? getComputedStyle(piece) : null;
        const mask = style ? style.getPropertyValue("--sp-ui-mask").trim() : "";
        const usable = inked && mask && mask !== "none" && host.getAttribute("data-mode") === "ink";
        any = any || Boolean(usable);
        host.style.setProperty(`--sp-kl-mask-${kind}`, usable ? mask : "none");
        host.style.setProperty(`--sp-kl-mask-position-${kind}`, style ? style.getPropertyValue("--sp-ui-mask-position").trim() || "center" : "center");
        host.style.setProperty(`--sp-kl-mask-size-${kind}`, style ? style.getPropertyValue("--sp-ui-mask-size").trim() || "100% 100%" : "100% 100%");
      }
      for (const level of SP_KL_TONES) {
        const piece = probe.querySelector(`[part='sp-tone'][data-tone='${level}']`);
        const style = piece ? getComputedStyle(piece) : null;
        const tone = style ? style.getPropertyValue("--sp-ui-tone").trim() : "";
        host.style.setProperty(`--sp-kl-tone-${level}`, tone || "none");
        host.style.setProperty(`--sp-kl-tone-size-${level}`, style ? style.getPropertyValue("--sp-ui-tone-size").trim() || "auto" : "auto");
      }
      host.setAttribute("data-kl-inked", any ? "true" : "false");
      host.setAttribute("data-kl-toned", probe.querySelector("[part='sp-tone']") && getComputedStyle(probe.querySelector("[part='sp-tone']")).getPropertyValue("--sp-ui-tone").trim() ? "true" : "false");
    };
    read();
    const observer = new MutationObserver(read);
    observer.observe(host, { attributes: true, attributeFilter: ["data-mode", "data-substrate", "data-ground", "data-frame", "class"] });
    return () => observer.disconnect();
  }, [inked]);
  return (
    <span ref={probeRef} className="sp-kl-probe" aria-hidden="true">
      {SP_KL_FRAMES.map((kind) => <span key={kind} part="sp-frame" data-kind={kind} />)}
      {SP_KL_TONES.map((level) => <span key={level} part="sp-tone" data-tone={level} />)}
    </span>
  );
}
