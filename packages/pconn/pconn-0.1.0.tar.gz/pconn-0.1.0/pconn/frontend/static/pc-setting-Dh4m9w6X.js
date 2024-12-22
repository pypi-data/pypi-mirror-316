import { t as c, a as u, j as g, x as e } from "./index-B4ls59Y5.js";
var l = Object.defineProperty, m = Object.getOwnPropertyDescriptor, w = (a, r, n, s) => {
  for (var t = s > 1 ? void 0 : s ? m(r, n) : r, i = a.length - 1, p; i >= 0; i--)
    (p = a[i]) && (t = (s ? p(r, n, t) : p(t)) || t);
  return s && t && l(r, n, t), t;
};
const h = [
  {
    path: "plugins",
    render: () => e`<pc-settings-plugins></pc-settings-plugins>`,
    enter: async () => (await import("./pc-settings-plugins-ClEkrUc_.js"), !0)
  },
  {
    path: "logs",
    render: () => e`<pc-logs></pc-logs>`,
    enter: async () => (await import("./pc-logs-Dqg-E63g.js"), !0)
  },
  {
    path: "workstations",
    render: () => e`<pc-settings-workstations></pc-settings-workstations>`,
    enter: async () => (await import("./pc-settings-workstations-Cbqg_MPC.js"), !0)
  },
  {
    path: "system",
    render: () => e`<pc-settings-system></pc-settings-system>`,
    enter: async () => (await import("./pc-settings-system-B4hEr06r.js"), !0)
  }
];
let o = class extends u {
  constructor() {
    super(...arguments), this._routes = new g(this, h);
  }
  render() {
    return e`${this._routes.outlet()}`;
  }
};
o = w([
  c("pc-setting")
], o);
