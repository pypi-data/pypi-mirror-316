import { p as o, a as m, h as c, b as p, x as d, t as u } from "./index-B4ls59Y5.js";
import "./filled-button-B0GLItPe.js";
import "./pc-expansion-panel-3kiRKGtk.js";
import { s as h } from "./styles-CHllVapX.js";
var v = Object.defineProperty, _ = Object.getOwnPropertyDescriptor, f = (t, e, l, i) => {
  for (var s = i > 1 ? void 0 : i ? _(e, l) : e, n = t.length - 1, r; n >= 0; n--)
    (r = t[n]) && (s = (i ? r(e, l, s) : r(s)) || s);
  return i && s && v(e, l, s), s;
};
let a = class extends m {
  constructor() {
    super(...arguments), this._fetchData = new c(
      this,
      async () => (await p.getRequest("/config/system")).data.result,
      () => []
    );
  }
  render() {
    return d`
      <pc-card outlined header="Platform Connectors">
        ${this._fetchData.render({
      complete: (t) => d`
            <div class="card-content">
              <md-list>
                <md-list-item>
                  <div slot="headline">Version <b>${t.version}</b></div>

                  <md-filled-button slot="end" @click=${this._updateLicense}
                    >UPDATE LICENSE</md-filled-button
                  >
                </md-list-item>
                <md-list-item>
                  <div slot="headline">Workstations</div>
                  <div slot="end">
                    ${t.assigned_workstations}/${t.licensed_workstations}
                  </div>
                </md-list-item>
                <md-list-item>
                  <pc-expansion-panel header="Plugins">
                    <md-list
                      >${t.plugins.map(
        (e) => d`<md-list-item>${e}</md-list-item>`
      )}</md-list
                    >
                  </pc-expansion-panel>
                </md-list-item>
              </md-list>
            </div>
          `
    })}
      </pc-card>
    `;
  }
  _updateLicense() {
    import("./pc-license-DxMj2WyV.js").then(() => {
      var e;
      const t = document.createElement("pc-license");
      t.allowClose = !0, (e = this.shadowRoot) == null || e.appendChild(t);
    });
  }
};
a.styles = [o, h];
a = f([
  u("pc-settings-system")
], a);
export {
  a as SystemSettings
};
