import { p as parser$1, f as flowDb } from "./flowDb-d35e309a-CHYLC-M2.js";
import { f as flowRendererV2, g as flowStyles } from "./styles-7383a064-BcOd--mb.js";
import { t as setConfig } from "./index-DHWIOlwj.js";
import "./graph-BhU2NOBf.js";
import "./layout-BByDPTGE.js";
import "./index-8fae9850-B8WFjSCl.js";
import "./clone-Bgssf9ER.js";
import "./edges-d417c7a0-CdFz1mwR.js";
import "./createText-423428c9-CITa5lJU.js";
import "./line-BGRsXZzv.js";
import "./array-DgktLKBx.js";
import "./path-Cp2qmpkd.js";
import "./channel-TKBtP1oX.js";
const diagram = {
  parser: parser$1,
  db: flowDb,
  renderer: flowRendererV2,
  styles: flowStyles,
  init: (cnf) => {
    if (!cnf.flowchart) {
      cnf.flowchart = {};
    }
    cnf.flowchart.arrowMarkerAbsolute = cnf.arrowMarkerAbsolute;
    setConfig({ flowchart: { arrowMarkerAbsolute: cnf.arrowMarkerAbsolute } });
    flowRendererV2.setConf(cnf.flowchart);
    flowDb.clear();
    flowDb.setGen("gen-2");
  }
};
export {
  diagram
};
//# sourceMappingURL=flowDiagram-v2-49332944-m8bMOiRU.js.map
