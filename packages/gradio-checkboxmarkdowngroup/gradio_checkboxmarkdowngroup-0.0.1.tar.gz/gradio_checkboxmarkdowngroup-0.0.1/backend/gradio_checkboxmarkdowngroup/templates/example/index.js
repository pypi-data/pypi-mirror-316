const {
  SvelteComponent: u,
  append_hydration: m,
  attr: g,
  children: y,
  claim_element: v,
  claim_text: b,
  detach: _,
  element: w,
  init: E,
  insert_hydration: j,
  noop: h,
  safe_not_equal: q,
  text: C,
  toggle_class: s
} = window.__gradio__svelte__internal;
function D(a) {
  let e, i;
  return {
    c() {
      e = w("div"), i = C(
        /*names_string*/
        a[2]
      ), this.h();
    },
    l(t) {
      e = v(t, "DIV", { class: !0 });
      var n = y(e);
      i = b(
        n,
        /*names_string*/
        a[2]
      ), n.forEach(_), this.h();
    },
    h() {
      g(e, "class", "svelte-1gecy8w"), s(
        e,
        "table",
        /*type*/
        a[0] === "table"
      ), s(
        e,
        "gallery",
        /*type*/
        a[0] === "gallery"
      ), s(
        e,
        "selected",
        /*selected*/
        a[1]
      );
    },
    m(t, n) {
      j(t, e, n), m(e, i);
    },
    p(t, [n]) {
      n & /*type*/
      1 && s(
        e,
        "table",
        /*type*/
        t[0] === "table"
      ), n & /*type*/
      1 && s(
        e,
        "gallery",
        /*type*/
        t[0] === "gallery"
      ), n & /*selected*/
      2 && s(
        e,
        "selected",
        /*selected*/
        t[1]
      );
    },
    i: h,
    o: h,
    d(t) {
      t && _(e);
    }
  };
}
function I(a, e, i) {
  let { value: t } = e, { type: n } = e, { selected: d = !1 } = e, { choices: c } = e, o = t.map((l) => {
    var f;
    return (f = c.find((r) => r[1] === l)) == null ? void 0 : f[0];
  }).filter((l) => l !== void 0).join(", ");
  return a.$$set = (l) => {
    "value" in l && i(3, t = l.value), "type" in l && i(0, n = l.type), "selected" in l && i(1, d = l.selected), "choices" in l && i(4, c = l.choices);
  }, [n, d, o, t, c];
}
class V extends u {
  constructor(e) {
    super(), E(this, e, I, D, q, {
      value: 3,
      type: 0,
      selected: 1,
      choices: 4
    });
  }
}
export {
  V as default
};
